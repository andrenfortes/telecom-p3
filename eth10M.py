def decode(sig):
    def decode_manchester(signal):
        decoded_bits = []
        sample_rate = 81  # MHz
        bit_rate = 10  # Mbps
        samples_per_bit = sample_rate * 1_000_000 // bit_rate
        
        # Assumindo que o sinal tem amostras de 1 bit por vez.
        bit_duration = len(signal) // (samples_per_bit * 2)
        
        if bit_duration == 0:
            raise ValueError("Bit duration cannot be zero.")
        
        last_value = signal[0]
        current_bit = None
        transition_count = 0
        
        for i in range(1, len(signal)):
            if signal[i] != last_value:
                transition_count += 1
                if transition_count >= (samples_per_bit // 2):
                    if current_bit is None:
                        current_bit = 1 if signal[i] > last_value else 0
                    else:
                        decoded_bits.append(current_bit)
                        current_bit = 1 if signal[i] > last_value else 0
                    transition_count = 0
                last_value = signal[i]

        # If the last bit wasn't appended, add it.
        if current_bit is not None:
            decoded_bits.append(current_bit)
        
        return decoded_bits

    def align_and_extract_frame(decoded_bits):
        sfd_pattern = [1, 0, 1, 0, 1, 0, 1, 1]
        sfd_index = -1

        # Encontrar o início do padrão SFD
        for i in range(len(decoded_bits) - len(sfd_pattern) + 1):
            if decoded_bits[i:i + len(sfd_pattern)] == sfd_pattern:
                sfd_index = i + len(sfd_pattern)
                break

        if sfd_index == -1:
            raise ValueError("SFD not found in the decoded bits!")

        # Extraindo bytes após o SFD
        frame_bits = decoded_bits[sfd_index:]
        frame_bytes = []

        for i in range(0, len(frame_bits), 8):
            byte = 0
            for bit in frame_bits[i:i+8]:
                byte = (byte << 1) | bit
            frame_bytes.append(byte)

        return bytes(frame_bytes)

    # Passo 1: Decodificar o sinal Manchester para bits
    decoded_bits = decode_manchester(sig)
    
    # Passo 2: Alinhar com o primeiro byte do quadro e extrair bytes do quadro
    frame_bytes = align_and_extract_frame(decoded_bits)

    return frame_bytes
