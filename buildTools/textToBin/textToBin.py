import sys

args_len = len(sys.argv)
binary = bytearray(b'')

if(args_len == 3):
    textFilePath = sys.argv[1]
    binFilePath = sys.argv[2]
    textFile = open(textFilePath, "r")
    binFile = open(binFilePath, 'wb')
    
    for line in textFile:
        val = 0
        line = line.split("\n")[0]
        
        if line[0] == "1":
            val += 128
        if line[1] == "1":
            val += 64
        if line[2] == "1":
            val += 32
        if line[3] == "1":
            val += 16
        if line[4] == "1":
            val += 8
        if line[5] == "1":
            val += 4
        if line[6] == "1":
            val += 2
        if line[7] == "1":
            val += 1
        print(line)
        binFile.write(val.to_bytes(1,"big"))

if(args_len != 3):
    print("\nUsage: python3 textToBin.py [textFilePath] [binFilePath]")
