import os
import sys
if(len(sys.argv) >=3):
	if(len(sys.argv)>=4):
		dirName = sys.argv[3]+"/"
	else:
		dirName= ""
	f2 = open(dirName+sys.argv[1],'rb+')
	f = open(sys.argv[2], 'rb+')
	f.seek(1)
	sevenbyte = f.read(8)
	if (sevenbyte == bytearray(b'ECFS\x00\x00\x00\x00')):
		print("This is a ECFS file system.")
		print("Name: "+f.read(8).decode("utf-8"))
	else:
		print("This is not a ECFS file system.")
		exit()
	pass
	f.seek(-8, os.SEEK_END)
	f.truncate()
	fileNameFile =(sys.argv[1][:8]).encode("utf-8")
	while(len(fileNameFile) < 8):
		fileNameFile+=b'\x00'
	f.write(bytearray(b'FILE\x00\x00\x00\x00'+fileNameFile))
	f.write(f2.read(os.path.getsize(dirName+sys.argv[1])))
	f.write(b'FSEND\x00\x00\x00')
	f.close()
	print("Successfully added file "+sys.argv[1]+" as "+sys.argv[1][:8]+".")
	exit()
else:
	print("Usage: ./ecfs-add.py [file to add] [ECFS filesystem file] (directory)")
	exit()