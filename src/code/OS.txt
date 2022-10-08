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

;all the variables above are general use variables to be used anywhere for data storages



;snakeLength    = 0x8010
;snakeDir       = 0x8011
;foodCords will also occupy 0x8013 since its an address
;foodCords      = 0x8012
;rngSeed        = 0x8014
;score          = 0x8015
;snakeTime      = 0x8016
;tempSnakeDir   = 0x8017
;f0Flag         = 0x8018

;cursorCords will also occupy 0x801a since its an address
;cursorCords    = 0x8019
;shiftFlag      = 0x801b
;behindCursor   = 0x801c

;all the variables above are specific use variables to be usedin particular places



                    #org 0x0000 	
                    JPA START
;---------------------------------------------------Key Map-----------------------------------------------------------------------

keymapNormal:
    '?????????? `?'                 ;00-0F  removed the first 3 bytes as they are occupied by JPA START
    '?????q1???zsaw2?'              ;10-1F  this page will be on the first page of the ROM
    '?cxde43?? vftr5?'              ;20-2F  keeping it like this makes it easier to map
    '?nbhgy6???mju78?'              ;30-3F
    '?,kio09??./l;p-?'              ;40-4F
    '??',39,'?[=????',10,']?\??'    ;50-5F
    '?????????1?47???'              ;60-6F
    '0.2568',27,'??+3-*9??'         ;70-7F
    '????????????????'              ;80-8F
    '????????????????'              ;90-9F
    '????????????????'              ;A0-AF
    '????????????????'              ;B0-BF
    '????????????????'              ;C0-CF
    '????????????????'              ;D0-DF
    '????????????????'              ;E0-EF
    '????????????????'              ;F0-FF
keymapShifted:
    '????????????? ~?'              ;00-0F  this section will be on the second page of the ROM
    '?????Q!???ZSAW@?'              ;10-1F
    '?CXDE#$?? VFTR%?'              ;20-2F
    '?NBHGY^???MJU&*?'              ;30-3F
    '?<KIO)(??>?L:P_?'              ;40-4F
    '??"?{+?????}?|??'              ;50-5F
    '?????????1?47???'              ;60-6F
    '0.2568???+3-*9??'              ;70-7F
    '????????????????'              ;80-8F
    '????????????????'              ;90-9F
    '????????????????'              ;A0-AF
    '????????????????'              ;B0-BF
    '????????????????'              ;C0-CF
    '????????????????'              ;D0-DF
    '????????????????'              ;E0-EF
    '????????????????'              ;F0-FF

;---------------------------------------------------------------------------------------------------------------------------------


;---------------------------------------------------Main--------------------------------------------------------------------------

START:              LDI 0xfe
                    STA 0xbfff          ;initialize the stack pointer
                    JPS bufferFlush     ;removes garbage values from the buffer
    
mainScreen:         CLB var0            ;var0 contains character to fill screen with
                    JPS fillScreen      ;this will clear the screen

                    CLB var3
                    JPS drawBorder      ;draws the normal border
        
    mainTextInit:   LDI 0x10            ;prints main screen text
                    STA var0
                    LDI 0x02
                    STA var1
                    LDI <osName
                    STA add0
                    LDI >osName
                    STA add0+1
                    JPS printText       ;prints the osName

                    LDI 0x02
                    STA var0
                    LDI 0x0e
                    STA var1
                    LDI <option1
                    STA add0
                    LDI >option1
                    STA add0+1
                    JPS printText       ;prints option1 which is snake

                    LDI 0x02
                    STA var0
                    LDI 0x10
                    STA var1
                    LDI <option2
                    STA add0
                    LDI >option2
                    STA add0+1
                    JPS printText       ;prints option2 which is textEditor

                    LDI 0x04
                    STA var0
                    LDI 0x1c
                    STA var1
                    LDI <bottom
                    STA add0
                    LDI >bottom
                    STA add0+1
                    JPS printText       ;prints the website link

    branchCheck:    CLB var0            ;check if any meaningful button is pressed
                    JPS checkKBMenu
                    LDA var0
                    CPI 0x00
                    BEQ snakeJMP
                    CPI 0x01
                    BEQ textJMP
                    CPI 0x02
                    BEQ secretMsg       ;print the secret message
                    JPA branchCheck
        
        secretMsg:  LDI 0x08            ;prints a secret message
                    STA var0
                    LDI 0x1a
                    STA var1
                    LDI <special
                    STA add0
                    LDI >special
                    STA add0+1
                    JPS printText
                    JPA branchCheck

        snakeJMP:   JPS snake           ;makes a subroutine jump to snake
                    JPA mainScreen
    
        textJMP:    JPS textEditor      ;makes a subroutine jump to textEditor
                    JPA mainScreen

textEditor:         CLB var0            ;var0 contains character to fill screen with
                    JPS fillScreen      ;this will clear the screen

                    CLB f0Flag          ;initialize the mandatory variables
                    CLB shiftFlag
                    CLB behindCursor
                    LDI 0x05            
                    STA cursorCords
                    LDI 0xc1
                    STA cursorCords+1   ;initialize cursorCords
                    LDI 0x0a
                    STR cursorCords     ;print the cursor in cursorCords

                    CLB var3
                    JPS drawBorder      ;draw the normal border

    textEditorinit: LDI 0x0e            ;prints some text
                    STA var0
                    LDI 0x02
                    STA var1
                    LDI <textEditorText
                    STA add0
                    LDI >textEditorText
                    STA add0+1
                    JPS printText       ;prints textEditor

                    LDI 0x04
                    STA var0
                    LDI 0x0f
                    STA var1
                    LDI <pressExitTxt
                    STA add0
                    LDI >pressExitTxt
                    STA add0+1
                    JPS printText       ;prints exit message
    
        wait:       LDI 0xff            ;wait for 2 seconds            
                    STA var0
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS delay
                    JPS bufferFlush


        erase:      LDI 0x04            ;erase the exit message
                    STA var0
                    LDI 0x0f
                    STA var1
                    LDI <eraser
                    STA add0
                    LDI >eraser
                    STA add0+1
                    JPS printText       ;prints spaces over the exit message

    textEditorLoop: KSO                 ;main loop of textEditor
                    AND 0x07            ;get the size of keyboard buffer
                    CPI 0x00            ;wait till it isnt zero
                    BEQ textEditorLoop
                    KBO                 ;take the keyboard byte and do some tests

                    CPI 0x76            ;check for escape
                    BEQ START           ;exit if pressed

                    CPI 0xe0            ;check if byte is 0xe0
                    BEQ textEditorLoop  ;ignore

                    CPI 0xf0            ;check if byte if 0xf0            
                    BEQ f0

                    STA var0            ;store keyboard data to be used later
                    LDA f0Flag
                    CPI 0x01            ;check the f0Flag and proceed accordingly
                    BEQ f0Before

        nof0Before: LDA var0            ;get the keybaord data back from var0
                    CPI 0x66            ;do some tests and branch            
                    BEQ backspace
                    CPI 0x5a
                    BEQ enter
                    CPI 0x75
                    BEQ arrowUp
                    CPI 0x74
                    BEQ arrowRight
                    CPI 0x72
                    BEQ arrowDown
                    CPI 0x6b
                    BEQ arrowLeft
                    CPI 0x12
                    BEQ shiftDown
                    CPI 0x59
                    BEQ shiftDown
                    
                    STA add0            ;store the keyboard data into lower 8-bits of add0
                    LDA shiftFlag       ;depending on shiftFlag, set upper 8-bits of add0 to 0x00 or 0x01
                    CPI 0x01
                    BEQ big
            
            small:  CLB add0+1
                    JPA ascii

            big:    LDI 0x01
                    STA add0+1

            ascii:  LDR add0            ;get the ascii value from the keyboard scancode
                    STR cursorCords     ;store it in place of cursor
                    CLB var1
                    JPS autoMoveCursor  ;move the cursor to the right
                    LDI 0x0a
                    STR cursorCords     ;print the new cursor

        f0Before:   CLB f0Flag          ;since current byte is not f0, clear the flag
                    LDA var0            ;get the keybaord data back from var0
                    CPI 0x12
                    BEQ shiftUp         ;left shift has been pressed
                    CPI 0x59
                    BEQ shiftUp         ;right shift has been pressed
                    JPA textEditorLoop

        shiftDown:  LDI 0x01            ;set shift flag to 0x01 as shift has been pressed     
                    STA shiftFlag
                    JPA textEditorLoop

        shiftUp:    CLB shiftFlag       ;clear the shift flag as it has been released
                    JPA textEditorLoop

        arrowUp:    LDA cursorCords     ;if cursor is already at the top, dont do anything
                    CPI 0x05
                    BEQ textEditorLoop
                    
                    LDA behindCursor    ;replace the character which was behind the cursor previously
                    STR cursorCords

                    DEB cursorCords     ;change the cursor cordinates and store the character into behindCursor
                    LDR cursorCords
                    STA behindCursor

                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop

        arrowRight: LDA cursorCords+1   ;if cursor is already at the top, dont do anything
                    CPI 0xe6
                    BEQ textEditorLoop
                    
                    LDA behindCursor    ;replace the character which was behind the cursor previously
                    STR cursorCords

                    INB cursorCords+1   ;change the cursor cordinates and store the character into behindCursor
                    LDR cursorCords
                    STA behindCursor

                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop

        arrowDown:  LDA cursorCords     ;if cursor is already at the top, dont do anything
                    CPI 0x1c
                    BEQ textEditorLoop
                    
                    LDA behindCursor    ;replace the character which was behind the cursor previously
                    STR cursorCords

                    INB cursorCords     ;change the cursor cordinates and store the character into behindCursor
                    LDR cursorCords
                    STA behindCursor

                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop

        arrowLeft:  LDA cursorCords+1   ;if cursor is already at the top, dont do anything
                    CPI 0xc1
                    BEQ textEditorLoop
                    
                    LDA behindCursor    ;replace the character which was behind the cursor previously
                    STR cursorCords

                    DEB cursorCords+1   ;change the cursor cordinates and store the character into behindCursor
                    LDR cursorCords
                    STA behindCursor

                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop

        enter:      LDA cursorCords     ;if cursor is at the bottom of the screen, then exit
                    CPI 0x1c
                    BNE moveDo
                    JPA textEditorLoop

            moveDo: LDA behindCursor    ;replace the character which was behind the cursor
                    STR cursorCords

                    INB cursorCords     ;increment the y_cord and set x_cord to 0xc1
                    LDI 0xc1
                    STA cursorCords+1
                    
                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop
        
        backspace:  CLE                 ;clear the current cursor
                    STR cursorCords
                    LDI 0x01            ;var1 == 0x01 will result in left cursor shift
                    STA var1            
                    JPS autoMoveCursor  
                    
                    LDI 0x0a            ;print the new cursor
                    STR cursorCords
                    JPA textEditorLoop

        f0:         LDI 0x01
                    STA f0Flag          ;set f0Flag to 0x01          
                    JPA textEditorLoop

;the only external function of textEditor       
autoMoveCursor:     LDA var1            ;if var1 == 0x01 , cursor move left. else it will move towards the right
                    CPI 0x01
                    BEQ left

    right:          LDA cursorCords+1   ;check if we cannot move to right anymore
                    CPI 0xe6
                    BEQ overflowR
                    INB cursorCords+1   ;if we can move towards the right, move towards the right
                    LDR cursorCords     ;store the character at the new cursorCords into behindCursor
                    STA behindCursor
                    RTS
        
        overflowR:  LDA cursorCords     ;check if we can move downwards
                    CPI 0x1c
                    BNE moveD
                    RTS                 ;if we cannot down, dont do anything
            
            moveD:  LDI 0xc1            ;if we can move down, move down one step and to the left most character
                    STA cursorCords+1   
                    INB cursorCords
                    RTS
    
    left:           LDA cursorCords+1   ;check if we cannot move to left anymore
                    CPI 0xc1
                    BEQ underflowL
                    DEB cursorCords+1   ;if we can move towards left, move to the left
                    RTS
        
        underflowL: LDA cursorCords     ;check if we can move up
                    CPI 0x05
                    BNE moveU           ;if we cannot move up, dont do anything
                    RTS
            
            moveU:  LDI 0xe6            ;if we can move up, go one step up and to the right most character
                    STA cursorCords+1
                    DEB cursorCords
                    RTS

snake:              LDI 0x01
                    STA snakeDir        ;set initial snakeDir to left
                    STA tempSnakeDir    ;set tempSnakeDir to left
                    LDI 0x0a            ;set initial snakeLength to 10
                    STA snakeLength
                    CLB score

                    LDI 0x0f
                    STA foodCords
                    LDI 0xd7
                    STA foodCords+1     ;initialize the foodCords
                    
                    CLB var0            ;code for the snake game
                    JPS fillScreen      ;this will clear the screen
                    
                    LDI 0x01
                    STA var3
                    JPS drawBorder      ;draws the snake border
                    JPS snakeInit       ;initialize the snake in memory and screen

                    LDI 0x25
                    STR foodCords       ;print the food in the foodCords

                    


    snkTextInit:    LDI 0x11            ;prints some text
                    STA var0
                    LDI 0x02
                    STA var1
                    LDI <snaketop       ;prints snake!
                    STA add0
                    LDI >snaketop
                    STA add0+1
                    JPS printText

                    LDI 0x09
                    STA var0
                    LDI 0x07
                    STA var1
                    LDI <snakemid2      ;prints press any key to play
                    STA add0
                    LDI >snakemid2
                    STA add0+1
                    JPS printText

                    LDI 0x07
                    STA var0
                    LDI 0x09
                    STA var1
                    LDI <pressExitSnk   ;prints press esc to exit
                    STA add0
                    LDI >pressExitSnk
                    STA add0+1
                    JPS printText

    keyboardWait:   LDI 0xff
                    STA var0
                    JPS delay               ;wait for 255ms so person can release the key
                    JPS bufferFlush         ;remove garbage data which maybe from main screen press
                    JPS checkKBAnyKey       ;continue only after pressing a key
                    LDA var0
                    CPI 0x00
                    BEQ START               ;if esc is pressed, exit           

    snkGameInit:    LDI 0x01
                    STA var0
                    LDI 0x02
                    STA var1
                    LDI <eraser             ;erase snake!
                    STA add0
                    LDI >eraser
                    STA add0+1
                    JPS printText

                    LDI 0x01
                    STA var0
                    LDI 0x07
                    STA var1
                    LDI <eraser             ;erase press any key to play
                    STA add0
                    LDI >eraser
                    STA add0+1
                    JPS printText

                    LDI 0x01
                    STA var0
                    LDI 0x09
                    STA var1
                    LDI <eraser             ;erase press esc key to exit
                    STA add0
                    LDI >eraser
                    STA add0+1
                    JPS printText

                    LDI 0x10
                    STA var0
                    LDI 0x02
                    STA var1
                    LDI <scoreDisp          ;print the initial score text
                    STA add0
                    LDI >scoreDisp
                    STA add0+1
                    JPS printText

    snkGameLoop:    INB snakeTime           ;a counter for the elapsed time, may overflow but dont care
                    JPS updateSnkDir        ;if any key has been pressed update the direction
                    LDA tempSnakeDir
                    STA snakeDir            ;set the main snakeDir to tempSnakeDir
                    JPS moveSnake           ;move the snake 1 step forward, in memory

                    JPS checkWallCollision  ;check if we have collided
                    LDA var0
                    CPI 0x01
                    BEQ gameOverInter       ;Intermediate step before jumping to gameOver subroutine
                    
                    JPS checkFoodCollision  ;check and create newFood if necessary

        noFood:     LDI 0x00
                    STA var0                ;tells IfCordInSnakeBody to not check the head, otherwise omegalul
                    LDA 0x8100
                    STA add0
                    LDA 0x8101
                    STA add0+1              ;gets the cordinates of the head and puts them in add0
                    JPS IfCordInSnakeBody   ;checks if they are inside the snake
                    LDA var1
                    CPI 0x01
                    BEQ gameOverInter       ;if they are, ends the game
                    
                    JPS changeSnake         ;increment the snake on the screen
                    LDI 0x7f
                    STA var0
                    JPS delay               ;create a 127ms delay
                    JPA snkGameLoop         ;loop over

    gameOverInter:  JPS gameOver
                    LDA var0
                    CPI 0x00
                    BEQ START
                    JPA snake

;---------------------------------------------------------------------------------------------------------------------------------




;---------------------------------------------------SNAKE! Specific Functions-----------------------------------------------------

gameOver:           CLB var0            ;presents the gameOver screen. if exit to menu,var1 = 0x00. if restart game, var1 = 0xff
                    JPS fillScreen      ;clear the screen

    gameOvertext:   LDI 0x0f            ;prints text on the screen
                    STA var0
                    LDI 0x0f
                    STA var1
                    LDI <gameOverMsg    ;prints gameOver!
                    STA add0
                    LDI >gameOverMsg
                    STA add0+1
                    JPS printText

                    LDI 0x0b
                    STA var0
                    LDI 0x10
                    STA var1
                    LDI <finScore       ;prints the score message
                    STA add0
                    LDI >finScore
                    STA add0+1
                    JPS printText

                    LDI 0x06
                    STA var0
                    LDI 0x18
                    STA var1
                    LDI <continue       ;prints press anykey to continue
                    STA add0
                    LDI >continue
                    STA add0+1
                    JPS printText

                    LDI 0x07
                    STA var0
                    LDI 0x1a
                    STA var1
                    LDI <pressExitSnk   ;prints press esc to exit
                    STA add0
                    LDI >pressExitSnk
                    STA add0+1
                    JPS printText

                    CLB var7
                    INB var7
                    JPS displayScore

    checkUserState: LDI 0xff            
                    STA var0
                    JPS delay           ;1 second delay so that player has enough time to release keys
                    JPS delay
                    JPS bufferFlush     ;remove garbage from buffer
                    JPS checkKBAnyKey   ;return variable will be checked in the outside function
                    RTS
                    
checkWallCollision: LDA 0x8100          ;if snake has collided with a wall, var0 = 0x01. else, var0 = 0x00
                    CPI 0x04            ;compare y_cord with upper wall 
                    BEQ wallCollided
                    CPI 0x1d            ;compare y_cord with lower wall
                    BEQ wallCollided
                    LDA 0x8101
                    CPI 0xc0            ;compare x_cord with left wall
                    BEQ wallCollided
                    CPI 0xe7            ;compare x_cord with right wall
                    BEQ wallCollided
                    CLB var0            ;set var0 = 0 
                    RTS

    wallCollided:   LDI 0x01
                    STA var0            ;set var0 = 1
                    RTS

checkFoodCollision: LDA foodCords       ;checks if snakes head has collided with food and creates new food accordingly
                    CPA 0x8100          ;compare the y_cord
                    BNE checkExitFood   ;exit if not the same
                    LDA foodCords+1     
                    CPA 0x8101          ;compare the x_cord
                    BNE checkExitFood   ;exit if not the same
                    CLB var0
                    JPS newFood         ;find newFood
                    INB score
                    CLB var7            ;display the incremented score
                    JPS displayScore
                    
    checkExitFood:  RTS

IfCordInSnakeBody:  LDA var0            ;if add0 is in snake, var1 = 1. if var0 == 0 ignores the head, else checks that too
                    CPI 0x00
                    BEQ noHeadCheck
                    BNE yesHeadCheck

    noHeadCheck:    LDI 0x01
                    STA var1            ;var1 is the counter, start it from 0x01 since we want to do 1 less iteration
                    LDI 0x02
                    STA add1
                    LDI 0x81
                    STA add1+1          ;set add1 to 0x8002, since we want to ignore the first 2-bytes
                    JPA loopI

    yesHeadCheck:   LDI 0x00
                    STA var1            ;var1 is the counter, start it from 0x00 since head is also included
                    LDI 0x00
                    STA add1
                    LDI 0x81
                    STA add1+1          ;set add1 to 0x8000, since we also want to check the head
                    JPA loopI

    loopI:          LDA var1
                    CPA snakeLength     ;do [snakeLength] number of iterations, could be 1 less if head is neglected
                    BEQ loopI_exit

                    LDR add1
                    CPA add0            ;check if y_cord is the same
                    BNE yNotSame
                    INB add1
                    LDR add1
                    CPA add0+1          ;check if x_cord is the same
                    BEQ InBody
                    BNE xNotSame

        yNotSame:   INB add1            ;setup add1 for the next comparision
        xNotSame:   INB add1
                    INB var1
                    JPA loopI
    
    loopI_exit:     CLB var1
                    RTS
    
    InBody:         LDI 0x01            ;since we have found an element to be inside the snake, var1 = 0x01
                    STA var1
                    RTS

newFood:            JPS randomNumber    ;creates the new food cordinates
                    LDI 0x25            ;dividend is already in var0, set divisor to 40
                    STA var1
                    JPS division        ;get the random number between [0,39] 
                    LDA var3            ;remainder will be our final x_cord
                    ADI 0xc1            ;GET x_cord TO VRAM range
                    STA add0+1

                    JPS randomNumber
                    LDI 0x17            ;dividend is already in var0, set divisior to 25
                    STA var1
                    JPS division        ;get the random number between [0,24]
                    LDA var3
                    ADI 0x05            ;adjust the y_cord, as the top 5 rows are occupied by score card
                    STA add0

                    LDI 0x01
                    STA var0
                    JPS IfCordInSnakeBody
                    LDA var1
                    CPI 0x00
                    BEQ foodGood        ;if food is not inside the snake, foodCords are good

    desperateFood:  LDI 0x06            ;emergency food cordinates. used if above generates foodCordswhich are inside the snake
                    STA add0            ;there is no chance the snake would be present at all these cordinates at once
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

    foodGood:       LDA add0
                    STA foodCords
                    LDA add0+1
                    STA foodCords+1     ;store the final cordinates into foodCords
                    
                    INB snakeLength     ;since we have eaten something
                    
                    LDI 0x25
                    STR foodCords       ;print the new food
                    RTS

snakeInit:          LDI 0x0f            ;initializes the snake in memory and screen
                    STA 0x8100          ;stores initial y_cord of 10 elements of snake in memory
                    STA 0x8102
                    STA 0x8104
                    STA 0x8106
                    STA 0x8108
                    STA 0x810a
                    STA 0x810c
                    STA 0x810e
                    STA 0x8110
                    STA 0x8112

                    LDI 0xd0            ;stores initial x_cord of 10 elements of snake in memory
                    STA 0x8101
                    DEC
                    STA 0x8103
                    DEC
                    STA 0x8105
                    DEC
                    STA 0x8107
                    DEC
                    STA 0x8109
                    DEC
                    STA 0x810b
                    DEC
                    STA 0x810d
                    DEC
                    STA 0x810f
                    DEC                  
                    STA 0x8111
                    DEC                  
                    STA 0x8113

                    LDI 0x58            ;draws the 10 snake elements onto the screen
                    STR 0x8100
                    LDI 0x4f
                    STR 0x8102
                    STR 0x8104
                    STR 0x8106
                    STR 0x8108
                    STR 0x810a
                    STR 0x810c
                    STR 0x810e
                    STR 0x8110
                    STR 0x8112
                    RTS

updateSnkDir:       KSO                 ;checks the keyboard and updates the direction of snake
                    AND 0x07            ;top 5-bits contain garbage
                    CPI 0x00
                    BEQ updateDirExit
                    KBO

                    CPI 0xf0
                    BEQ f0Press
                    CPI 0x75
                    BEQ upPress
                    CPI 0x74
                    BEQ rightPress
                    CPI 0x72
                    BEQ downPress
                    CPI 0x6b
                    BEQ leftPress

                    CLB f0Flag          ;this byte is clearly not 0xf0
                    JPA updateSnkDir
    
    f0Press:        INB f0Flag
                    JPA updateSnkDir

    upPress:        LDA f0Flag
                    CPI 0x01
                    BEQ keyPressExit    ;if previous byte was 0xf0, dont change anything
                    LDA snakeDir
                    CPI 0x02
                    BEQ keyPressExit    ;if snake is travelling downwards, dont change anything
                    CLB tempSnakeDir
                    JPA keyPressExit
    
    rightPress:     LDA f0Flag
                    CPI 0x01
                    BEQ keyPressExit    ;if previous byte was 0xf0, dont change anything
                    LDA snakeDir
                    CPI 0x03
                    BEQ keyPressExit    ;if snake is travelling leftwards, dont change anything
                    LDI 0x01
                    STA tempSnakeDir
                    JPA keyPressExit
    
    downPress:      LDA f0Flag
                    CPI 0x01
                    BEQ keyPressExit    ;if previous byte was 0xf0, dont change anything
                    LDA snakeDir
                    CPI 0x00
                    BEQ keyPressExit    ;if snake is travelling upwards, dont change anything
                    LDI 0x02
                    STA tempSnakeDir
                    JPA keyPressExit
    
    leftPress:      LDA f0Flag
                    CPI 0x01
                    BEQ keyPressExit    ;if previous byte was 0xf0, dont change anything
                    LDA snakeDir
                    CPI 0x01
                    BEQ keyPressExit    ;if snake is travelling rightwards, dont change anything
                    LDI 0x03
                    STA tempSnakeDir
                    JPA keyPressExit

    keyPressExit:   CLB f0Flag          ;clear the f0Flag as the current byte is not 0xf0
                    JPA updateSnkDir

    updateDirExit:  RTS

moveSnake:          LDI 0xff            ;moves the snake in memory
                    STA add0            ;initializes starting values of add0 and add1
                    LDI 0xfd
                    STA add1
                    LDI 0x81
                    STA add0+1
                    STA add1+1
                    
                    CLB var0            ;var0 is the counter
    loopF:          LDA var0
                    CPI 0xfe            ;loop 254 times, to copy 254 times
                    BEQ loopF_exit

                    LDR add1            ;load an element of the snake
                    STR add0            ;store the element of the snake

                    DEB add0            ;change the addresses
                    DEB add1

                    INB var0            ;increment our coutner
                    JPA loopF
    loopF_exit:     LDA snakeDir        ;find the new head position, based on the current snakeDir
                    CPI 0x00 
                    BEQ moveUp
                    CPI 0x01
                    BEQ moveRight
                    CPI 0x02
                    BEQ moveDown
                    CPI 0x03
                    BEQ moveLeft

        moveUp:     DEB 0x8100          ;if snakeDir is up decrement y_cord of previous head position
                    RTS
        moveRight:  INB 0x8101          ;if snakeDir is right increment x_cord of previous head position
                    RTS
        moveDown:   INB 0x8100          ;if snakeDir is down increment y_cord of previous head position
                    RTS
        moveLeft:   DEB 0x8101          ;if snakeDir is left decrement x_cord of previous head position
                    RTS
    
changeSnake:        LDI 0x4f            ;only changes the necessary characters to increment the snake
                    STR 0x8102          ;changes the previous head to a body element, 0x4f is "O"
                    CLE
                    ADA snakeLength
                    ADA snakeLength     ;adding twice since 1 element takes up 2 bytes 
                    STA add0
                    LDI 0x81
                    STA add0+1          
                    LDR add0            ;get the y_cord of the last element of the snake
                    STA add1
                    INB add0
                    LDR add0            ;get the x_cord of the last element of the snake
                    STA add1+1          ;add1 now contains cordinates of last body element
                    CLE
                    STR add1            ;erase the last element (0x00 is equivalent of space)
                    
                    LDI 0x58
                    STR 0x8100          ;draws the new the head element, 0x58 is "X"
                    RTS

displayScore:       LDA score           ;if var7 == 0x00, displays score in the game positon. else, in the gameOver position
                    STA var0            
                    LDI 0x0a            ;divide score by 10
                    STA var1
                    JPS division

                    LDA var3            ;remainder will be 1s place
                    STA var4            ;var4 will contain the 1s place digit

                    LDA var2
                    STA var0            ;10 is already in var1
                    JPS division        ;divide the quotient of previous division by 10
                    
                    LDA var3            ;remainder will be our 10s place
                    STA var5            ;var5 will contain the 10s place digit
                    
                    LDA var2            ;quotient should be 100s place
                    STA var6            ;var6 will contain the 100s place digit

                    LDA var7
                    CPI 0x00
                    BNE displayOver

    displayGame:    LDA var4            ;will display score while the game is being played
                    ADI 0x30            ;adding 48 brings them to the ascii character range
                    STA 0xd802
                    LDA var5
                    ADI 0x30
                    STA 0xd702
                    LDA var6
                    ADI 0x30
                    STA 0xd602
                    RTS
    
    displayOver:    LDA var4            ;will display score on the gameOver screen
                    ADI 0x30            ;adding 48 brings them to the ascii character range
                    STA 0xdc10
                    LDA var5
                    ADI 0x30
                    STA 0xdb10
                    LDA var6
                    ADI 0x30
                    STA 0xda10
                    RTS

;---------------------------------------------------------------------------------------------------------------------------------




;--------------------------------------------------------General Functions--------------------------------------------------------

printText:          LDA var0            ;var0 contains x_cord, var1 contains y_cord and add0 contains address of message
                    ADI 0xc0            ;done to take it to VRAM address range
                    STA add1+1          ;store the x_cord   
                    LDA var1
                    STA add1            ;address of where to draw is now in add1
    loopD:          LDR add0
                    CPI 0x0a            ;if character == 0x0a, stop printing 
                    BEQ loopD_exit
                    
                    STR add1            ;store the character onto the screen

                    INW add0
                    INB add1+1          ;increment x_cord of character 
                    JPA loopD
    loopD_exit:     RTS

drawBorder:         LDA var3            ;if var3 == 0x00 will draw normal_border else will draw snake_border
                    CPI 0x00
                    BNE snakeBorder
    
    normalBorder:   LDI 0x0a            ;draws multiple lines
                    STA var0
                    CLB var1
                    JPS drawVLine

                    LDI 0x27
                    STA var1
                    JPS drawVLine
                    
                    LDI 0x0b
                    STA var0
                    CLB var1
                    JPS drawHLine
                    
                    LDI 0x4
                    STA var1
                    JPS drawHLine
                    
                    LDI 0x1d
                    STA var1
                    JPS drawHLine

                    
                    LDI 0x0c            ;corrects some characters, where 2 or more lines join
                    STA 0xc000
                    LDI 0x0d
                    STA 0xe700

                    LDI 0x10
                    STA 0xc004
                    LDI 0x11
                    STA 0xe704

                    LDI 0x0e
                    STA 0xc01d
                    LDI 0x0f
                    STA 0xe71d
                    
                    RTS

    snakeBorder:    LDI 0x23            ;draws multiple lines
                    STA var0
                    CLB var1
                    JPS drawVLine
                    
                    LDI 0x27
                    STA var1
                    JPS drawVLine
                    
                    CLB var1
                    JPS drawHLine
                    
                    LDI 0x4
                    STA var1
                    JPS drawHLine
                    
                    LDI 0x1d
                    STA var1
                    JPS drawHLine
                    
                    RTS

fillScreen:         CLB var3            ;character to fill screen with is in var0 
    loopB:          LDA var3            ;var3 is our counter variable
                    CPI 0x1e            ;looping over 30 times, to draw 30 horizontal lines
                    BEQ loopB_exit

                    ;code which loops over
                    LDA var3
                    STA var1            ;drawVLine requires var1 to be x_cord of line and var0 is already the character
                    JPS drawHLine       ;draw repeated vertical lines           

                    INB var3            ;increment our counter
                    JPA loopB
    loopB_exit:     RTS

drawVLine:          LDA var1            ;character is in var0 and x_cord is in var1
                    ADI 0xc0            ;doing this to bring it into the VRAM address range
                    STA add0+1          ;storing the x_cord in the top 8-bits of add0
                    CLB var2            ;var2 is our counter variable
    loopA:          LDA var2
                    CPI 0x1e            ;loop over 40 times ad display is 40x30
                    BEQ loopA_exit
                    
                    ;code which loops over
                    STA add0            ;we already have var2 in our accumalator
                    LDA var0            
                    STR add0            ;store the character at the desired location

                    INB var2            ;increment our counter
                    JPA loopA
    loopA_exit:     RTS

drawHLine:          LDA var1            ;character is in var0 and y_cord is in var1
                    STA add0            ;store the y_cord in bottom 8-bits of add0
                    CLB var2            ;var2 is our counter variable

    loopC:          LDA var2
                    CPI 0x28            ;loop over 40 times as display is 40x30
                    BEQ loopC_exit
                    
                    ;code which loops over
                    ADI 0xc0            ;we already have var2 in our accumalator
                    STA add0+1          ;store the x_cord
                    LDA var0
                    STR add0            ;store the character at the desired location

                    INB var2            ;increment our coutner
                    JPA loopC
    loopC_exit:     RTS

delay:              CLB var2            ;provides a [var0] milliseconds of delay
    loopH:          CLB var1            
                    LDA var2            ;var2 is counter for loopH
                    CPA var0            ;want to repeat [var0] amount of times
                    BEQ loopH_exit

    loopG:          LDA var1                ;7 clock
                    CPI 0x14                ;5 clock, we will loop over 20 times
                    BEQ loopG_exit          ;6 clock
                    
                    NOP                     ;16 clock

                    INB var1                ;10 clock, var1 is counter for loopG
                    JPA loopG               ;6  clock
    
    loopG_exit:     INB var2                ;loopG will take 50*20 clocks, and be completed in 10^-3 seconds (1MHz clock)
                    JPA loopH
    loopH_exit:     RTS

division:           LDA var0            ;var0[0,127] is dividend and var1[0,127] is divisor. puts quotient in var2 and remainder in var3
                    CLB var2            ;var2 will be the quotient
    loopK:          CPA var1            
                    BMI loopK_exit      ;branch if no more subtraction is possible

                    SBA var1            
                    INB var2            ;increment our quotient, as an iteration has completed
                    
                    JPA loopK
    loopK_exit:     STA var3            ;remainder would be in accumalator, store it in var3
                    RTS

bufferFlush:        KBO                 ;flushes the keyboard buffer
                    KSO              
                    AND 0x07            ;only concerned about bottom 3 bits, top 5 contain garbage.
                    CPI 0x00            
                    BNE bufferFlush   
                    RTS     

randomNumber:       INB rngSeed         ;after calling, var0 will contain a random number. range will be [0,127]
                    LDA rngSeed         
                    ADA snakeTime       ;adding the snakeTime provides more randomness, just enough to make it seem random
                    STA rngSeed         
                    CLB var0            ;var0 is a counter here
                    LDI 0x82            ;specifies address to be inside a page of RAM
                    STA add2+1
    
    loopJ:          LDA var0
                    CPI 0x02            ;have to complete 2 iterations
                    BEQ loopJ_exit

                    LDA rngSeed
                    STA add2            ;create a random memory address pointing inside the RAM
                    LDR add2            ;loads the byte from the random address
                    STA rngSeed         ;stores the random byte, which will be later used to create a random address

                    INB var0
                    INB add2+1          ;increment the page inside RAM from which the byte will be sampled
                    JPA loopJ
    
    loopJ_exit:     LDA rngSeed         ;get the final random byte
                    AND 0x7f            ;making sure it doesn't exceed 127, which would be negative in 2's complement
                    STA var0
                    RTS

checkKBMenu:        KSO                 ;we only check for 1, 2 and s. if 1, var0 = 0x00. if 2, var0 = 0x01. if s, var0 = 0x03
                    AND 0x07            ;top 5-bits contain garbage
                    CPI 0x00
                    BEQ checkKBMenu     ;loop over if no new bits have arrived
                    KBO
                    CLB var0
                    CPI 0x16            ;1 check
                    BEQ checkMenuexit
                    INB var0
                    CPI 0x1e            ;2 check
                    BEQ checkMenuexit
                    INB var0
                    CPI 0x1b            ;s check
                    BEQ checkMenuexit
                    JPA checkKBMenu
    checkMenuexit:  RTS

checkKBAnyKey:      KSO                 ;we check for esc or any key. if esc, var0 = 0x00. else var0 = 0x01
                    AND 0x07            ;top 5-bits contain garbage
                    CPI 0x00
                    BEQ checkKBAnyKey   ;loop over if no new bits have arrived
                    KBO
                    CPI 0xf0            ;ignore 0xf0 and 0xe0
                    BEQ checkKBAnyKey
                    CPI 0xe0
                    BEQ checkKBAnyKey
                    
                    CLB var0            ;clearing our return variable
                    CPI 0x76            ;esc check
                    BEQ checkOverexit
                    INB var0
                    JPA checkOverexit

    checkOverexit:  RTS       

;---------------------------------------------------------------------------------------------------------------------------------



;--------------------------------------------------------Strings------------------------------------------------------------------

Strings:
    osName:             'amog-OS',10                            ;10 marks the end of the string
    option1:            'Press 1 for SNAKE!',10          
    option2:            'And   2 for Text-editor!',10
    bottom:             'Do visit: chvsnaveen12.github.io',10
    special:            'Made with a lot of pain',10
    snaketop:           'SNAKE!',10
    snakemid1:          'To WIN, reach 100 score.',10
    snakemid2:          'Press any key to play.',10
    eraser:             '                                ',10
    scoreDisp:          'Score:000',10
    gameOverMsg:        'Game over!',10
    finScore:           'Your score was:000',10
    continue:           'Press any key to play again.',10
    pressExitSnk:       'And esc key to exit SNAKE!',10
    pressExitTxt:       'And esc key to exit Text-editor!',10
    textEditorText:     'Text-editor!',10
    noReason:           'bytes: 3366'

;---------------------------------------------------------------------------------------------------------------------------------



;--------------------------------------------------------Comments-----------------------------------------------------------------
;To assemble the file:  python3 assembler\asm.py code\OS.s
;To flash the FLASH:    prom.exe -wassembler\output.bin

;---------------------------------------------------------------------------------------------------------------------------------