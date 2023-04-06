import caseTranslations as t

oneVal = {'neg': 'M=-M', 'not': 'M=!M'}
compare = {'eq': 'D;JEQ', 'lt': 'D;JLT', 'gt': 'D;JGT'}
twoVals = {'add': 'M=D+M', 'sub': 'M=M-D', 'or': 'M=D|M', 'and': 'M=D&M'}
segments = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}

compNum = '1'

endCode = '''//ending loop
(END)
@END
0;JMP'''



def translate(command, filename, compCount):
    parsed = command.split()

    if parsed[0] == 'push':
        asm = t.pushCommand(parsed, segments, filename)
    elif parsed[0] == 'pop':
        asm = t.popCommand(parsed, segments, filename)
    else:
        asm, compCount = t.arithmeticCommand(parsed[0], compCount, oneVal, compare, twoVals)
    return asm, compCount



filename = 'StaticTest'
with open(filename + '.vm') as f:
    lines = f.readlines()

assemblyCode = ''''''
for line in lines:
    if line[0]=='/' or line=='\n':
        continue

    asmAndCount = translate(line, filename, compNum)
    assemblyCode += asmAndCount[0] + '\n\n'
    compNum = asmAndCount[1]

assemblyCode += endCode


with open(filename + '.asm', 'w') as file:
    file.write(assemblyCode)
