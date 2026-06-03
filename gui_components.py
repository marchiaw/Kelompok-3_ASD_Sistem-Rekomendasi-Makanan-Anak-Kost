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
        
   def bangun_layout_admin(self):
        frame_input = tk.LabelFrame(self.tab_admin, text=" Kelola Data Makanan ")
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Nama Makanan:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_nama = tk.Entry(frame_input, width=25); self.ent_nama.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Harga (Rp):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_harga = tk.Entry(frame_input, width=25); self.ent_harga.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Warung:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_warung = tk.Entry(frame_input, width=25); self.ent_warung.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Lokasi:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_lokasi = tk.Entry(frame_input, width=25); self.ent_lokasi.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="Rating (1-5):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_rating = tk.Entry(frame_input, width=25); self.ent_rating.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_input, text="Kategori:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.ent_kategori = ttk.Combobox(frame_input, values=["Makanan", "Minuman", "Jajanan"], width=22, state="readonly")
        self.ent_kategori.grid(row=2, column=3, padx=5, pady=5)
        self.ent_kategori.set("Makanan")
 
