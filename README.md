# ECFS
EEPROM Compatible File System is a really simple file system, made specifically to use with Arduino's EEPROM.
# Tools
To work with ECFS tools, you need to have Python 3.9 minimum. I think it will work with 3.7, but I can't guarantee.
## ecfs-add 
ADD File to ECFS file
Usage: ./ecfs-add.py [file to add] [ECFS filesystem file] (directory)

## ecfs-mkfs
MAKE ECFS filesystem file

Usage: ./ecfs-mkfs.py FileSystemOutFileName FSPartitionName
FileSystemOutFileName is the output file.

## ecfs-export
EXPORT files from ECFS

Usage: ecfs-export.py [filesystem file] (action on duplicate file = copy(export with another name)|die(stop exporting and close programm)|overwrite(overwrite old file with new)) (folder)

## ecfs-util
UTILITY to WORK with EEPROM via serial port<br/>
Usage: ./ecfs-util.py [serial port] [filename] [action] (directory)<br/>
Actions:<br/>write - Flash to EEPROM<br/>clean - Clean EEPROM(set all blocks to 0)<br/>factory - Factory reset(set all blocks to 255)<br/>
Examples:<br/>
Write ./folder/fsFile to COM3: ./ecfs-util.py COM3 fsFile write ./folder<br/>
Write ./fsFile to COM3:  ./ecfs-util.py COM3 fsFile write<br/>
Factory reset: ./ecfs-util.py COM3 anythingCanBeWrittenHere factory<br/>
Clean EEPROM: ./ecfs-util.py COM3 anythingCanBeWrittenHere clean<br/>
Read EEPROM from COM3 and save to ./outputFSFIle: ./ecfs-util.py COM3 outputFSFIle readall<br/>

## ecfs-edit
UTILITY to read, edit, and write ECFS to EEPROM<br/>
REQUIRES ECFS-MKFS,ECFS-EXPORT, ECFS-ADD AND ECFS-UTIL (as ecfs-mkfs.py,ecfs-export.py, ecfs-add.py,ecfs-util.py) BE IN THE SAME DIRECTORY WITH ECFS-EDIT!
Usage: ./ecfs-edit.py [comPort]<br/>

1. Run ./ecfs-edit.py [comPort]
2. If ECFS is valid, files will be exported and output directory path will be written like this:
```
Current directory: C:\ecfs\temp-35876
Are done with editing files?
```
3. Open directory [current directory] and make changes to files, if you want.  Final size of directory must be less, than eeprom size. 
4. Go to terminal again, and press "y" and then "enter".
5. Wait for FS to build and flash to EEPROM. Direcrory [current directory] will be removed. If the FS file size will be more than EEPROM size, eeprom-edit will crash.
6. If flashing was successful, you will get exit code 0 and an "Done flashing." message.

# Arduino sketch

To start working with ECFS, you need to upload specific sketch to Arduino. It is called ecfs-api.ino and is available in Main branch of this repo.
<br/>

# Support me
If you want to support me, you can donate me here: https://donationalerts.com/r/mrcheatt
