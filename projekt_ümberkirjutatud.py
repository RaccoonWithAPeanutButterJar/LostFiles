import PySimpleGUI as sg
from pathlib import Path
import os
import win32api

global faili_asukoht
global otsi_fail

#Arvutis leiduvate ketaste leidmine
global kettad
kettad = win32api.GetLogicalDriveStrings()
kettad = kettad.split('\000')[:-1]
def lisa_kettad(list = []):
    for i in kettad:
        list.append(i)
    return list

#Popup otsingu jaoks
def popup(sõnum):
    layout = [[sg.Text(sõnum)]]
    window = sg.Window('Sõnum', layout, no_titlebar=True, keep_on_top=True, finalize=True)
    return window

#Kausta minemine
def kaust(faili_asukoht):
    #Faili vaade
    Failide_tulp = [
        [
            sg.Text("Kaust: "),
            #faili_asukoht here
            sg.Input(default_text = faili_asukoht, size=(25, 1), enable_events=True, key="-KAUST-"),
            sg.Button("Lemmik", enable_events = True, size = (6,1), key = "-LEMMIK-"),
            sg.FolderBrowse(),
            sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"),
        ],
        [
            sg.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-NIMEKIRI-"
            )
        ],
    ]

    Failide_valiku_tulp = [
        [sg.Text("Vali fail nimekirjast:")],
        [sg.Text(size=(40, 1), key="-TOUT-")],
    ]

    layout = [
        [
            sg.Column(Failide_tulp),
            sg.VSeperator(),
            sg.Column(Failide_valiku_tulp),
        ]
    ]

    window = sg.Window("Kausta sisu", layout, finalize = True)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-OK-":
            kaust = values["-KAUST-"]
            try:
                failide_nimekiri = os.listdir(kaust)
            except:
                failide_nimekiri = []

            fnames = [
                f
                for f in failide_nimekiri
                if os.path.isfile(os.path.join(kaust, f))
            ]
            window["-NIMEKIRI-"].update(fnames)
        #Vajutatakse "lemmik" nuppu
        if event == "-LEMMIK-":
            with open("lemmikud.txt", "a") as lemmikud:
                    lemmikud.write(faili_asukoht + '\n')
            sg.popup("Lisati lemmikutesse")
        # Fail valiti nimekirjast
        if event == "-NIMEKIRI-":  
            faili_nimi = os.path.join(
                values["-KAUST-"], values["-NIMEKIRI-"][0]
                )
            if Path(faili_nimi).is_file():
                try:
                    with open(faili_nimi, "rt", encoding='utf-8') as f:
                        text = f.read()
                    popup_text(faili_nimi, text)
                except Exception as e:
                    print("Error: ", e)
        
    window.close()

#Faili leidmine
def otsi_fail(faili_nimi, rada):
   tulemus = []
# Walking top-down from the root
   for root, dir, failid in os.walk(rada):
      if faili_nimi in failid:
         tulemus.append(os.path.join(root, faili_nimi))
   return tulemus[0]

#kui avada tekstifail
def popup_text(faili_nimi, text):

    layout = [
        [sg.Multiline(text, size=(80, 25)),],
    ]
    win = sg.Window(faili_nimi, layout, modal=True, finalize=True)

    while True:
        event, values = win.read()
        if event == sg.WINDOW_CLOSED:
            break
    win.close()  

#Kui failis "ajalugu" on rohkem kui 20 asja, siis kustutab algusest esimese ära
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
    faili_asukoht_ajalugu = []
    for rida in ajalugutxt:
        faili_asukoht_ajalugu.append(rida)
        fpath = [
                f
                for f in faili_asukoht_ajalugu
                ]
#Lemmikud failist ridade lugemine
with open("lemmikud.txt", "r+") as lemmikudtxt:
    faili_asukoht_lemmikud = []
    for rida in lemmikudtxt:
        faili_asukoht_lemmikud.append(rida)
        fpath2 = [
                f
                for f in faili_asukoht_lemmikud
                ]

faili_otsimis_menüü = [
        [sg.Text('Mis faili soovid leida: ')],
        [sg.In(size=(40, 20), key = "-INPUT-"), sg.FolderBrowse()],
        [sg.Text('Kust kettalt (Kui kasutad browse, siis võid vahele jätta): ')],
        [sg.Combo(values = lisa_kettad(), default_value = 'C:\\', font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-KOMBO-')],
        [sg.Text('Missugust vastuse formaati soovid: ')],
        [sg.Combo(values = ['top dir', 'bot dir', 'ketas'], default_value = 'top dir', font=('Arial Bold', 14), expand_x=True, enable_events=True,  readonly=False, key='-VASTUS-')],
        [sg.Button("OK", enable_events = True, size = (3, 1), key = "-OK-"), sg.Button("Cancel", enable_events = True, key = "-CANCEL-")]
        ]

#Ajaloo kast
ajalugu = [
    [sg.Text("Ajalugu")],
    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-AJALUGU-")],
]

#Lemmikute kast
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
popup_win = None

if faili_asukoht_ajalugu:
    window["-AJALUGU-"].update(fpath)
if faili_asukoht_lemmikud:
    window["-LEMMIKUD-"].update(fpath2)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit" or event == "-CANCEL-":
        break
    #Kui valitakse ajaloo tulbast fail
    elif event == "-AJALUGU-":
        faili_asukoht = values["-AJALUGU-"][0]
        break
    #Kui valitakse lemmikute tulbast väärtus
    elif event == "-LEMMIKUD-":
        faili_asukoht = values["-LEMMIKUD-"][0]
        break
    #Kui otsitakse faili
    elif event == "-OK-":
        window['-OK-'].update(disabled=True)
        popup_win = popup('Otsin...')
        window.force_focus()
        if values["-VASTUS-"] == 'top dir':
            if os.path.isdir(values["-INPUT-"]):
                faili_asukoht = values["-INPUT-"]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
            else:
                faili_asukoht = otsi_fail(values["-INPUT-"], values["-KOMBO-"])
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
        if values["-VASTUS-"] == 'bot dir':
            if os.path.isdir(values["-INPUT-"]):
                faili_asukoht = values["-INPUT-"].split("/")[0] + "/" + values["-INPUT-"].split("/")[1]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
            else:
                faili_asukoht = otsi_fail(values["-INPUT-"], values["-KOMBO-"]).split("\\")[0] + "\\" + otsi_fail(values["-INPUT-"], values["-KOMBO-"]).split("\\")[1]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
        if values["-VASTUS-"] == 'ketas':
            if os.path.isdir(values["-INPUT-"]):
                faili_asukoht = values["-INPUT-"][0:3]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
            else:
                faili_asukoht = otsi_fail(values["-INPUT-"], values["-KOMBO-"])[0:3]
                with open("ajalugu.txt", "a") as ajalugu:
                    ajalugu.write(faili_asukoht + '\n')
                break
        popup_win.close()
        popup_win = None
        window['-OK-'].update(disabled=False)
window.close()

if popup_win:
    popup_win.close()
window.close()

if os.path.isdir(faili_asukoht):
   kaust(faili_asukoht)
else:
    faili_tulemuste_menüü = [
        [
            sg.Text(f"Sinu fail asub: {faili_asukoht}"),
            sg.Button("Vii sinna", enable_events = True, key = "-VII-"),
        ]
    ]

    window = sg.Window("Faili asukoht", faili_tulemuste_menüü, finalize = True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit" or event == "-CANCEL-":
            break
        elif event == "-VII-":
            kaust(faili_asukoht[0:faili_asukoht.rfind("\\")])
            break
            
    window.close()
