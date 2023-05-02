import PySimpleGUI as sg
from pathlib import Path
import os
import win32api

global filepath
global find_files

#Arvutis leiduvate ketaste leidmine
global drives
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]
def add_drives(list = []):
    for i in drives:
        list.append(i)
    return list

#Kausta minemine
def kaust(filepath):
    #File view
    file_list_column = [
        [
            sg.Text("Folder: "),
            #filepath here
            sg.Input(default_text = filepath, size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.Button("Lemmik", enable_events = True, size = (6,1), key = "-FAVOURITE-"),
            sg.FolderBrowse(),
            sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]

    file_open_column = [
        [sg.Text("Choose a file from the list:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(file_open_column),
        ]
    ]

    window = sg.Window("Kausta sisu", layout, finalize = True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-OK-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
            ]
            window["-FILE LIST-"].update(fnames)
        #Vajutatakse "lemmik" nuppu
        if event == "-FAVOURITE-":
            with open("lemmikud.txt", "a") as lemmikud:
                    lemmikud.write(filepath + '\n')
        # A file was chosen from the listbox
        if event == "-FILE LIST-":  
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
                )
            if Path(filename).is_file():
                try:
                    with open(filename, "rt", encoding='utf-8') as f:
                        text = f.read()
                    popup_text(filename, text)
                except Exception as e:
                    print("Error: ", e)
        
    window.close()

#Faili leidmine
def find_files(filename, search_path):
   result = []
# Walking top-down from the root
   for root, dir, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result[0]

#definition for popup
def popup_text(filename, text):

    layout = [
        [sg.Multiline(text, size=(80, 25)),],
    ]
    win = sg.Window(filename, layout, modal=True, finalize=True)

    while True:
        event, values = win.read()
        if event == sg.WINDOW_CLOSED:
            break
    win.close()  

with open ("ajalugu.txt", "r+") as ajal:
    read = ajal.readlines()
    if len(read) > 20:
        ajal.seek(0)
        ajal.truncate(0)
        #open('ajalugu.txt', 'w').close()
        ajal.writelines(read[1:])
    else:
        pass

#Ajaloo failist ridade lugemine
with open("ajalugu.txt", "r+") as ajalugutxt:
    filepaths_ajalugu = []
    for rida in ajalugutxt:
        filepaths_ajalugu.append(rida)
        fpath = [
                f
                for f in filepaths_ajalugu
                ]
#Lemmikud failist ridade lugemine
with open("lemmikud.txt", "r+") as lemmikudtxt:
    filepaths_lemmikud = []
    for rida in lemmikudtxt:
        filepaths_lemmikud.append(rida)
        fpath2 = [
                f
                for f in filepaths_lemmikud
                ]

faili_otsimis_menüü = [
        [sg.Text('Mis faili soovid leida: ')],
        [sg.In(size=(40, 20), key = "-INPUT-"), sg.FolderBrowse()],
        [sg.Text('Kust kettalt (Kui kasutad browse, siis võid vahele jätta): ')],
        [sg.Combo(values = add_drives(), default_value = 'C:\ ', font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')],
        [sg.Text('Missugust vastuse formaati soovid: ')],
        [sg.Combo(values = ['top dir', 'bot dir', 'ketas'], default_value = 'top dir', font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-VASTUS-')],
        [sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"), sg.Button("Cancel", enable_events = True, key = "-CANCEL-")]
        ]

ajalugu = [
    [sg.Text("Ajalugu")],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-AJALUGU-")],
]

lemmikud = [
    [sg.Text("Lemmikud")],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-LEMMIKUD-")],
]

layout2 = [
        [
            sg.Column(ajalugu),
            sg.Column(lemmikud),
            sg.VSeperator(),
            sg.Column(faili_otsimis_menüü),
        ]
]

window = sg.Window('Faili otsing', layout2, finalize = True)
if filepaths_ajalugu:
    window["-AJALUGU-"].update(fpath)
if filepaths_lemmikud:
    window["-LEMMIKUD-"].update(fpath2)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit" or event == "-CANCEL-":
        break
    #Kui valitakse ajaloo tulbast fail
    elif event == "-AJALUGU-":
        filepath = values["-AJALUGU-"][0]
        break
    #Kui valitakse lemmikute tulbast väärtus
    elif event == "-LEMMIKUD-":
        filepath = values["-LEMMIKUD-"][0]
        break
    #Kui otsitakse faili
    elif event == "-OK-":
        if values["-VASTUS-"] == 'top dir':
            if os.path.isdir(values["-INPUT-"]):
                filepath = values["-INPUT-"]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
            else:
                filepath = find_files(values["-INPUT-"], values["-COMBO-"])
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
        if values["-VASTUS-"] == 'bot dir':
            if os.path.isdir(values["-INPUT-"]):
                filepath = values["-INPUT-"].split("/")[0] + "/" + values["-INPUT-"].split("/")[1]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
            else:
                filepath = find_files(values["-INPUT-"], values["-COMBO-"]).split("\\")[0] + "\\" + find_files(values["-INPUT-"], values["-COMBO-"]).split("\\")[1]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
        if values["-VASTUS-"] == 'ketas':
            if os.path.isdir(values["-INPUT-"]):
                filepath = values["-INPUT-"][0:3]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
            else:
                filepath = find_files(values["-INPUT-"], values["-COMBO-"])[0:3]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(filepath + '\n')
                break
window.close()

if os.path.isdir(filepath):
   kaust(filepath)
else:
    faili_tulemuste_menüü = [
        [
            sg.Text(f"Sinu fail asub: {filepath}"),
            sg.Button("Vii sinna", enable_events = True, key = "-VII-"),
        ]
    ]

    window = sg.Window("Faili asukoht", faili_tulemuste_menüü, finalize = True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit" or event == "-CANCEL-":
            break
        elif event == "-VII-":
            kaust(filepath[0:filepath.rfind("\\")])
            break
            
    window.close()
