import tkinter as tk
from tkinter import ttk

class InterfaceAnakKost:
    def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller
        
        self.root.title("Sistem Rekomendasi Makanan Anak Kost Unila")
        self.root.geometry("1000x680")

        self.tab_control = ttk.Notebook(root)
        self.tab_admin = ttk.Frame(self.tab_control)
        self.tab_user = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_admin, text='Admin')
        self.tab_control.add(self.tab_user, text='Menu Anak Kost')
        self.tab_control.pack(expand=1, fill="both")

        self.bangun_layout_admin()
        self.bangun_layout_user()
