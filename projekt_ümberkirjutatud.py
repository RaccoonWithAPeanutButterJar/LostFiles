import PySimpleGUI as sg
from pathlib import Path
import os
import win32api

layout1 = [[sg.Text('Mis faili soovid leida: ')],
          [sg.In(size=(40, 20), enable_events = True, key = "-INPUT-"), sg.FolderBrowse()],
          [sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"), sg.Cancel()]]

window = sg.Window('Faili otsing', layout1)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-INPUT-":
        global filepath
        filepath = values["-INPUT-"]
        print(filepath)
        break
window.close()

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

#File view
file_list_column = [
    [
        sg.Text("Folder: "),
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
window = sg.Window("FILE VIEWER", layout, finalize = True)

#While loop for the main window
# Folder name was filled in form the last window, make a list of files in the folder
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
