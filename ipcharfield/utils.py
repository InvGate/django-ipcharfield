from netaddr import IPAddress


def leading_zeros_repr(ip_address: IPAddress) -> str:
    if ip_address.version == 4:
        delimiter = '.'
        chunks_size = 3
    else:
        delimiter = ':'
        chunks_size = 4

    return leading_zeros_repr_with_delimiter(ip_address, delimiter, chunks_size)


def leading_zeros_repr_with_delimiter(ip_address: IPAddress, delimiter: str, chunks_size: int) -> str:
    chunks = str(ip_address).split(delimiter)

    if ip_address.version == 6:
        chunks = curate_chunks(chunks)

    for i in range(len(chunks)):
        chunks[i] = '{}{}'.format(''.join('0' for j in range(chunks_size - len(chunks[i]))), chunks[i])
    return delimiter.join(chunks)


def curate_chunks(chunks):
    """
    :param chunks: array of chunks between : delimiter of a ipv6

    In the very specific case of ipv6 one can have the :: occurrence which means 0000 chunks altogether.
    After the operation, the chunks with the form ['fff3', 'db03', '', '4']
                         will result in ['fff3', 'db03', '0000', '0000', '0000', '0000', '0000', '4']
    """
    new_chunks = []
    missing_chunks = 9 - len(chunks)
    for chunk in chunks:
        if chunk != '':
            new_chunks.append(chunk)
        else:
            for i in range(missing_chunks):
                new_chunks.append('0000')
            missing_chunks = 0
    return new_chunks


def ip_address_repr(value: str) -> str:
    return ip_address_repr_with_delimiter(value, '.' if '.' in value else ':')


def ip_address_repr_with_delimiter(value: str, delimiter: str) -> str:
    chunks = value.split(delimiter)
    for i in range(len(chunks)):
        last_0_index = 0
        while last_0_index < len(chunks[i]) - 1 and chunks[i][last_0_index] == '0':
            last_0_index += 1
        chunks[i] = chunks[i][last_0_index:]
    return str(IPAddress(delimiter.join(chunks)))
