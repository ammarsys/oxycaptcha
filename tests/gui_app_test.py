import tkinter as tk
import requests
import tkinter.font as tkFont

from tkinter import messagebox

from PIL import ImageTk, Image


class App:
    def __init__(self, root):
        root.title("undefined")

        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.root = root

        GLabel_428 = tk.Label(root)
        ft = tkFont.Font(family="Times", size=16)
        GLabel_428["font"] = ft
        GLabel_428["fg"] = "#333333"
        GLabel_428["justify"] = "center"
        GLabel_428["text"] = "This is a GUI to test the captchas from localhost"
        GLabel_428.place(x=120, y=40, width=500, height=95)

        GButton_967 = tk.Button(root)
        GButton_967["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        GButton_967["font"] = ft
        GButton_967["fg"] = "#000000"
        GButton_967["justify"] = "center"
        GButton_967["text"] = "Generate new captcha"
        GButton_967["relief"] = "sunken"
        GButton_967.place(x=60, y=210, width=79, height=36)
        GButton_967["command"] = self.GButton_967_command

        self.GLineEdit_150 = tk.Entry(root)
        self.GLineEdit_150["borderwidth"] = "1px"
        ft = tkFont.Font(family="Times", size=10)
        self.GLineEdit_150["font"] = ft
        self.GLineEdit_150["fg"] = "#333333"
        self.GLineEdit_150["justify"] = "center"
        self.GLineEdit_150["text"] = "solution "
        self.GLineEdit_150.place(x=60, y=260, width=79, height=30)

        GButton_566 = tk.Button(root)
        GButton_566["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        GButton_566["font"] = ft
        GButton_566["fg"] = "#000000"
        GButton_566["justify"] = "center"
        GButton_566["text"] = "Check solution"
        GButton_566.place(x=60, y=310, width=79, height=30)
        GButton_566["command"] = self.GButton_566_command

        self.latest_captcha_data = {}

    def GButton_967_command(self):
        response = requests.get("http://127.0.0.1:5000/api/v5/captcha")
        captcha_data = response.json()
        captcha_url = captcha_data["cdn_url"]

        captcha_image = Image.open(requests.get(captcha_url, stream=True).raw)
        captcha_photo = ImageTk.PhotoImage(captcha_image)
        captcha_label = tk.Label(self.root, image=captcha_photo)
        captcha_label.place(x=250, y=200)

        captcha_label.photo = captcha_photo

        self.latest_captcha_data = captcha_data

    def GButton_566_command(self):
        data = self.GLineEdit_150.get()

        ret = requests.post(
            f"http://127.0.0.1:5000/api/v5/check/{self.latest_captcha_data['solution_id']}?solution={data}"
        )

        messagebox.showinfo("Popup Title", ret.json())


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
