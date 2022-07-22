import sys,os,random,shutil
if(len(sys.argv) >= 2):
	comPort = sys.argv[1]
	pythonExec = sys.executable
	print("Exporting existing FS from EEProm..")
	os.system(pythonExec+" ecfs-util.py "+comPort+" ./tempFSFile readall")
	#print(pythonExec+" ecfs-util.py "+comPort+" ./tempFSFile readall")
	if(os.path.isfile("./tempFSFile")):
		print("Export success")
		print("Trying to export files from ECFS...")
		dirname = "./temp-"+str(random.randint(10000,99999))
		os.mkdir(dirname)
		exportResults = os.popen(pythonExec+" ecfs-export.py ./tempFSFile copy "+dirname+"/").read()
		print(exportResults)
		if("This is not a ECFS file system." in exportResults):
			print("Export failed; This is not an ECFS File System.")
			exit(1)
		else:			
			#os.popen('explorer.exe /e'+dirname)
			#os.popen('xdg-open "%s"' % dirname)
			if os.name == 'nt':
				print("Current directory: "+os.getcwd()+(dirname.replace('./','\\')))
			else:
				print("Current directory: "+os.getcwd()+(dirname.replace('./','/')))
			print("Are done with editing files? ")
			if(input() == "y"):
				print("Building FS...")
				print("Please, enter partition name: ")
				partitionName = input()
				mkFs = os.popen(pythonExec+" ecfs-mkfs.py tempFSFile_new "+partitionName).read()
				if( "Done!" in mkFs):
					print("Adding files..")
					for filename in os.listdir(dirname):
						addRes = os.popen(pythonExec+" ecfs-add.py "+filename+" tempFSFile_new "+dirname).read()
						if("Successfully added file" in addRes):
							print(filename+" added successfully as "+filename[:8]+".")
						else:
							print("Got errors while adding "+filename+":"+addRes)
							exit(1)
					print("Done adding files.")
					shutil.rmtree(dirname)
					os.remove("tempFSFile")
					print("FS Built successfully.")
					print("Flashing EEPROM..")
					flash = os.popen(pythonExec+" ecfs-util.py "+comPort+" tempFSFile_new write").read()
					if("DONE FLASHING EEPROM!" in flash):
						print("Done flashing.")
						os.remove("tempFSFile_new")
						exit(0)
				else:
					print("Something went wrong while making the FS. Here is full log: ")
					print(mkFs)
					os.remove("tempFSFile_new")
					exit(1)
			else:
				print("Stopping.")
				shutil.rmtree(dirname)
				os.remove("tempFSFile")
				exit(0)
	else:			
		print("Export failed")
		exit(1)

