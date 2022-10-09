opCodes = { 'NOP':'0',  'LDI':'1',  'LDA':'2',  'LDR':'3',  'LDS':'4',  'STA':'5',  'STR':'6',  'STS':'7',
            'INC':'8',  'INB':'9',  'INW':'10', 'DEC':'11', 'DEB':'12', 'DEW':'13', 'ADI':'14', 'ADA':'15',
            'ADR':'16', 'ADB':'17', 'ADW':'18', 'SBI':'19', 'SBA':'20', 'SBR':'21', 'SBB':'22', 'SBW':'23',
            'CPI':'24', 'CPA':'25', 'CPR':'26', 'ACI':'27', 'ACA':'28', 'ACR':'29', 'ACB':'30', 'ACW':'31',
            'SCI':'32', 'SCA':'33', 'SCR':'34', 'SCB':'35', 'SCW':'36', 'JPA':'37', 'JPR':'38', 'JPS':'39',
            'CLE':'40', 'CLB':'41', 'CLW':'42', 'NEG':'43', 'NEB':'44', 'NEW':'45', 'AND':'46', 'ANB':'47',
            'ORA':'48', 'ORB':'49', 'KBO':'50', 'KBB':'51', 'KSO':'52', 'KSB':'53', 'SEZ':'54', 'CLZ':'55',
            'SEN':'56', 'CLN':'57', 'SEC':'58', 'CLC':'59', 'RTS':'60', 'LSL':'61', 'LLB':'62', 'ROL':'63',
            'RLB':'64', 'LSR':'65', 'LRB':'66', 'ROR':'67', 'RRB':'68', 'ASR':'69', 'ARB':'70', 'PHS':'71',
            'PLS':'72', 'BNE':'73', 'BEQ':'74', 'BCC':'75', 'BCS':'76', 'BPL':'77', 'BMI':'78'}

lines, lineinfo, lineadr, labels = [], [], [], {}
LINEINFO_NONE, LINEINFO_ORG, LINEINFO_BEGIN, LINEINFO_END	= 0x00000, 0x10000, 0x20000, 0x40000

import sys                                          # read in <sourcefile> 2nd command parameter line by line
if len(sys.argv) != 2: print('usage: asm.py <sourcefile>'); sys.exit(1)
f = open(sys.argv[1], 'r')
while True:                                         # read in the source line
    line = f.readline()
    if not line: break
    lines.append(line.strip())                      # store each line without leading/trailing whitespaces
f.close()

variables = {}



for i in range(len(lines)):                         # PASS 1: do PER LINE replacements
    while(lines[i].find('\'') != -1):               # replace '...' occurances with corresponding ASCII code(s)
        k = lines[i].find('\'')
        l = lines[i].find('\'', k+1)
        if k != -1 and l != -1:
            replaced = ''
            for c in lines[i][k+1:l]: replaced += str(ord(c)) + ' '
            lines[i] = lines[i][0:k] + replaced + lines[i][l+1:]
        else: break

    if '=' in lines[i]:
        variable_split = lines[i].split('=')
        for p in range(len(variable_split)):
            variable_split[p] = variable_split[p].replace(';', '').strip()
        variables[variable_split[0]] = variable_split[1]

    if (lines[i].find(';') != -1): lines[i] = lines[i][0:lines[i].find(';')]    # delete comments
    lines[i] = lines[i].replace(',', ' ')                                       # replace commas with spaces
    lineinfo.append(LINEINFO_NONE)                  # generate a separate lineinfo
    if lines[i].find('#begin') != -1: lineinfo[i] |= LINEINFO_BEGIN; lines[i] = lines[i].replace('#begin', '')
    if lines[i].find('#end') != -1: lineinfo[i] |= LINEINFO_END; lines[i] = lines[i].replace('#end', '')
    k = lines[i].find('#org')
    if (k != -1):        
        s = lines[i][k:].split()                    # split from #org onwards
        lineinfo[i] |= LINEINFO_ORG + int(s[1], 0)  # use element after #org as origin address
        lines[i] = lines[i][0:k].join(s[2:])        # join everything before and after the #org ... statement

    if lines[i].find(':') != -1:
        labels[lines[i][:lines[i].find(':')]] = i   # put label with it's line number into dictionary
        lines[i] = lines[i][lines[i].find(':')+1:]  # cut out the label

    lines[i] = lines[i].split()                     # now split line into list of bytes (omitting whitepaces)

    if '=' in lines[i]:
        continue
    
    for j in range(len(lines[i])-1, -1, -1):        # iterate from back to front while inserting stuff
        try:
            if lines[i][j] in opCodes:
                lines[i][j] = opCodes[lines[i][j]]     # try replacing mnemonic with opcode
            elif lines[i][j] in variables:
                lines[i][j] = variables[lines[i][j]]
            elif '+' in lines[i][j]:
                comp = lines[i][j].split('+')
                variable_value = int(variables[comp[0]], 16)
                lines[i][j] = hex(variable_value + int(comp[1]))

            if lines[i][j].find('0x') == 0 and len(lines[i][j]) > 4:    # replace '0xWORD' with 'LSB MSB'
                val = int(lines[i][j], 16)
                lines[i][j] = str(val & 0xff)
                lines[i].insert(j+1, str((val>>8) & 0xff))    
        except:
            print("catchblock") 
            pass

adr = 0                                             # PASS 2: default start address
for i in range(len(lines)):
    for j in range(len(lines[i])-1, -1, -1):        # iterate from back to front while inserting stuff
        e = lines[i][j]                               
        if e[0] == '<' or e[0] == '>' : continue    # only one byte is required for this label
        if e.find('+') != -1: e = e[0:e.find('+')]  # omit +/- expressions after a label
        if e.find('-') != -1: e = e[0:e.find('-')]
        try:
            labels[e]; lines[i].insert(j+1, '0x@@') # is this element a label? => add a placeholder for the MSB
        except: pass
    if lineinfo[i] & LINEINFO_ORG: adr = lineinfo[i] & 0xffff   # react to #org by resetting the address
    lineadr.append(adr);                            # save line start address
    adr += len(lines[i])	  					    # advance address by number of (byte) elements

for l in labels: labels[l] = lineadr[labels[l]]     # update label dictionary from 'line number' to 'address'

for i in range(len(lines)):                         # PASS 3: replace 'reference + placeholder' with 'MSB LSB'
    for j in range(len(lines[i])):
        e = lines[i][j]; pre = ''; off = 0        
        if e[0] == '<' or e[0] == '>': pre = e[0]; e = e[1:]
        if e.find('+') != -1: off += int(e[e.find('+')+1:], 0); e = e[0:e.find('+')]
        if e.find('-') != -1: off -= int(e[e.find('-')+1:], 0); e = e[0:e.find('-')]
        try:
            adr = labels[e] + off
            if pre == '<': lines[i][j] = str(adr & 0xff)
            elif pre == '>': lines[i][j] = str((adr>>8) & 0xff)
            else: lines[i][j] = str(adr & 0xff); lines[i][j+1] = str((adr>>8) & 0xff)
        except: pass
        try: int(lines[i][j], 0)                    # check if ALL elements are numeric
        except: print('ERROR in line ' + str(i+1) + ': Undefined expression \'' + lines[i][j] + '\''); exit(1)

# for i in range(len(lines)):							# print out the result
#    s = ('%04.4x' % lineadr[i]) + ": "
#    for e in lines[i]: s += ('%02.2x' % (int(e, 0) & 0xff)) + ' '
#    print(s)

output_str = str()

insert = ''; showout = True                       # print out the result
for i in range(len(lines)):
    if lineinfo[i] & LINEINFO_BEGIN: showout = True
    if lineinfo[i] & LINEINFO_END: showout = False
    if showout:
        if lineinfo[i] & LINEINFO_ORG:
            if insert: print(insert); insert = ''
            print('%04.4x' % (lineinfo[i] & 0xffff))
            # output_str += '%04.4x' % (lineinfo[i] & 0xffff)
        for e in lines[i]:
            insert += ('%02.2x' % (int(e, 0) & 0xff)) + ' '
            if len(insert) >= 16*3 - 1: 
                print(insert); 
                output_str += str(insert)
                insert = ''
if insert: 
    print(insert)
    output_str += str(insert)

bin_list = [bytes.fromhex(x) for x in output_str.split()]


f = open('assembler\output.bin', 'wb')
for item in bin_list:
    f.write(item)

