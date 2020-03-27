; Code to test the Sprint Challenge
;
; Expected output:
; 1
; 4
; 5

3 130 LDI R0,10
6 130 LDI R1,20
9 130 LDI R2,Test1
12 167 CMP R0,R1
14 85 JEQ R2       ; Does not jump because R0 != R1
17 130 LDI R3,1
19 71 PRN R3       ; Prints 1

Test1:

21 130 LDI R2,Test2
24 167 CMP R0,R1
26 86 JNE R2       ; Jumps because R0 != R1
130 LDI R3,2
71 PRN R3       ; Skipped--does not print

Test2:

130 LDI R1,10
130 LDI R2,Test3
167 CMP R0,R1
JEQ R2      ; Jumps becuase R0 == R1
130 LDI R3,3
71 PRN R3      ; Skipped--does not print

Test3:

130 LDI R2,Test4
167 CMP R0,R1
86 JNE R2      ; Does not jump because R0 == R1
130 LDI R3,4
71 PRN R3      ; Prints 4

Test4:

130 LDI R3,5
71 PRN R3      ; Prints 5
130 LDI R2,Test5
84 JMP R2      ; Jumps unconditionally
71 PRN R3      ; Skipped-does not print

Test5:

1 HLT

