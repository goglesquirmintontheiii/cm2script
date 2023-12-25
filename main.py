import cm2py
import pyperclip
import json

f = input("Enter path of file to compile (output copies to clipboard): ")

sv = cm2py.Save()

blocks = {}
bctypes = {}
props = {}

buildings = {}

cont = open(f,'r').read().splitlines()

bn = ""

ws = False

x = 0
y = 0
z = 0
def pos():
    global x
    global y
    global z
    x += 1
    if x == 11:
        x = 0
        y += 1
    if y == 11:
        y = 0
        z += 1
    return x,y,z

def byname(nm):
    return cm2py.__getattribute__(nm)

def locate(txt):
    global bn 
    global ws
    global blocks
    global buildings
    txt = txt.strip()
    if (not '.' in txt) and ws and bn != "":
        txt = bn + '.' + txt
    if txt.startswith('global.'):
        txt = txt.replace('global.','')

    if '.' in txt:
        sp = txt.split('.')
        return buildings[sp[0]]['blocks'][sp[1]], sp[0]
    else:
        return blocks[txt], None

        
def dupe(src, t_of=0):
    global sv
    global buildings
    global blocks
    global props
    if src in buildings.keys():
        bd = buildings[src]
        otp = {"connections": [], 'blocks': {}, 'bctypes': {}, 'props': {}}
        for b in list(bd["blocks"].keys()):
            otp["blocks"][b] = sv.addBlock(byname(bd["bctypes"][b]), pos(), properties=bd["props"][b])
        for conn in bd["connections"]:
            sp = conn.split('>')
            csrc = sp[0]
            dest = sp[1]
            sv.addConnection(otp['blocks'][csrc],otp['blocks'][dest])
        return otp
    else:
        altp=props[src]
        if bctypes[src] == "TEXT" and len(props[src]) == 1:
            
            #props[src][0] += 1

            altp=[props[src][0]+t_of]
        return sv.addBlock(byname(bctypes[src]),pos(),properties=altp)

def fetchct(txt):
    txt = txt.strip()
    if '[' in txt and ']' in txt:
        otp = ''
        targ = ''
        br = False
        for v in txt:
            if v in '[]':
                br = not br
            elif br:
                otp += v
            else:
                targ += v
        alt = False
        if '.' in txt:
            alt = ']' in txt.split('.')[0]
        return int(otp.split(':')[0]), int(otp.split(':')[1]), alt, targ
    else:
        return -999, -999, False, txt

def cleandex(txt):
        txt = txt.strip()
        otp = ''
        targ = ''
        br = False
        for v in txt:
            if v in '[]':
                br = not br
            elif br:
                otp += v
            else:
                targ += v
        return targ
def handle_r(l):
    #linking
    global blocks
    global buildings
    global sv
    global bn 
    global ws
    spl = l.split('->')

    ct1, off1, alt1, sp1 = fetchct(spl[0])
    ct2, off2, alt2, sp2 = fetchct(spl[1])
    if -999 in [ct1,ct2]:
        src, b1 = locate(sp1)
        dest, b2 = locate(sp2)
        if (b1 is not None) and (b2 is not None) and (b1 == b2):
            buildings[b1]["connections"].append('>'.join([ spl[0].split('.')[0].strip(), spl[1].split('.')[0].strip() ]))
        sv.addConnection(src,dest)
    else:
        sp1 = cleandex(sp1)
        sp2 = cleandex(sp2)
        for i in range(ct1):
            src = ""
            dest = ""
            if alt1:
                src = f"{sp1.split('.')[0]}{i+off1}.{sp1.split('.')[1]}"
            else:
                src = sp1+f"{i+off1}"
            if alt2:
                dest = f"{sp2.split('.')[0]}{i+off2}.{sp2.split('.')[1]}"
            else:
                dest = sp2+f"{i+off2}"
            print(src,dest)
            handle_r(f'{src}->{dest}')
def handle_funcs(l):
    #run funcs, like :clone
    global blocks
    global buildings
    global props
    global sv
    global bn 
    global ws
    spl = l.split(':')
    targ = spl[0]
    func_raw = spl[1]
    func = ""
    for i in func_raw:
        if i == '(':
            break
        else:
            func += i
    arg = ''
    pr = False
    for i in func_raw:
        if i in '()':
            pr = not pr
        elif pr:
            arg += i
    if func == 'clone':
        if arg == '':
            arg = 1
        else:
            arg = int(arg)
        for c in range(arg):
            if targ in buildings.keys():
                buildings[targ+str(c)] = dupe(targ, c+1)
            else:
                blocks[targ+str(c)] = dupe(targ,c+1)
                bctypes[targ+str(c)] = bctypes[targ]
                props[targ+str(c)] = props[targ]
def proc_item(i):
    return int(i.strip())

def handle_eq(l):
    #handle definitions
    global blocks
    global buildings
    global sv
    global bn 
    global ws
    global props
    sp = l.split('=')
    n = sp[0].strip()
    typ = sp[1].strip()
    lprops = []

    if len(sp) > 2:
        lprops = list(map(proc_item, sp[2].split(',')))
    if ws and bn != "":
        buildings[bn]["blocks"][n] = sv.addBlock(byname(typ),pos(),properties=lprops)
        buildings[bn]["bctypes"][n] = typ
        buildings[bn]["props"][n] = lprops
    else:
        blocks[n] = sv.addBlock(byname(typ),pos(),properties=lprops)
        bctypes[n] = typ
        props[n] = lprops

for i in range(len(cont)):
    l = cont[i]
    if not l.startswith('#'):
        if l.startswith(' '):
            ws = True
        else:
            if bn != "":
                bn = ""
            ws = False
        l = l.lstrip()
        if l.endswith(':'):
            bn = l[:-1]
            if not bn in buildings.keys():
                buildings[bn] = {"connections": [], 'blocks': {}, 'bctypes': {}, 'props': {}}
        elif '->' in l:
            handle_r(l)
        elif ':' in l:
            handle_funcs(l)
        elif '=' in l:
            handle_eq(l)


#print(json.dumps(props,indent=1))
pyperclip.copy(sv.exportSave())
