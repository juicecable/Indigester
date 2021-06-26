# INDIGESTER

## An Intelligent and Fast Cross-Platform Backup and Forensics Tool

- Does backups of only the file types you want
- Gets rid of duplicates
- Provides strong integrity verification
- Forensically decrypts cache files
- Extracts archieves
- Keeps all of the original metadata (such as date created)
- Copies the exact directory structure
- Portable and extremely flexible
- Multicore

### Instructions:

  #### If backing up to a drive already in use:
    
    1. Place this folder into the removable backup drive (Only one backup drive should be inserted at a time)
    2. Modify delcopy.py, and set remdrive to the drive letter of the removable backup drive
    3. Run Delcopy.bat
    4. Run Import.bat as **Administrator** with as many of the drives that you want to backup from connected at once
    5. If any other drives need to be backed up, then disconnect the removable drives that have been backed up, and plug in the ones that still need to be backed up, and run Import.bat as **Administrator** again, until there are no more removable drives to backup
    6. If there are any other machines that need to be backed up, unplug the backup drive, and plug it into the machines that still need to be backed up and run Import.bat as **Administrator**

  #### If backing up to a new drive:
  
    1. Place this folder into the removable backup drive (Only one backup drive should be inserted at a time)
    2. Run Import.bat as **Administrator** with as many of the drives that you want to backup from connected at once
    3. If any other drives need to be backed up, then disconnect the removable drives that have been backed up, and plug in the ones that still need to be backed up, and run Import.bat as **Administrator** again, until there are no more removable drives to backup
    4. If there are any other machines that need to be backed up, unplug the backup drive, and plug it into the machines that still need to be backed up and run Import.bat as **Administrator**
    
  #### If your drive doesn't have enough space:
  
    1. **FOR ADVANCED USERS ONLY, BY FOLLOWING THIS LIST, YOU AGREE TO THE FACT THAT YOU ARE AWARE THE STEPS IN THIS LIST COULD LEAD TO PERMINENT DATA LOSS**
    2. Unnecessary files should be manually deleted if you started with a backup drive that was already in use
    3. If you encounter a folder that you cannot delete as an Administrator, then modify dels.py and set dir as the complete path to the folder that you want to attempt to delete, then run it (it will try to delete everything in the folder that it can)
    4. If the above happens, then after you are done with attempting to delete all of the bad folders, run check disk repair on the drive
    5. Now repeat step 3 for all of the bad folders after check disk has finished
    
  #### If your drive runs out of space but you have multiple drives to backup to:
  
    1. **A Simpler Alternative** is to have multiple backup drives
    2. Copy the latest version of this folder from the last backup drive to the new one, excluding the mediaStor folder
    3. Remove the last backup drive, and leave all of the same storage devices attached until the backup program can complete without the disk filling up completely in the process
    4. While remaining in this condition as stated above, the import.py file must be modified such that devmode = False, otherwise it must be devmode = True
    5. Follow the appropriate instructions on backing up to a drive already in use or to a new drive, then go back to step 2 until all of the files are backed up

### Compatibility

  Currently only compatible with Windows XP - Windows 11, partial support for Linux, and planned support for OS X and Android
  
### Benchmark

  The program currently is able to process about 1 million relevant files per hour on an SSD machine, and 300 thousand relevant files per hour on an HDD machine.
