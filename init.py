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

copy=False
clone=False
extract=True

foldername='mediaStor'
mapstor='fmap.bcsv'
hashlist=[]
exs=['web','audio','code','slide','sheet','image','book','text','video']
tpaths=['windows','programdata','program files (x86)','program files','$Recycle.Bin']
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
if otype=='nt':
    for i in range(65,91):
        q=chr(i)+':\\'
        if oe(q) and (widl(q)==2 or widl(q)==3):
            da(q)
            for ee in tpaths:
                ba(q.lower()+ee)
else:
    da('/')
    for ee in tpaths:
        ba('/'+ee)

del tpaths

os.chdir('..')

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

if not os.path.exists('gudcache'):

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

    gud=json.dumps(gpaths)
    f=open('gudcache','w')
    f.write(gud)
    f.close()

else:

    f=open('gudcache','r')
    gpaths=json.loads(f.read())
    f.close()
    n=1200
    ttt=0.01
    ts=100

ttt/=n
ttc=tth
ttd=0.01139822803296070972349760228548
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
                        if copy: etr=((n-i)*ttt)+((ts-brt)*tth)+((ts-brt)*ttc)+((n-i)*ttd)
                        else: etr=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)
                        #print('Estimated Max Time Remaining: '+tstr('%d:%H:%M:%S', etr))
                        print('Estimated Max Time Remaining: '+str(round(etr))+' s')
                        #aname=str(min(fn.stat().st_mtime,fn.stat().st_ctime))+q[1]
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
                            if clone: sp=opj(cw(),foldername,oy(root)[0][:1],oy(root)[1][1:],f)
                            else: sp=opj(cw(),foldername,f)
                            rrn=f
                            if isdumb(p): sp+=q[1]
                            if op(sp):
                                rrn=bs(ou(16)).decode()+q[1]
                                if clone: sp=opj(cw(),foldername,oy(root)[0][:1],oy(root)[1][1:],rrn)
                                else: sp=opj(cw(),foldername,rrn)
                            if copy:
                                ta=tt()
                                if clone: om(od(sp),exist_ok=True)
                                sc(p,sp)
                                ggw(h+(','+rrn+'\n').encode())
                                tb=tt()
                                ttc=(tb-ta)/ss
                            print('Done Copying File')
                        brt+=ss
                    except:
                        print('Failed Checking Or Copying '+str(i)+' Of '+str(n)+'!')
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
                                    #if copy: etr=((n-i)*ttt)+((ts-brt)*tth)+((ts-brt)*ttc)+((n-i)*ttd)
                                    #else: etr=((n-i)*ttt)+((ts-brt)*tth)+((n-i)*ttd)
                                    #print('Estimated Max Time Remaining: '+tstr('%d:%H:%M:%S', etr))
                                    #print('Estimated Max Time Remaining: '+str(round(etr))+' s')
                                    #aname=str(min(fn.stat().st_mtime,fn.stat().st_ctime))+q[1]
                                    g=zipo(nn,"r")
                                    fr=g.read
                                    file_hash = hln('blake2b')
                                    fu=file_hash.update
                                    while chunk := fr(4194304): fu(chunk)
                                    h=file_hash.digest()
                                    g.close()
                                    if not h in hashlist:
                                        hla(h)
                                        print('Copying File Of Size '+str(ss)+' Bytes')
                                        if clone: sp=opj(cw(),foldername,oy(root)[0][:1],oy(root)[1][1:],f,nn)
                                        else: sp=opj(cw(),foldername,ob(r))
                                        rrn=ob(r)
                                        if op(sp):
                                            aname=bs(ou(16)).decode()+q[1]
                                            if clone: sp=opj(cw(),foldername,oy(root)[0][:1],oy(root)[1][1:],f,od(nn),aname)
                                            else: sp=opj(cw(),foldername,aname)
                                            rrn=aname
                                        if copy:
                                            ta=tt()
                                            g=zipo(nn,"r")
                                            if clone: om(od(sp),exist_ok=True)
                                            dg=open(sp,'wb')
                                            co(g,dg)
                                            g.close()
                                            dg.close()
                                            cs(p,sp)
                                            ggw(h+(','+rrn+'\n').encode())
                                            tb=tt()
                                            ttc=(tb-ta)/ss
                                        print('Done Copying File')
                            o+=1
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

if otype=='nt': windll.kernel32.SetThreadExecutionState(0x80000000)