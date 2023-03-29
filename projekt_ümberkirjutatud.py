import PySimpleGUI as sg
from pathlib import Path
import os
import win32api

layout1 = [[sg.Text('Mis faili soovid leida: ')],
          [sg.In(size=(40, 20), key = "-FILE-"), sg.FileBrowse()],
          [sg.Button( size = (3, 1), key = "-OK-"), sg.Cancel()]] #ADD TEXT TO BUTTON!

window = sg.Window('Faili otsing', layout1)

event, values = window.read()
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
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
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

#Layout for window
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(file_open_column),
    ]
]

#Window
window = sg.Window("File Viewer", layout)

#While for the main window
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder
    elif event == "-FOLDER-":
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

    elif event == "-FILE LIST-":  # A file was chosen from the listbox
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
