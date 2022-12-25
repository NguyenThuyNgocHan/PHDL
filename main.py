import os
import sys
import wmi
from cryptography.fernet import Fernet
c=wmi.WMI()

def check_for_key(my_key):
   for disk in c.Win32_LogicalDisk():
      if disk.VolumeName==my_key:
         return disk
def load_key(usbDisk):
   port = usbDisk.DeviceID
   try:
      print('Trying to find key...')
      with open(f'{port}\\encryptionKey.key','rb') as encryptKey:
         key = encryptKey.read()
         print('Key Found')
   except:
      print('Key not found... Creating a new key')
      key = Fernet.generate_key()
      with open(f'{port}\\encryptionKey.key','wb') as encryptKey:
         encryptKey.write(key)
   return key

def encryptFiles(key,directory):
   files = os.listdir(directory)
   cipher = Fernet(key)
   global state
   state = 'encrypted'
   for file in files:
      with open(f'{directory}\{file}','rb') as old:
         original = old.read()
      encrypted = cipher.encrypt(original)
      with open(f'{directory}\{file}','wb') as old:
         old.write(encrypted)

def decryptFiles(key,directory):
   files = os.listdir(directory)
   cipher = Fernet(key)
   global state
   state = 'decrypted'
   for file in files:
      with open(f'{directory}\{file}','rb') as old:
         encrypted = old.read()
      decrypted = cipher.decrypt(encrypted)
      with open(f'{directory}\{file}','wb') as old:
         old.write(decrypted)

if __name__=='__main__':
   my_key=input("Enter the name of your USB device: ")
   FilesPath=input("Enter the path of the file you want to encrypt/decrypt: ")
   option=input("Want to encrypt your file? ->Type 1, Decrypt ->Type 2")
   if option=='1':
      state='decrypted'
   else:
      state='encrypted'
   disk = check_for_key(my_key)
   try:
      key = load_key(disk)
   except:
      print('No Key Available')
   if disk != None:
      if state=='encrypted':
         print ('Decrypting-----')
         decryptFiles(key, FilesPath)
      else:
         print ('Encrypting---------')
         encryptFiles(key, FilesPath)


# if __name__=='__main__':
#    exec(open("F:\Secret\TEXT.py").read())
#
