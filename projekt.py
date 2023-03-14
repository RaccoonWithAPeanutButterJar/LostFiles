import easygui
import os
import win32api
#Mida
otsitav = easygui.enterbox("What file are you looking for?")
#Arvutis leiduvad kettad
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
#Kust
path = easygui.buttonbox("From where do you want to search from?", "Choose which drive", drives)
#Faili leidmine
def find_files(filename, search_path):
   result = []
# Walking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

print(find_files(otsitav,path))