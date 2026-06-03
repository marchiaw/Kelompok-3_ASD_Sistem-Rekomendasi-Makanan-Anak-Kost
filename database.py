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
   with open(FILE_DB, "w", encoding="utf-8") as f:
        json.dump(data_bisa_disimpan, f, indent=4)

    with open(FILE_FAV, "w", encoding="utf-8") as f:
        json.dump(daftar_favorit.get_all(), f, indent=4)

    with open(FILE_HIST, "w", encoding="utf-8") as f:
        json.dump(riwayat_cari.get_all()[::-1], f, indent=4)
