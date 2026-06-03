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
