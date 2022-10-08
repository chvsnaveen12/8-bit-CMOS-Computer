desperateFood:  LDI 0x06
                    STA add0
                    LDI 0xc2
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0xe5
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0x1b
                    STA add0
                    LDI 0xc2
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0xe5
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0x0b
                    STA add0
                    LDI 0xd3
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0x17
                    STA add0
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0x11
                    STA add0
                    LDI 0xca
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood

                    LDI 0x1e
                    STA add0+1
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood