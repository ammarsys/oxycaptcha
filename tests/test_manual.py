from tkinter import Tk, Label, Entry, Button
from typing import Any, Union, TYPE_CHECKING
from io import BytesIO

from PIL import Image
from PIL.ImageTk import PhotoImage

if TYPE_CHECKING:
    from flask import Response


def _check_data(root: Tk, client: Any, captcha_data: dict, attempt: str) -> None:
    response: Union["Response", Any] = client.post(
        captcha_data["solution_check_url"], json={"attempt": attempt}
    )

    if response.json != {
        "case_sensitive_correct": True,
        "case_insensitive_correct": True,
    }:
        root.destroy()
        raise AssertionError("bad solution")
    else:
        root.destroy()


def test_solution(client: Any, captcha_data: dict):
    """Have a human manually solve the captcha"""

    root = Tk()
    root.geometry("400x300")

    res = client.get(captcha_data["cdn_url"])

    captcha_image = Image.open(BytesIO(res.data))
    captcha_photo = PhotoImage(captcha_image)
    captcha_label = Label(root, image=captcha_photo)
    captcha_label.place(x=50, y=50)
    captcha_info_label = Label(root, text="Write what you see", font=24)  # type: ignore
    captcha_info_label.place(x=130, y=180)
    captcha_solution_grid = Entry(root, width=300)
    captcha_solution_grid.place(x=0, y=220)
    captcha_send_button = Button(
        root,
        text="Check",
        width=10,
        command=lambda: _check_data(
            root, client, captcha_data, attempt=captcha_solution_grid.get()
        ),
    )
    captcha_send_button.place(x=150, y=250)

    root.mainloop()
