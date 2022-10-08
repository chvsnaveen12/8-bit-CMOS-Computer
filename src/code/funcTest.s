;var0 = 0x8000
;var1 = 0x8001
;var2 = 0x8002
;var3 = 0x8003
;var4 = 0x8004
;var5 = 0x8005
;var6 = 0x8006
;var7 = 0x8007

;add0 = 0x8008
;add1 = 0x800a
;add2 = 0x800c
;add3 = 0x800e

;The variables above are general use variables to be used anywhere for data storages
                

                #org 0x0000 	

START:          LDI 0xfe
                STA 0xbfff
sus:            LDA var4
                PHS 
                JPS FILL_SCREEN
                INB var4
                JPA sus

FILL_SCREEN:    LDS 0x03
                STA var0
                CLB var1

loopA:          LDA var1
                CPI 0x1e
                BEQ loopA_exit
                STA add0
                CLB var2

loopB:          LDA var2
                CPI 0x28
                BEQ loopB_exit
                ADI 0xc0
                STA add0+1
                LDA var0
                STR add0
                INB var2
                JPA loopB

loopB_exit:     INB var1
                JPA loopA
loopA_exit:     RTS