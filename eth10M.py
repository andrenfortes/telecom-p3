def decode(sig):
    def decode_manchester(signal):
        decoded_bits = []
        sample_rate = 81_000_000  # Hz (81 MHz)
        bit_rate = 10_000_000     # Hz (10 Mbps)
        samples_per_bit = sample_rate // bit_rate

        if samples_per_bit <= 0:
            raise ValueError("samples_per_bit must be greater than zero.")

        mid_sample_pos = samples_per_bit // 2

        if len(signal) < samples_per_bit:
            raise ValueError("Signal length is too short for the given sample rate and bit rate.")

        for i in range(0, len(signal) - samples_per_bit + 1, samples_per_bit):
            if i + mid_sample_pos >= len(signal):
                break

            current_sample = signal[i]
            next_sample = signal[i + mid_sample_pos]

            if current_sample == 0 and next_sample == 1:
                decoded_bits.append(0)
            elif current_sample == 1 and next_sample == 0:
                decoded_bits.append(1)
            else:
                decoded_bits.append(-1)  # Invalid transition

        cleaned_bits = [bit for bit in decoded_bits if bit != -1]
        print(f"Decoded bits: {cleaned_bits}")  # Debug statement
        return cleaned_bits

    def find_sfd_end(decoded_bits):
        sfd_pattern = [1, 0, 1, 0, 1, 0, 1, 1]
        sfd_len = len(sfd_pattern)
        max_mismatches = 2

        for i in range(len(decoded_bits) - sfd_len + 1):
            mismatches = sum(1 for j in range(sfd_len) if decoded_bits[i + j] != sfd_pattern[j])
            if mismatches <= max_mismatches:
                print(f"SFD found at index: {i + sfd_len}")  # Debug statement
                return i + sfd_len

        raise ValueError("Start Frame Delimiter (SFD) not found in the decoded bits!")

    def convert_bits_to_bytes(bits):
        frame_bytes = []
        byte = 0
        bit_count = 0
        for bit in bits:
            byte = (byte << 1) | bit
            bit_count += 1
            if bit_count == 8:
                frame_bytes.append(byte)
                byte = 0
                bit_count = 0
        if bit_count > 0:
            frame_bytes.append(byte << (8 - bit_count))  # Pad remaining bits
        print(f"Converted bytes: {frame_bytes}")  # Debug statement
        return bytes(frame_bytes)

    def extract_frame_bytes(decoded_bits, sfd_end_index):
        frame_bits = decoded_bits[sfd_end_index:]
        return convert_bits_to_bytes(frame_bits)

    decoded_bits = decode_manchester(sig)

    try:
        sfd_end_index = find_sfd_end(decoded_bits)
    except ValueError as e:
        print(f"Error finding SFD: {e}")
        return bytes()

    frame_bytes = extract_frame_bytes(decoded_bits, sfd_end_index)

    mac_address_length = 6
    if len(frame_bytes) >= mac_address_length:
        frame_bytes = frame_bytes[mac_address_length:]
    
    if len(frame_bytes) > 0 and frame_bytes[0] == 0x00:
        frame_bytes = frame_bytes[1:]

    print(f"Final decoded frame bytes: {frame_bytes}")  # Debug statement
    return frame_bytes
