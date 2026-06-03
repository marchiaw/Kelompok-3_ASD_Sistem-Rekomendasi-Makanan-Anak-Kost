import json
import os
from structures import WarungMakan

FILE_DB = "database_makanan.json"  
FILE_FAV = "favorit.json"
FILE_HIST = "riwayat.json"

def simpan_semua_data(database_warung, daftar_favorit, riwayat_cari):
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

def load_semua_data(riwayat_cari, daftar_favorit):
    database_warung = []

  
    # Load Main DB
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
            database_warung = muat_data_default()
    else:
        database_warung = muat_data_default()

    # Load Favorit
    if os.path.exists(FILE_FAV):
        try:
            with open(FILE_FAV, "r", encoding="utf-8") as f:
                fav_mentah = json.load(f)
                for item in fav_mentah[::-1]:
                    daftar_favorit.push(item)
        except json.JSONDecodeError:
            pass

    # Load Riwayat
    if os.path.exists(FILE_HIST):
        try:
            with open(FILE_HIST, "r", encoding="utf-8") as f:
                hist_mentah = json.load(f)
                for item in hist_mentah:
                    riwayat_cari.add_history_queue(item)
        except json.JSONDecodeError:
            pass
            
    return database_warung

def muat_data_default():
    dummy = [
    WarungMakan("Batagor Kering", 13000, "Jajanan", "Batagor Abah Unila", "Kampung Baru", 4.5),
    WarungMakan("Batagor Kuah", 15000, "Jajanan", "Batagor Abah Unila", "Kampung Baru", 4.5),
    WarungMakan("Ayam Geprek Original + Nasi", 24000, "Ayam", "Geprek Mas Boy", "Gedong Meneng", 4.7),
    WarungMakan("Ayam Geprek Pedas + Nasi", 24000, "Ayam", "Geprek Mas Boy", "Gedong Meneng", 4.7),
    WarungMakan("Nasi Uduk Komplit Telur", 10000, "Nasi", "Nasi Uduk Kampung Baru", "Kampung Baru", 4.4),
    WarungMakan("Paket Pecel Lele Maknyus", 15000, "Penyetan", "Pecel Lele Unila", "Gedong Meneng", 4.6),
    WarungMakan("Promo Mie Instan Warmindo", 7000, "Mie", "Warmindo Unila", "Kampung Baru", 4.3),
    WarungMakan("Nasi Sayur + Tahu Tempe", 8000, "Nasi", "Warung Makan Barokah", "Gedong Meneng", 4.4),
    WarungMakan("Dimsum Ayam Istimewa", 9000, "Cemilan", "Dimsum Unila", "Kampung Baru", 4.6),
    WarungMakan("Nasi Goreng Kambing", 25000, "Nasi", "Nasgor Kedaton", "Kedaton", 4.2),
    WarungMakan("Mie Ayam Karet", 12000, "Mie", "Mie Ayam Labuhan", "Labuhan Ratu", 2.1),
    WarungMakan("Sate Taichan Goreng", 20000, "Sate", "Taichan Rajabasa", "Rajabasa", 4.8),
    WarungMakan("Ayam Bakar Taliwang", 27000, "Ayam", "Ayam Bakar Unila", "Kampung Baru", 4.6),
