load.txt tells TIS-100 what program to load. 
TIS-100 autosaves when you hit escape, so change load.txt and restart the program to make a different program.


Commands:
MOV <SRC> <DEST> - moves the value in <SRC> to <DEST>
ADD <SRC> - adds the value in <SRC> to ACC
SUB <SRC> - subtracts the value in <SRC> from ACC
NEG - multiplies ACC by -1
SAV - Copies ACC to BAK
SWP - Swaps ACC and BAK
<LABEL>; - provides a point to jump to
JMP <LABEL> - jump to that label
JEZ <LABEL> - jump if ACC is zero
JNZ <LABEL> - jump if ACC is not zero
JGZ <LABEL> - jump if ACC is greater than zero
JLZ <LABEL> - jump if ACC is less than zero
JRO <CONSTANT> - jump that many lines (not working)

Ports:
UP, DOWN, LEFT, RIGHT - Inter-node ports. Reading or writing to these will freeze the node until the other node cooperates.
				After the communication, the port resets to NULL.
ACC - main node memory. Unlike the directional ports, it maintains its value when MOVed from.
BAK - backup node memory. Cannot be interacted with except by SAV and SWP.
NIL - Using NIL as <DEST> does nothing (but can be useful in a MOV since MOV RIGHT NIL still reads RIGHT and frees it up), NIL as <SRC> = 0.
<CONSTANT> - Can be used as <SRC> with obvious results.