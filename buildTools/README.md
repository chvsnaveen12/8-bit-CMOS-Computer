# Build tools
Provides an outline for the usage of the tools used while development.

## Assembler
asm.py is a modified version of the assembler written by [slu4](https://github.com/slu4coder/Minimal-UART-CPU-System)

I only added one feature, which I thought was essential to the process of writing in assembly(for my project), VARIABLES. Every other aspect of the assembler remained the same. 

 ### Variable usage
 This works like #define in C. We declare the variables at the top, and  the assembler replaces the variable everywhere in the code before doing  its first pass.
 
 ```
    ;snakeLength = 0x8010
    ;0inhex      = 0x00
  ```
  where ever snakeLength shows up, it gets replaced by 0x8010. And 0inhex by 0x00.
 
```
   ;snakeLength = 0x8010    ;Placing a comment right after, will result in a crash.
 ```
  
 Change the fileSeperator variable in [asm.py]() depending on your platform

```
   fileSeparator = '\\' #for windows
   fileSeparator = '/'  #for linux or macOS
 ```

### Usage
```
   python3 asm.py {PATH_TO_SOURCE}
 ```
 After running the command, python creates an output.bin file.
 
## Text to binary
I wrote all my microcode in text files, this converts the ascii format to binary.

### Usage
```
   python3 textToBin.py {PATH_TO_TEXT_FILE} {PATH_TO_BINARY_FILE}
 ```
 If the binary file is not present python will create it.
 
 If the binary file is present python will overwrite it.
 
 ### Format
 Ascii files should just contain a byte per line.

 ##### Example:
 ```
   01010101
   10101010
   11111111
   00000000
 ```
 

