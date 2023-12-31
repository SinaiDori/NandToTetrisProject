// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(INFLOOP)
@8192
D=A
@i
M=D
@KBD
D=M
@LOOPBLACK
D;JNE

(LOOPWHITE)
@i
D=M
@INFLOOP
D;JEQ
@i
M=M-1
D=M
@SCREEN
A=D+A
M=0
@LOOPWHITE
0;JMP

(LOOPBLACK)
@i
D=M
@INFLOOP
D;JEQ
@i
M=M-1
D=M
@SCREEN
A=D+A
M=-1
@LOOPBLACK
0;JMP

@INFLOOP
0;JMP