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

        for i in range(3, len(signal) - samples_per_bit + 1, samples_per_bit):
            if i + samples_per_bit >= len(signal):
                break

            current_sample = signal[i]
            next_sample = signal[i + samples_per_bit]

            if current_sample < next_sample:
                decoded_bits.append(0)
            elif current_sample > next_sample:
                decoded_bits.append(1)
            else:
                decoded_bits.append(current_sample)

        print(f"Decoded bits: {decoded_bits}")  # Debug statement
        return decoded_bits

    def find_sfd_end(decoded_bits):
        # Padrão do SFD
        sfd_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1]
        sfd_len = len(sfd_pattern)

        # Percorre a lista de bits
        for i in range(len(decoded_bits) - sfd_len + 1):
            # Verifica se os bits atuais correspondem ao padrão do SFD
            if decoded_bits[i:i + sfd_len] == sfd_pattern:
                print(f"SFD encontrado na posição {i}")
                return i + sfd_len  # Retorna a posição após o fim do SFD

        print("SFD não encontrado")
        return -1  # Retorna -1 se o SFD não for encontrado

    def convert_bits_to_bytes(bits):
        frame_bytes = []
        byte = ''
        bit_count = 0
        for bit in bits:
            byte += str(bit)
            bit_count += 1
            if bit_count == 8:
                frame_bytes.append(int(byte[::-1], 2))
                byte = ''
                bit_count = 0

        print(f"Converted bytes: {frame_bytes}")  # Debug statement
        return bytes(frame_bytes)

    def extract_frame_bytes(decoded_bits, sfd_end_index):
        print("DECODE: ", decoded_bits[sfd_end_index:sfd_end_index+8])
        frame_bits = decoded_bits[sfd_end_index:]
        return convert_bits_to_bytes(frame_bits)

    decoded_bits = decode_manchester(sig)

    try:
        sfd_end_index = find_sfd_end(decoded_bits)
    except ValueError as e:
        print(f"Error finding SFD: {e}")
        return bytes()

    frame_bytes = extract_frame_bytes(decoded_bits, sfd_end_index)

    print(f"Final decoded frame bytes: {frame_bytes}")  # Debug statement
    return frame_bytes
