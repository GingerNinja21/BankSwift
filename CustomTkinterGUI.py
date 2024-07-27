import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import messagebox, simpledialog
import random
import string
import file
from PIL import Image, ImageTk
from file import LoginValidation, DataValidation, account_creation
from LoginGUI2_0 import BankingApplicationGUI

logo_gif = "BANKSWIFT.gif"
logo_static = "logo.png"

class App():
    def __init__(self):
        self.app = ctk.CTk()  # Store the app instance as an attribute
        window_width = 800
        window_height = 600

        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.app.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        container = ctk.CTkFrame(self.app)
       
        container.pack(fill="both",pady=200 , padx=400, expand=True)

        ### MAIN FRAME ####
        Main_frame = ctk.CTkFrame(container)
        Main_frame.pack(fill="both", expand=True)  # Use pack to ensure Main_frame takes space

        # Load and resize the image
        self.Main_frame_background_image = Image.open("background.png")
        self.Main_frame_resized_background = self.Main_frame_background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window size
        self.Main_frame_background = CTkImage(self.Main_frame_resized_background)

        # Create and place the label with the background image
        Main_frame_background_photo = ctk.CTkLabel(Main_frame, image=self.Main_frame_background, width=400 , height=400)
        Main_frame_background_photo.place(relx=0, rely=0, anchor="nw")

        # Keep a reference to the image to prevent garbage collection
        Main_frame_background_photo.image = self.Main_frame_background





        ### CREATE ACCOUNT FRAME ###
        Create_account_frame = ctk.CTkFrame(container)

        ### LOGIN FRAME ###
        Login_frame = ctk.CTkFrame(container)

        for frame in (Main_frame , Create_account_frame , Login_frame):
           frame.grid(row=0,column=0 , sticky="nsew")
        
        

        self.show_frame(Main_frame)
    
    def show_frame(self,frame):
        frame.tkraise()

    def run(self):
        self.app.mainloop()

class AnimatedGIF(ctk.CTkLabel):
    def __init__(self, master, gif_path, static_image_path, width, height, delay=100):
        super().__init__(master)
        self.master = master
        self.delay = delay
        self.gif_path = gif_path
        self.gif_path = gif_path
        self.static_image_path = static_image_path
        self.static_image_path=static_image_path
        self.width = width
        self.height = height
        self.frames = []
        self.load_frames()
        self.static_image = self.load_static_image()
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.config(image=self.image)
        self.animate()
        

    def load_frames(self):
        image = ctk.CTkImage(self.gif_path)
        for frame in range(0, image.n_frames):
            image.seek(frame)
            resized_image = image.resize(self.width, self.height,Image.Resampling.LANCZOS)
            frame_image = ctk.CTkImage(resized_image)
            self.frames.append(frame_image)

    def load_static_image(self):
        image = ctk.CTkImage(self.static_image_path)
        image = image.resize((self.width, self.height), Image.Resampling.LANCZOS)
        return ctk.CTkImage(image)

    def animate(self):

        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 2  
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1 
            self.config(image=self.frames[self.current_frame])
            self.after(self.delay, self.animate)
        else:
            self.config(image=self.static_image)


if __name__ == "__main__" :
    app= App()
    app.run()

