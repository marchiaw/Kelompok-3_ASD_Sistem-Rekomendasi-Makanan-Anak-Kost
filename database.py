import json
import os
from models import WarungMakan

FILE_DB = "database_makanan.json"  
FILE_FAV = "favorit.json"
FILE_HIST = "riwayat.json"

def simpan_semua_state(database_warung, daftar_favorit, riwayat_cari):
    data_bisa_disimpan = []
    for item in database_warung:
        data_bisa_disimpan.append({
            "nama": item.nama,
            "harga": item.harga,
            "kategori": item.kategori,
            "nama_warung": item.nama_warung,
            "lokasi": item.lokasi,
            "rating": item.rating
        })
