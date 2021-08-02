# Copyright Derek Frombach, All Rights Reserved
import os
import shutil
import time
import base64
import json
import zipfile
import magic # extern
from stat import S_IREAD, S_IRGRP, S_IROTH, S_ISVTX

copy = True # Copy the files
clone = True # Clone the directory structure
extract = True # Un-zip the zips
backupTime = 60000 # Number of entries before periodic backup of hashtable
devMode = True # Allows for portability
maxSize = 4294967296 # Max file size in bytes that can be copied or checked (for fat32)
chunkSize = 268435456 # Size in bytes of each file chunk (bigger is better, unless you don't have enough RAM)
dynamicSize = True # If to ignore chunkSize and use dynamic chunk size based on available RAM
useFastHash = True # If to use blake3 instead of blake2s
readOnly = True # Make copied files read-only

folderName = "mediaStor" # Storage Folder
extensions = [
    "web",
    "audio",
    "code",
    "slide",
    "sheet",
    "image",
    "book",
    "text",
    "video",
] # Categories To Care About
badDirectories = [
    "windows",
    "programdata",
    "program files (x86)",
    "program files",
    "$recycle.bin",
] # Root Folders To Avoid
hashList = set()
newHashes = set()
verifList = set()
written = False

# Making hash computation significantly faster
if useFastHash:
    import blake3
    hashAlgorithm = blake3.blake3

    def newHash():
        return hashAlgorithm(multithreading=True)
else:
    import hashlib
    hashAlgorithm = hashlib.new

    def newHash():
        return hashAlgorithm('blake2s')

# Speedups
pathJoin = os.path.join
fileGetSize = os.path.getsize
hashListAdd = hashList.add
newHashesAdd = newHashes.add
verifListUpdate = verifList.update
pureCopy = shutil.copy2
isFile = os.path.isfile
getCurrentWorkingDirectory = os.getcwd
walk = os.walk
currentTime = time.time
pathExists = os.path.exists
base16Encode = base64.b16encode
urandom = os.urandom
zipOpen = zipfile.ZipFile
isZipfile = zipfile.is_zipfile
directoryName = os.path.dirname
fileName = os.path.basename
copyAttributes = shutil.copystat
copyCachedFile = shutil.copyfileobj
makeDirectoryStructure = os.makedirs
getDriveLetter = os.path.splitdrive
decyperCacheFile = magic.magic_file
changeProperties = os.chmod

# OS Compatability and Keep-Alive
osType = os.name
if osType == "nt":
    from ctypes import windll
    windowsDriveType = windll.kernel32.GetDriveTypeW
    windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# Dynamic Memory Allocation
if dynamicSize:
    import psutil
    chunkSize = min(int(psutil.virtual_memory()[1]) // 4, maxSize)

# Functions

def hashIt(fileA="", fileASize=0, fileBytes=b''):

    """Hashes a chunk or a file, given:
    
    fileA: The file path (string)
    fileASize: The file size (integer)
    fileBytes: The file chunk (bytes)
    """

    fileHash = newHash()
    hashUpdate = fileHash.update
    if fileA!="":
        if fileASize==0:
            fileASize = fileGetSize("python38.dll")
        fileARead = fileA.read
        while chunk := fileARead(min(chunkSize,fileASize)):
            lastChunk = chunk
            hashUpdate(chunk)
        fileA.close()
    else:
        hashUpdate(fileBytes)
        lastChunk = fileBytes
    hash = fileHash.digest()
    return hash, lastChunk

def benchMark():

    """Benchmarks the file read and hashing times"""

    print(os.getcwd())
    timeA = currentTime()
    fileASize = fileGetSize("python38.dll")
    fileA = open("python38.dll", "rb")
    hashIt(fileA, fileASize)
    timeB = currentTime()
    timeToHash = (timeB - timeA) / fileASize
    return timeToHash

def listDrives():

    """Returns a list of the drives"""

    drives = []
    badPaths = set()
    badPathsAdd = badPaths.add
    drivesAppend = drives.append
    if osType == "nt":
        for index in range(65, 91):
            driveLetter = chr(index) + ":\\"
            if pathExists(driveLetter) and (windowsDriveType(driveLetter) == 2 or windowsDriveType(driveLetter) == 3):
                drivesAppend(driveLetter)
                for badPath in badDirectories:
                    badPathsAdd(driveLetter.lower() + badPath)
    else:
        drivesAppend("/")
        for badPath in badDirectories:
            badPathsAdd("/" + badPath)
    return drives, badPaths

def loadCategories():

    """Loads the file type categories"""

    global badPaths
    fileA = open("categories.json", "r")
    forms = json.loads(fileA.read())
    fileA.close()
    extensionList = []
    extensionListAppend = extensionList.extend
    allExtensions = []
    for index in extensions:
        extensionListAppend(forms[index])
    extensionList = list(set(extensionList))
    zips = forms["archiv"]
    allExtensions.extend(extensionList)
    allExtensions.extend(zips)
    allExtensions = list(set(allExtensions))
    badPaths.add(getCurrentWorkingDirectory().lower())
    return extensionList, allExtensions, zips

def getExtension(filePath, includeZip=False, openFile=True):

    """Gets the extension of the file path and checks if its in the categories, given:

    filePath: The file path (string)
    includeZip: If to include zip in the categories
    openFile: If to open the file to look for magic
    """

    index = filePath.rfind(".")
    if index == -1 and openFile:
        possibleExtensions = decyperCacheFile(filePath)
        for extensionDetails in possibleExtensions:
            extension = extensionDetails[2].lower()[1:].strip()
            if extension == "webp" or extension == "png" or extension == "jpg" or extension == "jpeg": # Fix For An Issue Where Animated Images Appear Still
                extension = "gif"
            if includeZip:
                if extension in allExtensions:
                    return True, "." + extension
            else:
                if extension in extensionList:
                    return True, "." + extension
        return False, ".none"
    extension = filePath[index + 1 :].lower().strip()
    if extension == "webp": # Replaces Webpages With Images For Compatability
        extension = "gif"
    if includeZip:
        return extension in allExtensions, "." + extension
    return extension in extensionList, "." + extension

def isZip(filePath):

    """Checks if the file is an archive type file which can be opened by python, given:
    
    filePath: The file path (string)
    """

    index = filePath.rfind(".")
    if index > -1:
        extension = filePath[index + 1 :].lower().strip()
        return extension in zips and isZipfile(filePath)
    return False

def isCacheFile(filePath):

    """Checks if the file is a cache type file without an extension, given:

    filePath: The file path (string)
    """

    index = filePath.rfind(".")
    return index == -1

def loadHashList():

    """Loads the hashlist from file"""

    global hashList
    if isFile("hashlist.hash"):
        fileA = open("hashlist.hash", "rb")
        fileARead = fileA.read
        while chunk := fileARead(32):
            if len(chunk) == 32:
                hashListAdd(chunk)
        fileA.close()

def saveHashList():
    global written
    global newHashes

    """Saves the hashlist to file, and preforms integrity verification step"""

    if written:
        tempList=list(newHashes)
        del newHashes
        newHashes = set()
        pureCopy("hashlist.hash","~hashlist.hash")
        fileA = open("hashlist.hash", "ab")
        fileA.write(b"".join(tempList))
        fileA.close()
        pureCopy("veriflist.hash","~veriflist.hash")
        tempVar = [hashIt(fileBytes = hash)[0] for hash in tempList]
        verifListUpdate(tempVar)
        fileA = open("veriflist.hash", "wb")
        [fileA.write(hash) for hash in tempVar]
        fileA.close()
    else:
        del newHashes
        newHashes = set()
        tempList=list(hashList)
        verifListUpdate(hashList)
        if pathExists("hashlist.hash"):
            pureCopy("hashlist.hash","~hashlist.hash")
        fileA = open("hashlist.hash", "wb")
        fileA.write(b"".join(tempList))
        fileA.close()
        if pathExists("veriflist.hash"):
            pureCopy("veriflist.hash","~veriflist.hash")
        fileA = open("veriflist.hash", "wb")
        [fileA.write(hashIt(fileBytes = hash)[0]) for hash in tempList]
        fileA.close()
        written = True

def scanFiles(drives, badPaths):

    """Scans the files on the drives, given:
    
    drives: The list of the drives to scan (list of strings)
    badPaths: The list of the paths to not scan (list of strings)
    """

    goodPaths = set()
    goodPathsAdd = goodPaths.add
    if not pathExists("gudcache") or devMode:
        numberOfFiles = 0
        totalSize = 0
        for drive in drives:
            for root, dirs, files in walk(drive):
                try:
                    bad = False
                    for path in badPaths:
                        if path in root.lower():
                            bad = True
                            break
                    if not bad:
                        print(root)
                        for fileName in files:
                            path = pathJoin(root, fileName)
                            if getExtension(path, True)[0]:
                                numberOfFiles += 1
                                totalSize += fileGetSize(path)
                                goodPathsAdd(path)
                except:
                    pass
        goodPaths=list(goodPaths)
        pathCache = json.dumps([numberOfFiles,totalSize,goodPaths])
        fileA = open("gudcache", "w")
        fileA.write(pathCache)
        fileA.close()
    else:
        fileA = open("gudcache", "r")
        numberOfFiles, totalSize, goodPaths = json.loads(fileA.read())
        fileA.close()

    return goodPaths, totalSize, numberOfFiles

def calculateEstimatedTimeRemaining(totalSize, openedSize, numberOfFiles, index):

    """Attempts to calculate the estimated time remaining, given:
    *Doesn't compensate for OS overhead*
    
    totalSize: The max cumulative size of the files (integer)
    openedSize: The max cumulative size of files already processed (integer)
    numberOfFiles: The max cumulative number of files still to be processed (integer)
    index: The current number of files that have been processed (integer)
    """

    if copy:
        return ((totalSize - openedSize) * timeToHash) + ((totalSize - openedSize) * timeToCopy) + ((numberOfFiles - index) * timeToDisplay)
    else:
        return ((totalSize - openedSize) * timeToHash) + ((numberOfFiles - index) * timeToDisplay)

def modifyPath(folderName, root, sourceFileName, sourcePath, sourceFileShortName="", subFilePath="", subFileName=""):

    "Modifies a path in order to satisfy the requirement of unique file names"

    temporaryDrive = getDriveLetter(root)
    if sourceFileShortName!="":
        if clone:
            destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], sourceFileShortName, subFilePath)
        else:
            destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, fileName(subFileName))
        if isFile(destinationPath):
            replacementFileName = base16Encode(urandom(4)).decode() + extension[1]
            if clone:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], sourceFileShortName, directoryName(subFilePath), replacementFileName)
            else:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, replacementFileName)
        if isFile(destinationPath):
            replacementFileName = base16Encode(urandom(4)).decode() + extension[1]
            if clone:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], sourceFileShortName, directoryName(subFilePath), replacementFileName)
            else:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, replacementFileName)
    else:
        if clone:
            destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], sourceFileName)
        else:
            destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, sourceFileName)
        if isCacheFile(sourcePath):
            destinationPath += extension[1]
        if isFile(destinationPath):
            replacementFileName = base16Encode(urandom(4)).decode() + extension[1]
            if clone:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], replacementFileName)
            else:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, replacementFileName)
        if isFile(destinationPath):
            replacementFileName = base16Encode(urandom(4)).decode() + extension[1]
            if clone:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, temporaryDrive[0][:1], temporaryDrive[1][1:], replacementFileName)
            else:
                destinationPath = pathJoin(getCurrentWorkingDirectory(), folderName, replacementFileName)
    return destinationPath

def directoryCopy(sourcePath, fileSize, destinationPath):

    """Copies a directory structure (folders only), and copies the file into the folder if its small enough (for some reason), given:
    
    sourcePath: The source path to copy the structure from (string of leaf folder)
    fileSize: The size of the file that may or may not be copied (integer)
    destinationPath: The destination path to copy the structure to (string of parent folder)
    """

    if clone:
        makeDirectoryStructure(directoryName(destinationPath), exist_ok=True)
    if fileSize <= chunkSize:
        fileA = open(destinationPath, "wb")
        fileA.write(lastChunk)
        fileA.close()
        copyAttributes(sourcePath, destinationPath)
        return True
    return False

# Benchmarking
timeToHash = benchMark()

# Listing All Drives
drives, badPaths = listDrives()

# Path Correction
os.chdir("..")

# Load And Filter Categories
extensionList, allExtensions, zips = loadCategories()

# Loading The Very Important Hashtable
loadHashList()
print("Running")

# Scanning The Drive(s) For Applicable Files And Caching (Or Loading Cache)
goodPaths, totalSize, numberOfFiles = scanFiles(drives, badPaths)
del drives
del badPaths
print("There Are " + str(numberOfFiles) + " Media Files Detected")

# Preperation Of Variables And Timing Prediction Info
index = 0
openedSize = 0
timeToCopy = timeToHash
timeToDisplay = 0.01139822803296070972349760228548 # Printing Line Time Prediction Constant
predictedTime = calculateEstimatedTimeRemaining(totalSize, openedSize, numberOfFiles, index)

# The Main Loop
allowBackup = True
timeC = currentTime()
for sourcePath in goodPaths:
    try:
        root = directoryName(sourcePath)
        sourceFileName = fileName(sourcePath)
        sourceFileSize = fileGetSize(sourcePath) # File Size
        if sourceFileSize > 0 and sourceFileSize <= maxSize:
            extension = getExtension(sourcePath)
            if extension[0]: # If The File Type Is Wanted
                allowBackup = True
                index += 1
                print("Checking File " + str(index) + " Of " + str(numberOfFiles) + " Of Size " + str(sourceFileSize) + " Bytes")
                estimatedTimeRemaining = calculateEstimatedTimeRemaining(totalSize, openedSize, numberOfFiles, index)
                print("Estimated Time Remaining: " + str(round(estimatedTimeRemaining)) + "s")
                fileA = open(sourcePath, "rb")
                hash, lastChunk = hashIt(fileA, sourceFileSize)
                if not hash in hashList:
                    print("Copying File Of Size " + str(sourceFileSize) + " Bytes")
                    destinationPath = modifyPath(folderName, root, sourceFileName, sourcePath)
                    if copy:
                        timeA = currentTime()
                        if not directoryCopy(sourcePath, sourceFileSize, destinationPath):
                            pureCopy(sourcePath, destinationPath)
                        if readOnly:
                            changeProperties(destinationPath, S_IREAD|S_IRGRP|S_IROTH|S_ISVTX)
                        timeB = currentTime()
                        timeToCopy = (timeB - timeA) / sourceFileSize
                    hashListAdd(hash)
                    newHashesAdd(hash)
                    print("Done Copying File")
                openedSize += sourceFileSize
            elif isZip(sourcePath): #If The File Type Is Zip And Is Wanted
                allowBackup = True
                index += 1
                print("Checking Archive " + str(index) + " Of " + str(numberOfFiles) + " Of Size " + str(sourceFileSize) + " Bytes")
                sourceZip = zipOpen(sourcePath, "r")
                numberOfSubFiles = len(sourceZip.namelist())
                subFileIndex = 1
                subZipOpen = sourceZip.open
                for subFilePath in sourceZip.namelist():
                    subFileName = fileName(subFilePath)
                    extension = getExtension(subFileName, openFile=False)
                    if extension[0]:
                        sourceFileShortName = sourceFileName.split(".")[0]
                        subFileSize = sourceZip.getinfo(subFilePath).file_size
                        print("Checking Subfile " + str(subFileIndex) + " of " + str(numberOfSubFiles) + " Of Size " + str(subFileSize) + " Bytes")
                        estimatedTimeRemaining = calculateEstimatedTimeRemaining(totalSize+subFileSize, openedSize, numberOfFiles + numberOfSubFiles, index + subFileIndex)
                        print("Estimated Time Remaining: " + str(round(estimatedTimeRemaining)) + "s")
                        if subFileSize > 0 and subFileSize<=maxSize:
                            fileA = subZipOpen(subFilePath, "r")
                            hash, lastChunk = hashIt(fileA, subFileSize)
                            if not hash in hashList:
                                print("Copying File Of Size " + str(subFileSize) + " Bytes")
                                destinationPath = modifyPath(folderName, root, sourceFileName, sourcePath, sourceFileShortName, subFilePath, subFileName)
                                if copy:
                                    timeA = currentTime()
                                    if not directoryCopy(sourcePath, subFileSize, destinationPath):
                                        fileA = zipOpen(subFilePath, "r")
                                        fileB = open(destinationPath, "wb")
                                        copyCachedFile(fileA, fileB)
                                        fileA.close()
                                        fileB.close()
                                        copyAttributes(sourcePath, destinationPath)
                                    if readOnly:
                                        changeProperties(destinationPath, S_IREAD|S_IRGRP|S_IROTH|S_ISVTX)
                                    timeB = currentTime()
                                    timeToCopy = (timeB - timeA) / subFileSize
                                hashListAdd(hash)
                                newHashesAdd(hash)
                                print("Done Copying File")
                        elif subFileSize > maxSize:
                            print("File " + str(subFilePath) + " of Size " + str(subFileSize) + " Bytes Is Too Big")
                    subFileIndex += 1
            if index % backupTime == 0 and index != 0 and allowBackup: # Backup
                saveHashList()
                print("Backed Up!")
                allowBackup = False
        elif sourceFileSize > maxSize:
            print("File " + str(sourcePath) + " of Size " + str(sourceFileSize) + " Bytes Is Too Big")
    except:
        print("Failed Checking Or Copying " + str(index) + " Of " + str(numberOfFiles) + "!")
timeD = currentTime()
print(timeD - timeC)
print(predictedTime)

# Saving Hashtable
print("Done Copying And Checking Files")
saveHashList()
print("DONE EVERYTHING!")

# End Keep-Alive
if osType == "nt":
    windll.kernel32.SetThreadExecutionState(0x80000000)
