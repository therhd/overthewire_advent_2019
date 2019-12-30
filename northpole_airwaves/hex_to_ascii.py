string = '7370726561645f584d41535f63683333723a5f7331'
string = '9562081468050e17050e80551054687a8f05442fc1'
ascii = ''
for i in range(0, len(string), 2):
    pair = string[i:i+2]
    ascii = ascii + chr(int(pair, 16))
    
print(ascii)
