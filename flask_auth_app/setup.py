##Setup script for the project
#This script will edit working paths within the files
#To change:

# ./project/main.py: line 19
# subprocess.Popen(['/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/receiver.py'], shell=True)

# ./project/main.py: line 24
# subprocess.Popen(["sh /home/beechat/BeechatHive-main/flask_auth_app/project/killradio.sh"], shell=True)

# ./project/main.py: line 38
# print("/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"")

# ./project/main.py: line 40
# subprocess.Popen(["/bin/python3 /home/beechat/BeechatHive-main/flask_auth_app/project/sender.py \"<G>"+gateway+"</G><T>"+ xmppaddress +"</T><M>"+ message+"</M>\"" ], shell=True)



# Import the os module
import os

# Get the current working directory
cwd = os.getcwd()

# Print the current working directory
print("Current working directory: {0}".format(cwd))


#input file
fin = open(cwd+"/project/main.py", "rt")
#output file to write the result to
fout = open(cwd+"/project/main.py.out", "wt")
#for each line in the input file
for line in fin:
	#read replace the string and write to output file
	fout.write(line.replace('/home/beechat/BeechatHive-main/flask_auth_app/', cwd+"/"))
#close input and output files
fin.close()
fout.close()

#Delete old file
myfile= cwd+"/project/main.py"

## Try to delete the file ##
try:
    os.remove(myfile)
except OSError as e:  ## if failed, report it back to the user ##
    print ("Error: %s - %s." % (e.filename, e.strerror))
#Rename new file
os.rename(cwd+"/project/main.py.out",cwd+"/project/main.py")

