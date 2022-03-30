# INDIGESTER

## An Intelligent and Fast Cross-Platform Backup and Forensics Tool

[![CodeQL](https://github.com/juicecable/Indigester/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/juicecable/Indigester/actions/workflows/codeql-analysis.yml)

- Does backups of only the file types you want
- Gets rid of duplicates
- Provides strong integrity verification
- Forensically decrypts cache files
- Extracts archives
- Keeps all of the original metadata (such as date created)
- Copies the exact directory structure
- Portable and extremely flexible
- Multicore
- Useful for regular secure offsite backups

### Instructions:

#### If backing up to a drive already in use:
  
  1. Place this folder into the removable backup drive (Only one backup drive should be inserted at a time)
  2. Modify delcopy.py, and set remdrive to the drive letter of the removable backup drive
  3. Run Delcopy.bat
  4. Run Import.bat as **Administrator** with as many of the drives that you want to backup from the ones connected at once
  5. If any other drives need to be backed up, disconnect the removable drives that have been backed up, and plug in the ones that still need to be backed up, then run Import.bat as **Administrator** again until there are no more removable drives to backup
  6. If there are any other machines that need to be backed up, unplug the backup drive, and plug it into the machines that still need to be backed up and run Import.bat as **Administrator**

#### If backing up to a new drive:

  1. Place this folder into the removable backup drive (Only one backup drive should be inserted at a time)
  2. Run Import.bat as **Administrator** with as many of the drives that you want to backup from the ones connected at once
  3. If any other drives need to be backed up, then disconnect the removable drives that have been backed up, and plug in the ones that still need to be backed up, and run Import.bat as **Administrator** again, until there are no more removable drives to backup
  4. If there are any other machines that need to be backed up, unplug the backup drive, and plug it into the machines that still need to be backed up and run Import.bat as **Administrator**
    
#### If your drive doesn't have enough space:

  1. **FOR ADVANCED USERS ONLY, BY FOLLOWING THIS LIST, YOU AGREE TO THE FACT THAT YOU ARE AWARE THAT THE STEPS IN THIS LIST COULD LEAD TO PERMANENT DATA LOSS**
  2. Unnecessary files should be manually deleted if you started with a backup drive that was already in use
  3. If you encounter a folder that you cannot delete as an Administrator, modify dels.py and set dir as the complete path to the folder that you want to attempt to delete, then run it (it will try to delete everything in the folder that it can)
  4. If the above happens, then after you are done with attempting to delete all of the bad folders, run check disk repair on the drive
  5. Now repeat step 3 for all of the bad folders after check disk has finished
    
#### If your drive runs out of space but you have multiple drives to backup to:

  1. **A Simpler Alternative** is to have multiple backup drives
  2. Copy the latest version of this folder from the last backup drive to the new one, excluding the mediaStor folder
  3. Remove the last backup drive, and leave all of the same storage devices attached until the backup program can complete without the disk filling up completely in the process
  4. While remaining in this condition as stated above, the import.py file must be modified such that devmode = False, otherwise it must be devmode = True
  5. Follow the appropriate instructions on backing up to a drive already in use or to a new drive, then go back to step 2 until all of the files are backed up
    
#### If using Mac OSX:

  1. Follow the instructions for backing up to a new drive or a drive all ready in use, except running mac_importer.sh instead of Import.bat, and mac_delcopy.sh instead of Delcopy.bat
    
#### If wanting to just test or benchmark:

  1. Follow the relevant steps for backing up a drive that is already in use or a new drive, except run Init.bat (mac_init.sh for mac) instead of Import.bat

### Compatibility

  Currently only compatible with Windows XP - Windows 11, MAC OSX, partial support for Linux, and planned support for Android
  
### Benchmark

  The program currently is able to process about 1 million relevant files per hour on an SSD machine, and 300 thousand relevant files per hour on an HDD machine.
