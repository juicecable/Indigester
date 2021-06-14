import subprocess
import os

dir='D:\\D\\usr'
os.chdir(dir)

def dirrem(adir):
    dirs=os.listdir(adir)
    for d in dirs:
        try:
            p=os.path.join(adir,d)
            print(p)
            cmd='cmd /c del /F /Q /S '+p
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            out=proc.communicate()
            if len(out[1])>0:
                dirrem(p)
            if os.path.isdir(p):
                cmd='cmd /c rmdir /Q /S '+p
                proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            out=proc.communicate()
        except:
            pass

print('running')
dirrem(dir)