import customtkinter
from threading import Thread
from PIL import Image, ImageTk
from winsound import SND_FILENAME, PlaySound, SND_ALIAS
import tkinter as tk


class MessageBox(customtkinter.CTkToplevel):
    def __init__(self, title, message, option=None):
        if option == 'error':

            sound_thread = Thread(target=lambda: PlaySound(
                'Sounds/cuckoo_clock.wav', SND_FILENAME))
        else:
            sound_thread = Thread(target=lambda: PlaySound(
                "SystemExclamation", SND_ALIAS))

        sound_thread.start()

        super().__init__()
        self.color = "floral white"
        if customtkinter.get_appearance_mode() == 'Light':
            self.color = 'floral white'
        elif customtkinter.get_appearance_mode() == 'Dark':
            self.color = 'gray12'
        self.configure(fg_color=self.color)
        self.title(title)
        frame1 = customtkinter.CTkFrame(self, fg_color=self.color)
        frame1.pack(fill='both', expand=True, side='top')

        frame2 = customtkinter.CTkFrame(self, fg_color=self.color)
        frame2.pack(fill='both', expand=True, side='bottom')

        self.resizable(False, False)

        self.iconbitmap("images/cuckoo.ico")

        if option == 'success':
            icon = Image.open("images/success2.png")
            icon = icon.resize((105, 105), Image.LANCZOS)

        if option == 'error':
            icon = Image.open("images/cuckoo_funny.png")
            icon = icon.resize((140, 140), Image.LANCZOS)

            icon = icon.transpose(Image.FLIP_LEFT_RIGHT)

        icon = ImageTk.PhotoImage(icon)
        icon_label = tk.Label(frame1, image=icon,
                              bg=self.color)
        icon_label.image = icon

        icon_label.pack(side='left', padx=10, pady=10,
                        expand='false', fill='none', anchor='center')

        message_label = customtkinter.CTkLabel(
            frame1, text=message, font=('Bahnschrift SemiLight', 20), wraplength=500, bg_color=self.color)
        message_label.pack(side='left', padx=10, pady=15,
                           anchor='center')

        ok_button = customtkinter.CTkButton(frame2, text="OK", font=(
            'Bahnschrift SemiLight', 16), width=130, height=60, command=self.destroy)
        ok_button.pack(padx=10, pady=15, anchor='center')

        self.bind('<Return>', lambda event: self.destroy())
        self.grab_set()

        message_label.update_idletasks()
        label_height = message_label.winfo_reqheight()
        label_width = message_label.winfo_reqwidth()
        window_width = 450 + (label_width-250)
        window_height = 280 + (label_height-40)
        x_coord = (self.winfo_screenwidth()/2) - (window_width/2)
        y_coord = (self.winfo_screenheight()/2) - (window_height/2)
        self.geometry("%dx%d+%d+%d" %
                      (window_width, window_height, x_coord, y_coord))
        if option == 'success':
            self.after(400, lambda: self.destroy())
        self.wait_window()
