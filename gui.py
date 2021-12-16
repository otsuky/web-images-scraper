import PySimpleGUI as sg

from saveImage import download_images_from_url_list


def make_window():
    sg.theme("DarkAmber")
    layout = [
        [sg.Text("画像取得元 URL:")],
        [sg.Multiline(size=(None, 8), expand_x=True, expand_y=True, key="-URL_LIST-")],
        [sg.Text("出力先フォルダ")],
        [
            sg.In(key="-FOLDER_PATH-"),
            sg.Button("選択", key="-SELECT_FOLDER-"),
        ],
        [sg.Text("Basic 認証")],
        [
            sg.Text("User:"),
            sg.In(size=(20,), expand_x=True, key="-BASIC_USER-"),
        ],
        [
            sg.Text("Pass:"),
            sg.In(size=(20,), expand_x=True, key="-BASIC_PASS-"),
        ],
        [sg.Text("結果:")],
        [sg.Output(size=(None, 20), expand_x=True)],
        [sg.Button("Start", key="-START-"), sg.Button("Close", key="-CLOSE-")],
    ]
    return sg.Window("画像一括保存する太郎", layout, resizable=True, font=(None, 14))


def main():
    window = make_window()

    while True:
        event, values = window.read()

        if event == "-SELECT_FOLDER-":
            folder = sg.PopupGetFolder("出力先フォルダ:", no_titlebar="true", font=(None, 14))
            if folder is None:
                continue
            window["-FOLDER_PATH-"].update(folder)
            window.refresh()

        if event == "-START-":
            err = ""
            if values["-FOLDER_PATH-"] == "":
                err += "・出力先フォルダを入力してください\n"
            if values["-URL_LIST-"] == "":
                err += "・画像取得元 URL を入力してください\n"
            if err == "":
                download_images_from_url_list(
                    values["-URL_LIST-"].splitlines(), values["-FOLDER_PATH-"]
                )
            else:
                sg.popup_error(err.rstrip("\n"), font=(None, 14))

        if event == sg.WIN_CLOSED or event == "-CLOSE-":
            break
    window.close()


main()
