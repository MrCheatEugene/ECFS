import sys
if not(len(sys.argv)>=3):
	print("If you want to use CLI, run ecfs-mkfs like this: ecfs-mkfs.py FileSystemOutFileName FSPartitionName")
	print("Enter output FS Partition file name: ")
	fsName = input()
	print("Enter FS name(up to 7 chars): ")
	fsUserName = input()
else:
	fsName = sys.argv[1]
	fsUserName = sys.argv[2]
if not(len(fsUserName) <=7):
	print("FS Name is more than 7 chars!")
	sys.exit(1)
else:
	fsFile= open(fsName,'wb')
	byteFSUserName = fsUserName.encode('utf-8')
	while(len(byteFSUserName) < 7):
		byteFSUserName+=b'\x00'
	fsFile.write(b'\x00ECFS\x00\x00\x00\x00'+byteFSUserName)
	fsFile.write(b'FSEND\x00\x00\x00')
	fsFile.close()
	print("Done!")
	sys.exit(0)