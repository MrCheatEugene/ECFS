import serial,os,sys,time,binascii,string                      
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

if(len(sys.argv) ==4):
	waitForData = False
	waitForWrite = False
	waitForDEVName = False
	waitForSize = False
	ser = serial.Serial(sys.argv[1], 2000000)
	buf = ""
	while True:
		string = (str(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','')))
		if(string == "10 INIT"):
			waitForDEVName = True
		elif(string == "5 INFO" and waitForDEVName == True):
			buf = ""
			waitForData = True
		elif(string == "5 INFO" and waitForSize == True):
			buf = ""
			waitForData = True
		elif(string == "5 INFO" and waitForDEVName == False):
			buf = ""
			waitForData = True
		elif(string == "6 INFOEND" and waitForDEVName == False and waitForData == True and waitForSize == True):
			waitForSize = False
			if(sys.argv[3] == "readall"):
				ser.write("21 READALL\r\n".encode("utf-8"))
				waitForData = True
			elif(sys.argv[3] == "clean"):
				ser.write("30 CLEAR\r\n".encode("utf-8"))
				if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
					print("EEPROM is now empty(every byte is 0x00). Unplug and plug back in your Arduino board now.")
					exit()
				else:
					exit()
			elif(sys.argv[3] == "factory"):
				ser.write("35 RESET\r\n".encode("utf-8"))
				if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
					print("EEPROM has been reseted to factory defaults(every byte is 0xFF). Unplug and plug back in your Arduino board now.")
					exit()
				else:
					exit()
			elif(sys.argv[3] == "write"):
				if((int(os.path.getsize(sys.argv[2])) <=int(buf.replace('\r\n','')))):
					print("File is valid for writing, using "+str(os.path.getsize(sys.argv[2]))+" out of "+str(buf.replace('\r\n','')))
				else:
					print("File isn't valid for writing, using "+str(os.path.getsize(sys.argv[2]))+" out of "+str(buf.replace('\r\n',''))+"(you need to remove "+str((os.path.getsize(sys.argv[2]) - int(buf.replace('\r\n',''))))+" bytes)")
					exit()
				waitForWrite = True
				file = open(sys.argv[2],"rb+")
				byte = b'\x00'
				addr = -1
				while byte:
					addr = addr+1
					byte = file.read(1)		
					ser.write(("25 WRITE"+'\r\n').encode("utf-8"))
					print("Writing block at address "+str(addr)+"..")
					if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
						print("Pass 1/4")
					else:
						print("Failed to write block!")
					ser.write(("5 INFO"+"\r\n").encode("utf-8"))
					if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
						print("Pass 2/4")
					else:
						print("Failed to write block!")
					ser.write(str(str(addr)+","+str(int.from_bytes(byte,"little"))+"\r\n").encode("utf-8"))
					if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
						print("Pass 3/4")
					else:
						print("Failed to write block!")
					ser.write(("6 INFOEND"+"\r\n").encode("utf-8"))
					if(ser.readline().decode("utf-8").replace('\r\n','').replace('\n','') == "15 OK"):
						print("Pass 4/4, Block written successfuly.")
					else:
						print("Failed to write block!")
					ser.readline()
					#time.sleep(0.1)
					#print(ser.readline())
				waitForData = False
				waitForWrite = False
				print("DONE FLASHING EEPROM!")
				exit()
			else:
				exit()
		elif(string == "6 INFOEND" and waitForDEVName == True and waitForData == True):
			waitForDEVName = False
			waitForData = False
			print("Device name: "+buf)
			waitForSize = True
			waitForData = True
			ser.write("3 SIZE\r\n".encode("utf-8"))
			
		elif(string == "6 INFOEND" and waitForDEVName == False and waitForData == True):
			waitForDEVName = False
			waitForData = False
			if(sys.argv[3] == "readall"):
				f = open(sys.argv[2], 'wb')
				bytesCounter = 0
				invBytesCounter = 0
				for val in buf.split():
					if (is_hex(val)):
						try:
							f.write(bytes.fromhex(val))
							bytesCounter+=1
						except ValueError as err:
							invBytesCounter+=1
					else:
						invBytesCounter+=1
				f.close()
				print("Successfuly wrote "+str(bytesCounter)+" bytes into "+sys.argv[2]+", "+str(invBytesCounter)+" bytes are invalid.")
				exit()
		else:
			if waitForData == True:
				buf+=string
			pass
else:
	print("Usage: ./ecfs-util.py [serial port] [filename] [action] (directory)")
	print("Actions:\nwrite - Flash to EEPROM\nclean - Clean EEPROM(set all blocks to 0)\nfactory - Factory reset(set all blocks to 255)")
	print("Examples:")
	print("Write ./folder/fsFile to COM3: ./ecfs-util.py COM3 fsFile write ./folder/")
	print("Write ./fsFile to COM3:  ./ecfs-util.py COM3 fsFile write")
	print("Factory reset: ./ecfs-util.py COM3 anythingCanBeWrittenHere factory")
	print("Clean EEPROM: ./ecfs-util.py COM3 anythingCanBeWrittenHere clean")
	print("Read EEPROM from COM3 and save to ./outputFSFIle: ./ecfs-util.py COM3 outputFSFIle readall")