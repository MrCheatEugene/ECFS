import time,sys,random
try:
    if(len(sys.argv) ==2 or len(sys.argv) >=3 ):
        with open(sys.argv[1], "r+b") as f:
            byte = f.read(1)
            files = []
            prevTell = 0
            firstSevenByte = True;
            currentWritingFile  = open("empty", 'wb')
            doWriteFile = False
            FID = 0
            while byte:
                
                # Do stuff with byte.
                if(firstSevenByte == True):
                    sevenbyte = f.read(8)
                pass
                if (sevenbyte == bytearray(b'ECFS\x00\x00\x00\x00') and firstSevenByte == True):
                    print("This is a ECFS file system.")
                    firstSevenByte = False
                    print("Name: "+f.read(8).decode("utf-8"))
                    FID+=1
                    f.seek(16)
                elif(firstSevenByte == False):
                     if(f.read(8) == bytearray(b'FSEND\x00\x00\x00')):
                        print("File \""+fileName+"\" exported successfuly.")
                        print("Done.")
                        exit()
                     else:
                        f.seek(f.tell()-8)
                     #if():
                     #	exit()
                     if(doWriteFile == False and f.read(8)==bytearray(b'FILE\x00\x00\x00\x00')):
                        doWriteFile = True
                        fileName = f.read(8).replace(b'\x00',b'').decode("utf-8")
                        if(fileName in files and len(sys.argv) >= 3 and sys.argv[2] == "copy"):
                            copyfileName = fileName+"_copy("+str(random.randint(10000,99999))+")"
                            print("File \""+fileName+"\" already exists! It will be exported as \""+copyfileName+"\".")
                            fileName = copyfileName
                            print("WARNING: THIS FILESYSTEM IS DAMAGED, PLEASE FIX IT")
                        elif(fileName in files and len(sys.argv) >= 3 and sys.argv[2] == "die"):
                            print("File \""+fileName+"\" already exists!")
                            print("WARNING: THIS FILESYSTEM IS DAMAGED, PLEASE FIX IT")
                            print("Exiting..")
                            exit()
                        elif(fileName in files and len(sys.argv) >= 3 and sys.argv[2] == "overwrite"):
                            print("File \""+fileName+"\" already exists! The previous file called \""+fileName+"\" will be rewritten by current file.")
                            print("WARNING: THIS FILESYSTEM IS DAMAGED, PLEASE FIX IT")
                        elif(fileName in files and len(sys.argv) <= 2):
                            print("File \""+fileName+"\" already exists!")
                            print("WARNING: THIS FILESYSTEM IS DAMAGED, PLEASE FIX IT")
                            print("Exiting..")
                            exit()
                        files.append(fileName)
                        print("Trying to export file \""+fileName+"\"...")
                        dirToExport = ""
                        if(len(sys.argv)>=4):
                            dirToExport = sys.argv[3]
                        currentWritingFile = open(dirToExport+fileName, "wb")
                     else:
                        bytetow = f.read(1);
                        if(doWriteFile):
                           if(f.read(8)==bytearray(b'FILE\x00\x00\x00\x00')):
                               doWriteFile = False;
                               if(FID == 1):
                                  currentWritingFile.write(bytetow)
                               f.seek(f.tell()-8)
                               print("File \""+fileName+"\" exported successfuly.")
                           else:
                               currentWritingFile.write(bytetow)
                               f.seek(f.tell()-8)
                     #exit()
                else:
                	print("This is not a ECFS file system.")
                	exit()
    else:
        print("Usage: ecfs-export.py [filesystem file] (action on duplicate file = copy(export with another name)|die(stop exporting and close programm)|overwrite(overwrite old file with new)) (folder)")
except IOError:
    print('Error While Opening the file!')  
