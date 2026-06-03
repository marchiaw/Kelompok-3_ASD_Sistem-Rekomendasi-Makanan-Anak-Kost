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
        
def load_semua_state(riwayat_cari, daftar_favorit):
    database_warung = []
    if os.path.exists(FILE_DB):
        try:
            with open(FILE_DB, "r", encoding="utf-8") as f:
                data_mentah = json.load(f)
                for item in data_mentah:
                    database_warung.append(
                        WarungMakan(item["nama"], item["harga"], item["kategori"], 
                                    item["nama_warung"], item["lokasi"], item["rating"])
                    )
        except json.JSONDecodeError:
            database_warung = suntik_data_default()
    else:
        database_warung = suntik_data_default()
