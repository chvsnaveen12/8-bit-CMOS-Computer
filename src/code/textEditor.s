
    textEditorLoop: KSO                 ;main loop of textEditor
                    AND 0x07            ;get the size of keyboard buffer
                    CPI 0x00            ;wait till it isnt zero
                    BEQ textEditorLoop
                    KBO                 ;take the keyboard byte and do some tests
                    
        exitCheck:  CPI 0x76
                    BNE backspace
                    JPA START

        backspace:  CPI 0x66
                    BNE notbkspace
                    LDA f0Flag
                    CPI 0x01
                    BEQ bkspacef0
                    CLB f0Flag
                    LDI 0x00
                    STR cursorCords
                    DEB cursorCords+1
                    LDI 0x0a
                    STR cursorCords
                    JPA textEditorLoop

        bkspacef0:  CLB f0Flag
                    JPA textEditorLoop

        notbkspace: CPI 0xf0            ;check if byte is 0xf0
                    BNE notf0
                    CLB f0Flag          ;if byte is 0xf0 set f0Flag and loop over
                    INB f0Flag
                    JPA textEditorLoop

        notf0:      STA var0            ;store the data in var0 for future
                    LDA f0Flag
                    CPI 0x01            ;check if previous byte was 0xf0
                    BEQ previousf0



        noF0Before: CLB f0Flag          ;clear the f0Flag
                    LDA var0            ;get the keyboard data back
                    CPI 0x12
                    BEQ shft
                    CPI 0x59
                    BEQ shft
                    JPA notShift
            shft:   CLB shiftFlag
                    INB shiftFlag
                    JPA textEditorLoop

        previousf0: CLB f0Flag          ;clear the f0Flag
                    LDA var0            ;get the keyboard data back
                    CPI 0x12
                    BEQ shftf0
                    CPI 0x59
                    BEQ shftf0
                    JPA notShiftf0
            shftf0: CLB shiftFlag
                    JPA textEditorLoop
        
        notShift:   STA add0
                    LDA shiftFlag
                    CPI 0x00
                    BEQ small

            big:    CLB add0+1
                    INB add0+1
                    JPA int

            small:  CLB add0+1


            int:    LDR add0
                    STR cursorCords
                    INB cursorCords+1
                    LDI 0x0a
                    STR cursorCords
                    JPA textEditorLoop

        notShiftf0: JPA textEditorLoop

