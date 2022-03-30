#Copyright (c) 2022 Derek Frombach
import os
import shutil
import time
import magic #extern
import json
import zipfile

delothers=False #do not set to true
extract = True # Un-zip the zips
backuptime = 6000 # Number of entries before periodic backup of hashtable
devmode = True # Allows for portability
maxsize = 4294967296 # Max file size in bytes that can be copied or checked (for fat32)
chunksize = 268435456 # Size in bytes of each file chunk (bigger is better, unless you don't have enough RAM)
dynamicsize = True # If to ignore chunksize and use dynamic chunk size based on available RAM
usefasthash = True # If to use blake3 instead of blake2s

remdrive='D' #Drive to preform the de-duplication on
exs = [
    "web",
    "audio",
    "code",
    "slide",
    "sheet",
    "image",
    "book",
    "text",
    "video",
    "archiv",
] # Categories To Care About
tpaths = [
    "windows",
    "programdata",
    "program files (x86)",
    "program files",
    "$recycle.bin",
    "system volume information",
] # Root Folders To Avoid
gpaths = set()
hashlist = set()

otype=os.name
if otype=='nt':
    from ctypes import windll

# Making hash computation significantly faster
if usefasthash:
    import blake3
    hln = blake3.blake3

    def newhash():
        return hln(multithreading=True)
else:
    import hashlib
    hln = hashlib.new

    def newhash():
        return hln('blake2s')

# Speedups
opj = os.path.join
opg = os.path.getsize
hla = hashlist.add
sc = shutil.copy2
op = os.path.isfile
cw = os.getcwd
gp = gpaths.add
ow = os.walk
tt = time.time
oe = os.path.exists
tlc = time.localtime
tstr = time.strftime
ou = os.urandom
zp = zipfile.Path
zz = zipfile.ZipFile
zi = zipfile.is_zipfile
od = os.path.dirname
ob = os.path.basename
cs = shutil.copystat
co = shutil.copyfileobj
om = os.makedirs
oy = os.path.splitdrive
mf = magic.magic_file
ot = os.remove

# OS Compatability and Keep-Alive
otype = os.name
if otype == "nt":
    from ctypes import windll
    widl = windll.kernel32.GetDriveTypeW
    windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# Dynamic Memory Allocation
if dynamicsize:
    import psutil
    chunksize = min(int(psutil.virtual_memory()[1]) // 4, maxsize)

# Benchmarking
ta = tt()
g = open("python38.dll", "rb")
fr = g.read
ss=opg("python38.dll")
file_hash = newhash()
fu = file_hash.update
while chunk := fr(min(chunksize,ss)):
    fu(chunk)
h = file_hash.digest()
g.close()
tb = tt()
tth = (tb - ta) / ss

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

# Load And Filter Categories
f = open("categories.json", "r")
forms = json.loads(f.read())
f.close()
el = []
ela = el.extend
al = []
for n in exs:
    ela(forms[n])
el = list(set(el))
zips = forms["archiv"]
al.extend(el)
al.extend(zips)
al = list(set(al))
del forms
ba(cw().lower())

# Function Definitions

def extget(a, bind=False, r=True):

    """Gets the extension of the file path and checks if its in the categories, given:

    a: The file path (string)
    bind: If to include zip in the categories
    r: If to open the file to look for magic
    """

    i = a.rfind(".")
    if i == -1 and r:
        e = mf(a)
        for n in e:
            q = n[2].lower()[1:].strip()
            if q == "webp" or q == "png" or q == "jpg" or q == "jpeg": # Fix For An Issue Where Animated Images Appear Still
                q = "gif"
            if bind:
                if q in al:
                    return True, "." + q
            else:
                if q in el:
                    return True, "." + q
        return False, ".none"
    q = a[i + 1 :].lower().strip()
    if q == "webp": # Replaces Webpages With Images For Compatability
        q = "gif"
    if bind:
        return q in al, "." + q
    return q in el, "." + q


def iszip(a):

    """Checks if the file is an archive type file which can be opened by python, given:
    
    a: The file path (string)
    """

    i = a.rfind(".")
    if i > -1:
        q = a[i + 1 :].lower().strip()
        return q in zips and zi(a)
    return False


def isdumb(a):

    """Checks if the file is a cache type file without an extension, given:

    a: The file path (string)
    """

    i = a.rfind(".")
    return i == -1


# Loading The Very Important Hashtable
if op("hashlist.hash"):
    f = open("hashlist.hash", "rb")
    fr = f.read
    while chunk := fr(32):
        if len(chunk) == 32:
            hla(chunk)
    f.close()

print("Running")

# Scanning The Drive For Applicable Files
n = 0
ts = 0
ttt = 0
for drive in drives:
    for root, dirs, files in ow(drive):
        try:
            bad = False
            for q in bpaths:
                if q in root.lower():
                    bad = True
                    break
            if not bad:
                print(root)
                ta = tt()
                for f in files:
                    p = opj(root, f)
                    if extget(p, True)[0]:
                        n += 1
                        ts += opg(p)
                        gp(p)
                tb = tt()
                ttt += tb - ta
        except:
            pass
ttt /= n
ttc = tth
ttd = 0.01139822803296070972349760228548 # Printing Line Time Prediction Constant

print("There Are " + str(n) + " Media Files Detected")

# Preperation Of Variables And Timing Prediction Info
i = 0
brt = 0
iitt = ((n - i) * ttt) + ((ts - brt) * tth) + ((n - i) * ttd)

# The Main Loop
hugs = True
aatt = tt()
for p in gpaths:
    root = od(p)
    f = ob(p)
    ss = opg(p) # File Size
    if ss > 0:
        try:
            q = extget(p)
            if q[0]: # If The File Type Is Wanted
                hugs = True
                i += 1
                print("Checking File " + str(i) + " Of " + str(n) + " Of Size " + str(ss) + " Bytes")
                etr = ((n - i) * ttt) + ((ts - brt) * tth) + ((n - i) * ttd)
                print("Estimated Max Time Remaining: " + str(round(etr)) + "s")
                g = open(p, "rb")
                fr = g.read
                file_hash = newhash()
                fu = file_hash.update
                while chunk := fr(min(chunksize,ss)):
                    fu(chunk)
                h = file_hash.digest()
                g.close()
                if not h in hashlist:
                    if not h in hashlist:
                        hla(h)
                    else:
                        print('Deleting File: '+p)
                        ot(p)
                brt += ss
            elif iszip(p): #If The File Type Is Zip And Is Wanted
                hugs = True
                i += 1
                print("Checking Archive " + str(i) + " Of " + str(n) + " Of Size " + str(ss) + " Bytes")
                zipd = zz(p, "r")
                ln = len(zipd.namelist())
                o = 1
                zipi = zipd.getinfo
                zipo = zipd.open
                for nn in zipd.namelist():
                    r = ob(nn)
                    gg = extget(r, r=False)
                    if gg[0]:
                        f = f.split(".")[0]
                        ss = zipd.getinfo(nn).file_size
                        print("Checking Subfile " + str(o) + " of " + str(ln) + " Of Size " + str(ss) + " Bytes")
                        if ss > 0:
                            g = zipo(nn, "r")
                            fr = g.read
                            file_hash = newhash()
                            fu = file_hash.update
                            while chunk := fr(min(chunksize,ss)):
                                fu(chunk)
                            h = file_hash.digest()
                            g.close()
                            if not h in hashlist:
                                hla(h)
                    o += 1
            elif delothers:
                print('Deleting File: '+p)
                ot(p)
            if i % backuptime == 0 and i != 0 and hugs: # Backup
                f = open("hashlist.hash", "wb")
                f.write(b"".join(list(hashlist)))
                f.close()
                print("Backed Up!")
                hugs = False
        except:
            print("Failed Checking Or Deleting " + str(i) + " Of " + str(n) + "!")
aaet = tt()
print(aaet - aatt)
print(iitt)

# Saving Hashtable
print("Done Copying And Checking Files")
f = open("hashlist.hash", "wb")
f.write(b"".join(hashlist))
f.close()
print("DONE EVERYTHING!")

# End Keep-Alive
if otype == "nt":
    windll.kernel32.SetThreadExecutionState(0x80000000)
