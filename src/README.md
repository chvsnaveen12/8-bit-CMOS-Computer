# Build environment
This is the usual build environment. All the code resides in /code. Download [prom.exe by slu4](https://github.com/slu4coder/SST39SF010-FLASH-Programmer) and place it in this folder.
### Usual commands

##### Assemble OS.s
```
   python3 assembler/asm.py code/OS.s
```
##### Flash the ROM
```
   prom.exe assembler\output.bin
 ```

### File strucure
    .
    └── src                    # The usual build environment
        ├── assembler          # The assembler used to assemble code
        │   ├── asm.py         # main assembler code 
        │   ├── check.bin      # reading back from the FLASH to get the checksum
        │   └── output.bin     # output of the assembler which has to be flashed
        ├── backUpCode
        │   └── OSbackup.s     # local backup
        ├── charset            # charset for the gpu
        │   ├── charset.bin    # charset.txt but in binary format
        │   └── charset.txt    # contains 2048 bytes in ascii format of the charset
        ├── code               # main code resides here
        │   ├── funcTest.s
        │   ├── OS.s           # the code running on the CPU
        │   ├── OS.txt         # OS.s but in txt format for easy viewing
        │   ├── snake.s
        │   └── textEditor.s
        ├── microcode          # control microcode for the control unit 
        │   ├── left.bin       # left.txt but in binary format
        │   ├── left.txt       # contains 16384 bytes of the left control ROM/FLASH in ascii
        │   ├── right.bin      # right.txt but in binary format
        │   └── right.txt      # contains 16384 bytes of the right control ROM/FLASH in ascii
        ├── textToBin
        │   └── textToBin.py   # used to convert charset.txt, left.txt and right.txt into binary
        └── prom.exe           # used to upload the binary files to ROM/FLASH chips
