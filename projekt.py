import easygui
import os
otsitav = easygui.enterbox("What file are you looking for?")
path = easygui.buttonbox("From where do you want to search?", "choose", ['C:', 'K:'])
def find_files(filename, search_path):
   result = []

# Wlaking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

print(find_files(otsitav,path))
