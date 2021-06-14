#Copyright Derek Frombach, All Rights Reserved
import hashlib
import os
#import pathlib
import shutil
import time
import magic #extern
import base64
import json
import zipfile

copy=True
clone=True
extract=True
delothers=False #do not set to true

remdrive='D'
hashlist=[]
exs=['web','audio','code','slide','sheet','image','book','text','video','archiv']
tpaths=['windows','program files (x86)','program files','$recycle.bin','system volume information']
gpaths=[]

otype=os.name
if otype=='nt':
    from ctypes import windll

opj=os.path.join
opg=os.path.getsize
hln=hashlib.new
hla=hashlist.append
#pp=pathlib.Path
sc=shutil.copy2
op=os.path.isfile
cw=os.getcwd
gp=gpaths.append
ow=os.walk
tt=time.time
oe=os.path.exists
if otype=='nt': widl=windll.kernel32.GetDriveTypeW
tlc=time.localtime
tstr=time.strftime
bs=base64.b16encode
ou=os.urandom
zp=zipfile.Path
zz=zipfile.ZipFile
zi=zipfile.is_zipfile
od=os.path.dirname
ob=os.path.basename
cs=shutil.copystat
co=shutil.copyfileobj
om=os.makedirs
oy=os.path.splitdrive
ot=os.remove

if otype=='nt': windll.kernel32.SetThreadExecutionState(0x80000000|0x00000001)

ta=tt()
g=open('python38.dll',"rb")
fr=g.read
file_hash = hln('blake2b')
fu=file_hash.update
while chunk := fr(4194304): fu(chunk)

h=file_hash.digest()
g.close()
tb=tt()
tth=(tb-ta)/4194304

drives=[]
bpaths=[]
ba=bpaths.append
da=drives.append
q=remdrive+':\\'
da(q)
for ee in tpaths:
    ba(q.lower()+ee)

del tpaths

os.chdir('..')

if oe('hashlist.hash'):
    y=input('The Data File Already exists, continuing could perminently delete all data, do you want to loose data? (y/n): ')
    if y.strip().lower()=='y':
        y=input('Are you really sure you want to loose data? (y/n): ')
        if y.strip().lower()=='y':
            pass
        else:
            print('Exiting')
            exit()
    else:
        print('Exiting!')
        exit()

f=open('categories.json','r')
forms=json.loads(f.read())
f.close()
el=[]
ela=el.extend
al=[]
for n in exs:
    ela(forms[n])
el=list(set(el))
zips=forms['archiv']
al.extend(el)
al.extend(zips)
al=list(set(al))
del forms

ba(cw().lower())

def extget(a,bind=False,r=True):
    i=a.rfind('.')
    if i==-1 and r:
        e=magic.magic_file(a)
        for n in e:
            q=n[2].lower()[1:].strip()
            if q=='webp' or q=='png' or q=='jpg' or q=='jpeg': q='gif'
            if bind:
                if q in al: return True,'.'+q
            else:
                if q in el: return True,'.'+q
        return False,'.none'
    q=a[i+1:].lower().strip()
    if q=='webp': q='gif'
    if bind: return q in al,'.'+q
    return q in el,'.'+q

def iszip(a):
    i=a.rfind('.')
    if i>-1:
        q=a[i+1:].lower().strip()
        return q in zips and zi(a)
    return False

def isdumb(a):
    i=a.rfind('.')
    return i==-1

def subfolder(p):
    contents = p.iterdir()
    for i in contents:
        if i.is_file(): yield i
        elif i.is_dir(): yield from subfolder(i)

if op('hashlist.hash'):
    f=open('hashlist.hash','rb')
    fr=f.read
    while chunk := fr(64):
        if len(chunk)==64: hla(chunk)
    f.close()

print("Running")

n=0
ts=0
ttt=0
for drive in drives:
    for root, dirs, files in ow(drive):
        try:
            bad=False
            for q in bpaths:
                if q in root.lower():
                    bad=True
                    break
            if not bad:
                ta=tt()
                for f in files:
                    p=opj(root,f)
                    if extget(p,True)[0]:
                        n+=1
                        ts+=opg(p)
                        bad=True
                if bad:
                    root=root.lower()
                    if not any(x in root for x in gpaths):
                        print(root)
                        gp(root)
                    tb=tt()
                    ttt+=tb-ta
        except: pass

if delothers:
    gpaths=[drives[0]]

ttt/=n
ttc=tth
ttd=0.01139822803296070972349760228548
#Sumination of time to walk per file (given), time to compute hash per 4Mb Block (given), and time to copy per file size(running given)

print("There Are "+str(n)+" Media Files Detected")

i=0
brt=0

iitt=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)

input(gpaths)

aatt=tt()
for ee in gpaths: 
    for root, dirs, files in ow(ee):
        for f in files:
            p=opj(root,f)
            ss=opg(p)
            if ss>0:
                try: q=extget(p)
                except: continue
                if q[0]:
                    i+=1
                    print('Checking File '+str(i)+' Of '+str(n))
                    try:
                        #fn=pp(p)
                        etr=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)
                        print('Estimated Max Time Remaining: '+str(round(etr))+' s')
                        g=open(p,"rb")
                        fr=g.read
                        file_hash = hln('blake2b')
                        fu=file_hash.update
                        while chunk := fr(16777216): fu(chunk)
                        h=file_hash.digest()
                        g.close()
                        if not h in hashlist:
                            hla(h)
                        else:
                            print('Deleting File: '+p)
                            ot(p)
                        brt+=ss
                    except:
                        print('Failed Checking Or Deleting '+str(i)+' Of '+str(n)+'!')
                elif iszip(p):
                    try:
                        i+=1
                        print('Checking Archive '+str(i)+' Of '+str(n))
                        zipd=zz(p,'r')
                        ln=len(zipd.namelist())
                        o=1
                        zipi=zipd.getinfo
                        zipo=zipd.open
                        for nn in zipd.namelist():
                            r=ob(nn)
                            gg=extget(r,r=False)
                            if gg[0]:
                                f=f.split('.')[0]
                                print('Checking Subfile '+str(o)+' of '+str(ln))
                                ss=zipd.getinfo(nn).file_size
                                if ss>0:
                                    g=zipo(nn,"r")
                                    fr=g.read
                                    file_hash = hln('blake2b')
                                    fu=file_hash.update
                                    while chunk := fr(16777216): fu(chunk)
                                    h=file_hash.digest()
                                    g.close()
                                    if not h in hashlist:
                                        hla(h)
                            o+=1
                    except:
                        print('Failed Checking Or Deleting '+str(i)+' Of '+str(n)+'!')
                elif delothers:
                    print('Deleting File: '+p)
                    ot(p)

aaet=tt()
print(aaet-aatt)
print(iitt)

print('Done Deleting And Checking Files')
f=open('hashlist.hash','wb')
f.write(b''.join(hashlist))
f.close()
print('DONE EVERYTHING!')

if otype=='nt': windll.kernel32.SetThreadExecutionState(0x80000000)