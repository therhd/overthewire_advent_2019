def flip_bits(symbols: str):
    symbols_flipped = ''
    for symbol in list(symbols):
        if symbol == '1':
            symbols_flipped = '{}{}'.format(symbols_flipped, '0')
        else:
            symbols_flipped = '{}{}'.format(symbols_flipped, '1')
    return symbols_flipped


def decode_pair_symbols(symbols: str, one: str, zero: str):
    symbol_pair = ''
    bits = ''
    for symbol in list(symbols):
        symbol_pair = '{}{}'.format(symbol_pair, symbol)
        if len(symbol_pair) == 2:
            if symbol_pair == zero:
                bits = '{}{}'.format(bits, '0')
            if symbol_pair == one:
                bits = '{}{}'.format(bits, '1')
            symbol_pair = ''
    return bits


def bits_to_bytes(bits: str, endian: str='little'):
    return int(bits, 2).to_bytes((len(bits) + 7) // 8, endian)


def display(bits: str):
    bytes_ = bits_to_bytes(bits, 'little')
    # print('Base Symbols   :   {}'.format(' '.join([symbols[i:i+2] for i in range(0, len(symbols), 2)])))
    print('Bits           :   {}'.format(' '.join([bits[i:i+8] for i in range(0, len(bits), 8)])))
    print('Hex            :   {}'.format(bytes_.hex()))
    print('Chars          :   {}'.format(bytes_))
    print('UTF Chars only :   {}'.format(bytes_.decode('utf-8','ignore')))


symbols = '10101010111000010111011101110111000010101010111000010101111010000101010101000010101011100001010101010001110111010101000011101110101010100001110101010001010101010000101010101110000111010101010000111011101110101000010101011101110000101010111011100001010101010000101011101000011101010101000010101110111011100001110101010100001010101010000101010111011100001010101010000111011101010100001010101011100001010101010000101011101000011101110101010000111011101010100001110101010100001011101110111011100001110111010101000011101110111011101000010101010100001010111010000111011101010100001010101011100001010101110111000011101110111011101110000101010101000010101110100000000'
#symbols = flip_bits(symbols)
for i in range(0,7):
    data = decode_pair_symbols(symbols, one='11', zero='01')
    display(data)
    symbols = symbols[2:]


# Do a loop through all possible mutations here