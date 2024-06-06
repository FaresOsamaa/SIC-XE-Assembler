from operator import *

file = open('in.txt', 'r')

readl = file.readlines()

fileNew = open("intermediate.txt", "w")

for n in readl:

    fileNew.write(n[3:32]+'\n')
fileNew.close()


sym = {}
loc = []
opcodeTable = {

    "ADD": "18",
    "AND": "40",
    "COMP": "28",
    "DIV": "24",
    "J": "3C",
    "JEQ": "30",
    "JGT": "34",
    "JLT": "38",
    "JSUB": "48",
    "LDA": "00",
    "LDCH": "50",
    "LDL": "08",
    "LDX": "04",
    "MUL": "20",
    "OR": "44",
    "RD": "D8",
    "RSUB": "4C",
    "STA": "0C",
    "STCH": "54",
    "STL": "14",
    "STSW": "E8",
    "STX": "10",
    "SUB": "1C",
    "TD": "E0",
    "TIX": "2C",
    "WD": "DC",
}


opcodeTableF1 = {

    "FIX": "C4",
    "FLOAT": "C0",
    "HIO": "F4",
    "NORM": "C8",
    "SIO": "F0",
    "TIO": "F8"
}


fileIntermediate = open("intermediate.txt", 'r')
fileIn = fileIntermediate.readline()


out = open("out_pass1.txt", "w")
symtab = open("symbTable.txt", "w")


out2 = open("out_pass2.txt", 'w')
hte = open("HTE.txt", 'w')


out.write("-")
out.write("".join(fileIn))
newl = fileIn.strip().split()
symtab.write("Opcode Address\n-----------\n")


out2.write("-")
out2.write("".join(fileIn))
temp = fileIn.strip().split()
name = temp[0]
start_add = "00"+temp[2]


locationCounter = newl[2]
start = locationCounter

for i in fileIntermediate.readlines():
    n = i.strip().split()

    if not i.isspace():
        if n[0] != '.':

            if len(n[0]) > 6:

                exit()

            out.write(hex(int(locationCounter, 16)))

            out.write("".join(i))
            loc.append(locationCounter)

            out2.write(hex(int(locationCounter, 16)))

            out2.write("".join(i))

            if n[0] != "-":
                symtab.write(n[0] + " " + hex(int(locationCounter, 16)) + "\n")

                sym[n[0]] = str(hex(int(locationCounter, 16)))

            if n[1] in opcodeTable.keys() or n[1] == "WORD":
                locationCounter = str(hex(int(locationCounter, 16) + (3)))

            elif n[1] in opcodeTableF1.keys():
                locationCounter = str(hex(int(locationCounter, 16) + (1)))

            elif n[1] == "RESW":
                temp = int(n[2], 16)
                locationCounter = str(
                    hex(int(locationCounter, 16) + (temp) * 3))

            elif n[1] == "RESB":
                locationCounter = str(
                    hex(int(locationCounter, 16) + int(n[2])))
            elif n[1] == "BYTE":
                if n[2][0] == "X":
                    locationCounter = str(
                        hex(int(locationCounter, 16) + int((len(n[2]) - 3) / 2)))
                elif n[2][0] == "C":
                    locationCounter = str(
                        hex(int(locationCounter, 16) + (len(n[2]) - 3)))

            else:
                print("ERROR IN INSTRUCTION INPUT")

fileIntermediate.close()
out.close()
symtab.close()
out2.close()

fileIntermediate2 = open("intermediate.txt", 'r')
fileIn2 = fileIntermediate2.readline()

objcode = open("objcode.txt", "w")

no_list = ["RESW", "RESB"]

objectCodeList = []

for i in fileIntermediate2.readlines():
    n = i.strip().split()
    if not i.isspace():
        if n[0] != '.' and n[1] != "START" and n[1] != "END":

            if n[1] in opcodeTableF1.keys():
                objcode.write(opcodeTableF1.get(n[1])+"\n")
                objectCodeList.append(opcodeTableF1.get(n[1]))

            elif (n[1] in opcodeTable.keys() and "#" in n[2]) or n[1] == "WORD":
                if "#" in n[2] and n[1] != "WORD":
                    opIM = bin(int(n[2][1:]))[2:].zfill(
                        15)
                    opC = bin(int(opcodeTable.get(n[1]))+1)[2:].zfill(8)

                    if ",X" in n[2]:
                        opC = opC+"1"

                    else:
                        opC = opC + "0"
                    final_objCode = str(opC)+str(opIM)
                    final_objCode = hex(int(final_objCode, 2))[2:]

                    leng_final_obCode = len(final_objCode)

                    while leng_final_obCode < 6:
                        final_objCode = "0"+final_objCode
                        leng_final_obCode = leng_final_obCode+1

                    objcode.write(final_objCode+"\n")
                    objectCodeList.append(final_objCode)

                if n[1] == "WORD":
                    opW = hex(int(n[2], 10))[2:]

                    leng_opW = len(opW)

                    while leng_opW < 6:
                        opW = "0" + opW
                        leng_opW = leng_opW + 1

                    objcode.write(opW + "\n")
                    objectCodeList.append(opW)

            elif "#" in n[2] and n[1] != "WORD":

                exit()

            elif n[1] == 'BYTE':
                if "X" in n[2]:
                    opX = hex(int(n[2][2:len(n[2]) - 1], 16))[2:]

                    objcode.write(opX + "\n")
                    objectCodeList.append(opX)
                elif "C" in n[2]:
                    opCC = str(''.join(hex(ord(n[2][2]))))[2:] + str(''.join(hex(ord(n[2][3]))))[2:] + str(
                        ''.join(hex(ord(n[2][4]))))[2:]

                    objcode.write(opCC + "\n")
                    objectCodeList.append(opCC)
            elif n[1] == "RSUB":
                opR = opcodeTable.get(n[1])
                opR = opR+"0000"

                objcode.write(opR + "\n")
                objectCodeList.append(opR)

                pass
            elif n[1] in opcodeTable.keys():
                inst_F3 = opcodeTable.get(n[1])
                if n[2] in sym or ",X" in n[2]:
                    if ",X" in n[2]:
                        Xvar = n[2]
                        Xvar = Xvar[0:len(n[2]) - 2]

                        inst_var = sym.get(Xvar)[2:]
                    else:
                        inst_var = sym.get(n[2])[2:]

                final_objCode = inst_F3+inst_var
                final_objCode = hex(int(final_objCode, 16))

                if ",X" in n[2]:
                    x = "8000"
                    final_objCode = hex(int(final_objCode, 16) + int(x, 16))

                final_objCode = final_objCode[2:]

                leng_final_obCode = len(final_objCode)

                while leng_final_obCode < 6:
                    final_objCode = "0" + final_objCode
                    leng_final_obCode = leng_final_obCode + 1

                objcode.write(final_objCode + "\n")
                objectCodeList.append(final_objCode)

            elif n[1] in no_list:

                objcode.write("-"+"\n")
                objectCodeList.append("-")

fileIntermediate2.close()
objcode.close()

objCodeFile = open("objcode.txt", "r")
out1 = open("out_pass1.txt", "r+")
out2 = open("out_pass2.txt", 'w')
out1_line = out1.readline()
out2.write(out1_line)
j = 0

for i in out1.readlines():
    n = i.strip()

    out2.write(n+"\t"+objectCodeList[j]+"\n")
    j = j+1

out2.close()
objCodeFile.close()

out3 = open("out_pass2.txt", "r")
hte = open("hte.txt", 'w')

leng_name = len(name)

while leng_name < 6:
    name = name+"X"
    leng_name = leng_name+1


last_add = loc[len(loc)-1]

length = hex(int(last_add, 16)-int(start_add, 16))

hte.write("H, "+name+", "+start_add+", 00"+length[2:]+"\n")

line_1 = out3.readline()

tstart = 0
tlimit = 0
n = 0
flag = 1
flagos = 0
flagEndT = 0
flagnos = 0
str1 = ""
str2 = ""
flagTen = 0
start = start_add

for i in out3.readlines():
    x = i.split()
    n += 1
    str2 = ''
    flagTen = 0
    if flagEndT == 1:
        tstart = int(x[0], 16)
        flagEndT = 0
    if start == "00"+x[0][2:]:
        hte.write("T")
        tstart = int(start, 16)
        hm = str(hex(tstart)).replace('0x', '')
        if len(hm) < 6:
            for i in range(6 - len(hm)):
                hm = "0" + hm
        hte.write(", " + hm)

    if x[2] == "RESB" or x[2] == "RESW":
        tstart = int(x[0], 16)
        mod = str(hex(tlimit + 3))
        if len(mod) < 4:
            for i in range(4 - len(mod)):
                mod = "0" + mod
        str2 = ", " + mod
        str2 = str2.replace('0x', '')
        str2 = str2 + str1
        if len(str2) >= 6:
            hte.write(str2)

        tlimit = 0
        flagos = 0
        flagEndT = 1
        str2 = ''
        str1 = ''
        continue
    if tlimit >= 27:
        tstart = int(x[0], 16)
        mod = str(hex(tlimit + 3))
        if len(mod) < 4:
            for i in range(4 - len(mod)):
                mod = "0" + mod
        str2 = ", " + mod
        str2 = str2.replace('0x', '')
        str2 = str2 + str1
        hte.write(str2)
        str2 = ''
        str1 = ''
        tlimit = 0
        flagos = 0
        flagTen = 1

    if tlimit < 27:
        if tlimit == 0 and n > 2 and flagos == 0:
            hte.write("\nT")
            hm = str(hex(tstart)).replace('0x', '')
            if len(hm) < 6:
                for i in range(6 - len(hm)):
                    hm = "0" + hm
            hte.write(", " + hm)
            flagos = 1

        mod = str(hex(tlimit + 3))
        if len(mod) < 4:
            for i in range(4 - len(mod)):
                mod = "0" + mod
        str2 = ", " + mod
        str2 = str2.replace('0x', '')

        str1 += str(", " + str(x[4]))
        tlimit = int(x[0], 16) - tstart
if flagTen != 1:
    hte.write(str2 + str1)

hte.write("\nE, "+start_add)

hte.close()
