import PySimpleGUI as sg


def make_window():
    sg.theme("DarkAmber")
    layout = [
        [sg.Text("画像を取得する URL")],
        [sg.Multiline(size=(None, 8))],
        [
            sg.Text("出力先フォルダ:"),
            sg.Text("未選択", key="-FOLDERNAME-"),
            sg.Button("選択", key="-SELECT_FOLDER-"),
        ],
        [sg.Button("Start", key="-START-"), sg.Button("Close", key="close")],
    ]

    return sg.Window("画像を一括保存する太郎", layout, size=(400, 200))


def main():
    window = make_window()

    while True:
        event, values = window.read()

        if event == "-SELECT_FOLDER-":
            folder = sg.PopupGetFolder("出力先フォルダ:", no_titlebar="true")
            if folder is None:
                continue
            window["-FOLDERNAME-"].update(folder)
            window.refresh()

        if event == "-START-":
            print(values[0].splitlines())

        if event == sg.WIN_CLOSED or event == "close":
            print("close")
            break

        print("Youentered ", folder, values)

    window.close()
