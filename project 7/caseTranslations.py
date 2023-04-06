def pushCommand(command, segments, filename):
    if command[1] in segments:
        asm = f'''//push {command[1]} {command[2]}
@{command[2]}
D=A

@{segments[command[1]]}
A=D+M
D=M

'''

    elif command[1] == 'constant':
        asm = f'''//push {command[1]} {command[2]}
@{command[2]}
D=A

'''

    elif command[1] == 'static':
        asm = f'''//push {command[1]} {command[2]}
@{filename}.{command[2]}
D=M

'''

    elif command[1] == 'temp':
        asm = f'''//push {command[1]} {command[2]}
@{command[2]}
D=A

@5
A=D+A
D=M

'''

    else:
        if command[2]=='0':
            thisorthat = 'THIS'
        else:
            thisorthat = 'THAT'

        asm = f'''//push {command[1]} {command[2]}
@{thisorthat}
D=M

'''


    asm += '''@SP
A=M
M=D
@SP
M=M+1'''

    return asm

################################################################################################

def popCommand(command, segments, filename):
    if command[1] in segments:
        asm = f'''//pop {command[1]} {command[2]}
@{command[2]}
D=A

@{segments[command[1]]}
D=D+M

@addr
M=D

@SP
AM=M-1
D=M

@addr
A=M
M=D'''

    elif command[1] == 'static':
        asm = f'''//pop {command[1]} {command[2]}
@SP
AM=M-1
D=M

@{filename}.{command[2]}
M=D'''

    elif command[1] == 'temp':
        asm = f'''//pop {command[1]} {command[2]}
@{command[2]}
D=A

@5
D=D+A

@addr
M=D

@SP
AM=M-1
D=M

@addr
A=M
M=D'''

    else:
        if command[2] == '0':
            thisorthat = 'THIS'
        else:
            thisorthat = 'THAT'

        asm = f'''//pop {command[1]} {command[2]}
@SP
AM=M-1
D=M

@{thisorthat}
M=D'''

    return asm

################################################################################################

def arithmeticCommand(command, compNum, oneVal, compare, twoVal):

    asm = f'''//{command}
@SP
AM=M-1
D=M
A=A-1
'''

    if command in oneVal:
        asm = f'''//{command}
@SP
A=M-1
{oneVal[command]}'''


    elif command in compare:
        asm += f'''D=M-D

@TRUE.{compNum}
{compare[command]}
D=0

@FALSE.{compNum}
0;JMP

(TRUE.{compNum})
D=-1

(FALSE.{compNum})
@SP
A=M-1
M=D'''
        compNum = str(int(compNum) + 1)


    else:
        asm += f'''{twoVal[command]}'''

    return asm, compNum
