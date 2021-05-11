#Copyright Derek Frombach, All Rights Reserved
import hashlib
import os
import pathlib
import shutil
import time
from ctypes import windll

copy=False

foldername='mediaStor'
mapstor='fmap.bcsv'
hashlist=[]
el=['png','jpg','tiff','jpeg','raw','mp4','mkv','avi','mp3','ogg','wav','ts','ps','m4a','mov','flv','img','dng']
tpaths=['windows','programdata','program files (x86)','program files']
gpaths=[]

opj=os.path.join
opg=os.path.getsize
hln=hashlib.new
hla=hashlist.append
pp=pathlib.Path
sc=shutil.copy2
op=os.path.isfile
cw=os.getcwd
gp=gpaths.append
ow=os.walk
tt=time.time
oe=os.path.exists
widl=windll.kernel32.GetDriveTypeW
tlc=time.localtime
tstr=time.strftime

windll.kernel32.SetThreadExecutionState(0x80000000|0x00000001)

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
for i in range(65,91):
    q=chr(i)+':\\'
    if oe(q) and (widl(q)==2 or widl(q)==3):
        da(q)
        for ee in tpaths:
            ba(q.lower()+ee)

del tpaths

os.chdir('..')

ba(cw().lower())

def extget(a):
    i=a.rfind('.')
    q=a[i+1:].lower().strip()
    return q in el,'.'+q

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
                print(root)
                ta=tt()
                for f in files:
                    p=opj(root,f)
                    if extget(p)[0]:
                        n+=1
                        ts+=opg(p)
                        bad=True
                if bad:
                    root=root.lower()
                    if not any(x in root for x in gpaths):
                        gp(root)
                    tb=tt()
                    ttt+=tb-ta
        except: pass

ttt/=n
ttc=tth
ttd=0.0113982280329607
#Sumination of time to walk per file (given), time to compute hash per 4Mb Block (given), and time to copy per file size(running given)

print("There Are "+str(n)+" Media Files Detected")

i=0
brt=0
if copy: iitt=((n-i)*ttt)+((ts-brt)*tth)+((ts-brt)*ttc)+((n-i)*ttd)

else: iitt=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)

ggg=open(mapstor,'ab')
ggw=ggg.write
aatt=tt()
for ee in gpaths: 
    for root, dirs, files in os.walk(ee):
        for f in files:
            p=opj(root,f)
            q=extget(p)
            if q[0]:
                i+=1
                print('Checking File '+str(i)+' Of '+str(n))
                try:
                    fn=pp(p)
                    ss=opg(p)
                    if copy: etr=((n-i)*ttt)+((ts-brt)*tth)+((ts-brt)*ttc)+((n-i)*ttd)
                    else: etr=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)
                    #print('Estimated Max Time Remaining: '+tstr('%d:%H:%M:%S', etr))
                    print('Estimated Max Time Remaining: '+str(round(etr))+' s')
                    aname=str(min(fn.stat().st_mtime,fn.stat().st_ctime))+q[1]
                    g=open(p,"rb")
                    fr=g.read
                    file_hash = hln('blake2b')
                    fu=file_hash.update
                    while chunk := fr(4194304): fu(chunk)
                    h=file_hash.digest()
                    g.close()
                    if not h in hashlist:
                        hla(h)
                        print('Copying File Of Size '+str(ss)+' Bytes')
                        sp=opj(cw(),foldername,f)
                        rrn=f
                        if op(sp):
                            sp=opj(cw(),foldername,aname)
                            rrn=aname
                        if copy:
                            ta=tt()
                            sc(p,sp)
                            ggw(h+(','+rrn+'\n').encode())
                            tb=tt()
                            ttc=(tb-ta)/ss
                        print('Done Copying File')
                    brt+=ss
                except:
                    print('Failed Checking Or Copying '+str(i)+' Of '+str(n)+'!')

aaet=tt()
print(aaet-aatt)
print(iitt)

print('Done Copying And Checking Files')
ggg.close()
f=open('hashlist.hash','wb')
f.write(b''.join(hashlist))
f.close()
print('DONE EVERYTHING!')

windll.kernel32.SetThreadExecutionState(0x80000000)