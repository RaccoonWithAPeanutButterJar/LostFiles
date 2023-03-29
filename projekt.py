from easygui import*
import os
import win32api
img = ".\\racc.png"
#Mida
otsitav = enterbox("What file are you looking for?")
#Arvutis leiduvad kettad
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
#Kust
path = buttonbox("From where do you want to search?" + "\n" + "(He will find it)", "Choose which drive",image = img,  choices = drives)
#Faili leidmine
def find_files(filename, search_path):
   result = []
# Walking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return msgbox(f"Fail asub: {result}") #Message

find_files(otsitav,path)