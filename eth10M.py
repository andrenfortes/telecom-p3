def decode(sig):

    sfd_index = -1
    manchester_dec = []
    internet_frame = []
    counter = 0

    for i in range(len(sig)):
        counter += 1
        if sig[i-1] != sig[i] and counter >= 7:
            manchester_dec.append(sig[i])
            counter = 0

    # Busca pelo SFD (1, 1 seguidos)
    for i in range(1, len(manchester_dec)):
        if manchester_dec[i-1] == 1 and manchester_dec[i] == 1:
            sfd_index = i + 1
            break

    # Remover o preâmbulo e SFD
    manchester_dec = manchester_dec[sfd_index:]

    for i in range(0, len(manchester_dec), 8):
        byte = manchester_dec[i:i + 8]
        byte_invertido = byte[::-1]  # Inverte o byte
        valor_int = int("".join(str(x) for x in byte_invertido), 2)
        internet_frame.append(valor_int)

    return bytes(internet_frame[:-1])

