import os,pyAesCrypt,argparse,secrets
from alive_progress import alive_bar
from time import sleep
parser = argparse.ArgumentParser(
add_help=False,
formatter_class=argparse.RawDescriptionHelpFormatter,
description='''\
Version 1.0
Just a script to AES encrypt stuff
------------------------------------
name.py -o [encrypt] [decrypt] -f filename.txt -key keyname.key
name.py -o [encrypt] [decrypt] -d /dirpath/ -key keyname.key
name.py --keygen "keyname.key"
''')
parser.add_argument('-o','--operation')
parser.add_argument('-d','--dir')
parser.add_argument('-f','--file')
parser.add_argument('-k','--key')
parser.add_argument('--keygen')
parser.print_help()
args = parser.parse_args() 
def keygen(keyName):
    with open(keyName,'wb') as kFile:
        kFile.write(secrets.randbits(1024))
        return(kFile)
def loadKey(kFile):
    with open(kFile,'rb') as key:
        return key.peek().hex()
if args.keygen:
    keygen(args.keygen)
if args.operation == "encrypt" and args.dir:
    if args.key == "":
        print('No key entered')
    for f in os.listdir(args.dir):
        if ".yn" in f:
            continue
        f=args.dir+"/"+f
        pyAesCrypt.encryptFile(f,f+'.yn',loadKey(args.key),bufferSize=64*1024)
        with alive_bar(1,title='Encrypting: '+f, bar='classic2') as bar:
            for f in args.dir:
                sleep(0.01)
            bar()
if args.operation == "encrypt":
    if args.file:
        if args.key == "":
            print('No key entered')
        pyAesCrypt.encryptFile(args.file,args.file+'.yn',loadKey(args.key),bufferSize=64*1024)
        print("Encrypting: "+args.file,"> ",args.file+".yn" )
if args.operation == "decrypt" and args.dir:
    if args.key == "":
        print('No key entered')
    for f in os.listdir(args.dir):
        if ".yn" in f:
            f=args.dir+"/"+f
            pyAesCrypt.decryptFile(f,f.replace(".yn",""),loadKey(args.key),bufferSize=64*1024)
            with alive_bar(1,title='Decrypting: '+f, bar='classic2') as bar:
                for f in args.dir:
                    sleep(0.01)
                bar()
if args.operation == "decrypt":
    if args.file:
        if args.key == "":
            print('No key entered')
        else:
            if '.yn' in args.file:
                pyAesCrypt.decryptFile(args.file,args.file.strip(".yn"),loadKey(args.key),bufferSize=64*1024)
                print("Decrypting: "+args.file,"> ",args.file.strip(".yn") )
            else:
                print("Unable to decrypt file")





