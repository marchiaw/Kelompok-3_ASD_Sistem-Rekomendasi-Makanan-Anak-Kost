import tkinter as tk
from tkinter import messagebox
import math

# PROSES CROSS-IMPORT MODULAR SELURUH BERKAS SECARA BERSIH
from models import WarungMakan
from structures import QueueHistoryLinkedList, StackFavoriteLinkedList, BSTHarga
from algorithms import binary_search_warung, merge_sort_rating
from gui_components import InterfaceAnakKost
import database

class AplikasiRekomendasiAnakKost:
    def __init__(self, root):
        self.riwayat_cari = QueueHistoryLinkedList()  
        self.daftar_favorit = StackFavoriteLinkedList() 
        self.objek_terpilih = None 

# Load database lokaL
        self.database_warung = database.load_semua_state(self.riwayat_cari, self.daftar_favorit)
      
# Hubungkan core logic dengan view GUI
        self.ui = InterfaceAnakKost(root, self)

        self.hitung_statistik()
        self.refresh_tabel_admin(self.database_warung)
        self.tampilkan_di_list_user(self.database_warung)

    def trigger_sinkronisasi(self):
        database.simpan_semua_state(self.database_warung, self.daftar_favorit, self.riwayat_cari)

    def hitung_statistik(self):
        if not self.database_warung:
            self.ui.lbl_total_menu.config(text="Total Menu : 0")
            self.ui.lbl_rata_harga.config(text="Harga Rata-rata : Rp0")
            self.ui.lbl_rata_rating.config(text="Rating Rata-rata : 0.0")
            self.ui.lbl_menu_terbaik.config(text="Menu Terbaik : -")
            return

        total_menu = len(self.database_warung)
        total_harga = sum(item.harga for item in self.database_warung)
        total_rating = sum(item.rating for item in self.database_warung)

        rata_harga = total_harga / total_menu
        rata_rating = total_rating / total_menu

        terbaik = self.database_warung[0]
        for item in self.database_warung:
            if item.rating > terbaik.rating:
                terbaik = item
            elif item.rating == terbaik.rating:
                if item.harga < terbaik.harga:
                    terbaik = item

        self.ui.lbl_total_menu.config(text=f"Total Menu : {total_menu}")
        self.ui.lbl_rata_harga.config(text=f"Harga Rata-rata : Rp {rata_harga:,.0f}")
        self.ui.lbl_rata_rating.config(text=f"Rating Rata-rata : {rata_rating:.1f}")
        self.ui.lbl_menu_terbaik.config(text=f"Menu Terbaik : {terbaik.nama} ({terbaik.nama_warung})")
