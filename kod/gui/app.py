import customtkinter
from . import parameters as param


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title = param.TITLE
        self.geometry(f"{param.WINDOW_WIDTH}x{param.WINDOW_HEIGHT}")
        
        
        