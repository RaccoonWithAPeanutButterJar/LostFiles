import PySimpleGUI as sg
from pathlib import Path
import os
import win32api

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

    #Layout for main window
    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(file_open_column),
        ]
    ]
    #Window
    window = sg.Window("Kausta sisu", layout, finalize = True)
    #While loop for the main window
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #Folder field was filled in
        if event == "-OK-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
            ]
            window["-FILE LIST-"].update(fnames)
        # A file was chosen from the listbox
        elif event == "-FILE LIST-":  
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
global find_files
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
    print(read)
    if len(read) > 20:
        ajal.seek(0)
        ajal.truncate(0)
        #open('ajalugu.txt', 'w').close()
        ajal.writelines(read[1:])
    else:
        pass

with open("ajalugu.txt", "r+") as ajalugutxt:
    filepaths = []
    for rida in ajalugutxt:
        filepaths.append(rida)
        fpath = [
                f
                for f in filepaths
                ]

faili_otsimis_menüü = [
        [sg.Text('Mis faili soovid leida: ')],
        [sg.In(size=(40, 20), key = "-INPUT-"), sg.FolderBrowse()],
        [sg.Text('Kust kettalt (Kui kasutad browse, siis võid vahele jätta): ')],
        [sg.Combo(values = add_drives(), default_value = add_drives()[0], font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')],
        [sg.Text('Missugust vastuse formaati soovid: ')],
        [sg.Combo(values = ['top dir', 'bot dir', 'ketas', 'vii sinna'], default_value = 'vii sinna', font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-VASTUS-')],
        [sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"), sg.Button("Cancel", enable_events = True, key = "-CANCEL-")]
        ]

ajalugu = [
    [sg.Text("Ajalugu")],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-AJALUGU-")],
]

layout2 = [
        [
            sg.Column(ajalugu),
            sg.VSeperator(),
            sg.Column(faili_otsimis_menüü),
        ]
]

global filepath

window = sg.Window('Faili otsing', layout2, finalize = True)
if filepaths:
    window["-AJALUGU-"].update(fpath)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit" or event == "-CANCEL-":
        break
    elif event == "-AJALUGU-":
        filepath = values["-AJALUGU-"][0]
        print(filepath)
        break
    elif event == "-OK-":
        if os.path.isdir(values["-INPUT-"]):
            filepath = values["-INPUT-"]
            print(filepath)
            with open("ajalugu.txt", "a") as history:
                history.write(filepath + '\n')
            break
        else:
            filepath = find_files(values["-INPUT-"], values["-COMBO-"])
            print(filepath)
            with open("ajalugu.txt", "a") as history:
                history.write(filepath + '\n')
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
