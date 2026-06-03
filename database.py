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


    if os.path.exists(FILE_FAV):
        try:
            with open(FILE_FAV, "r", encoding="utf-8") as f:
                fav_mentah = json.load(f)
                for item in fav_mentah[::-1]:
                    daftar_favorit.push(item)
        except json.JSONDecodeError:
            pass

    if os.path.exists(FILE_HIST):
        try:
            with open(FILE_HIST, "r", encoding="utf-8") as f:
                hist_mentah = json.load(f)
                for item in hist_mentah:
                    riwayat_cari.add_history_queue(item)
        except json.JSONDecodeError:
            pass
            
    return database_warung
    
def suntik_data_default():
    dummy = [
        WarungMakan("Batagor Kering", 13000, "Jajanan", "Batagor Abah Unila", "Kampung Baru", 4.5),
        WarungMakan("Batagor Kuah", 15000, "Jajanan", "Batagor Abah Unila", "Kampung Baru", 4.5),
        WarungMakan("Ayam Geprek Original + Nasi", 24000, "Makanan", "Geprek Mas Boy", "Gedong Meneng", 4.7),
        WarungMakan("Ayam Geprek Pedas + Nasi", 24000, "Makanan", "Geprek Mas Boy", "Gedong Meneng", 4.7),
        WarungMakan("Nasi Uduk Komplit Telur", 10000, "Makanan", "Nasi Uduk Kampung Baru", "Kampung Baru", 4.4),
        WarungMakan("Paket Pecel Lele Maknyus", 15000, "Makanan", "Pecel Lele Unila", "Gedong Meneng", 4.6),
        WarungMakan("Promo Mie Instan Warmindo", 7000, "Makanan", "Warmindo Unila", "Kampung Baru", 4.3),
        WarungMakan("Nasi Sayur + Tahu Tempe", 8000, "Makanan", "Warung Makan Barokah", "Gedong Meneng", 4.4),
        WarungMakan("Dimsum Ayam Istimewa", 9000, "Jajanan", "Dimsum Unila", "Kampung Baru", 4.6),
        WarungMakan("Nasi Goreng Kambing", 25000, "Makanan", "Nasgor Kedaton", "Kedaton", 4.2),
        WarungMakan("Mie Ayam Karet", 12000, "Makanan", "Mie Ayam Labuhan", "Labuhan Ratu", 2.1),
        WarungMakan("Sate Taichan Goreng", 20000, "Makanan", "Taichan Rajabasa", "Rajabasa", 4.8),
        WarungMakan("Ayam Bakar Taliwang", 27000, "Makanan", "Ayam Bakar Unila", "Kampung Baru", 4.6),
                WarungMakan("Ayam Penyet Sambal Ijo", 18000, "Makanan", "Penyetan Rajabasa", "Rajabasa", 1.5),
        WarungMakan("Es Teh Manis Keliling", 3000, "Minuman", "Teh Solo Kedaton", "Kedaton", 3.5),
        WarungMakan("Seblak Level 5", 14000, "Jajanan", "Seblak Bloom", "Kampung Baru", 4.4),
        WarungMakan("Bakso Aci Garut", 15000, "Jajanan", "Baci Labuhan Ratu", "Labuhan Ratu", 4.4),
        WarungMakan("Burger Crispy Cheese", 20000, "Makanan", "Unila Burger", "Gedong Meneng", 4.5),
        WarungMakan("Bubur Ayam Pagi", 10000, "Makanan", "Bubur Kedaton", "Kedaton", 3.9),
        WarungMakan("Nasi Kuning Pagi", 9000, "Makanan", "Nasi Kuning Ibu", "Kampung Baru", 4.6),
        WarungMakan("Kopi Susu Gula Aren", 18000, "Minuman", "Cafe Labuhan", "Labuhan Ratu", 4.6),
        WarungMakan("Pisang Bakar Keju", 12000, "Jajanan", "Pisang Aroma Unila", "Kampung Baru", 4.5),
        WarungMakan("Nasi Padang Serba 10rb", 10000, "Makanan", "RM Padang Rajabasa", "Rajabasa", 2.8),
        WarungMakan("Thai Tea Green Tea", 11000, "Minuman", "Dum Dum Thai", "Gedong Meneng", 4.6),
        WarungMakan("Pempek Kapal Selam", 15000, "Jajanan", "Pempek Kedaton", "Kedaton", 4.5),
        WarungMakan("Bakso Urat Jumbo", 19000, "Makanan", "Bakso Mas Doel", "Gedong Meneng", 4.7),
        WarungMakan("Roti Bakar Cokelat", 14000, "Jajanan", "Roti Bakar Rajabasa", "Rajabasa", 3.2),
        WarungMakan("Pecel Sayur Madiun", 10000, "Makanan", "Warung Jatim", "Kampung Baru", 4.3),
        WarungMakan("Soto Betawi Daging", 30000, "Makanan", "Soto Kedaton", "Kedaton", 4.7),
        WarungMakan("Susu Murni Hangat", 8000, "Minuman", "Warmindo Unila", "Kampung Baru", 4.3),
        WarungMakan("Jus Mangga Kecut", 10000, "Minuman", "Fresh Labuhan", "Labuhan Ratu", 2.4),
        WarungMakan("Gulai Tunjang Padang", 28000, "Makanan", "RM Minang Jaya", "Gedong Meneng", 4.8),
        WarungMakan("Tahu Sumedang Anget", 5000, "Jajanan", "Tahu Rajabasa", "Rajabasa", 4.1),
        WarungMakan("Roti Bakar Bandung", 16000, "Jajanan", "Roti Bakar Unila", "Kampung Baru", 4.4),
        WarungMakan("Mie Instan + Telur", 10000, "Makanan", "Warkop Kedaton", "Kedaton", 3.0),
        WarungMakan("Juice Mangga Segar", 12000, "Minuman", "Healthy Corner", "Gedong Meneng", 4.5),
        WarungMakan("Gudeg Jogja", 22000, "Makanan", "Gudeg Labuhan Ratu", "Labuhan Ratu", 4.3),
        WarungMakan("Soto Ayam Lamongan", 15000, "Makanan", "Soto Cak Slamet", "Kampung Baru", 4.6),
        WarungMakan("Ceker Mercon", 12000, "Jajanan", "Mercon Rajabasa", "Rajabasa", 2.2),
        WarungMakan("Gado-Gado Spesial", 13000, "Makanan", "Warung Jatim", "Kampung Baru", 4.4),
        WarungMakan("Ayam Bakar Madu", 26000, "Makanan", "Bakar Kedaton", "Kedaton", 4.6),
        WarungMakan("Siomay Ikan", 12000, "Jajanan", "Siomay Labuhan", "Labuhan Ratu", 3.7),
        WarungMakan("Es Buah Segar", 15000, "Minuman", "Es Rajabasa", "Rajabasa", 4.5),
        WarungMakan("Nasi Gila Spesial", 18000, "Makanan", "Nasgil Kedaton", "Kedaton", 2.9),
        WarungMakan("Kebab Besar", 20000, "Jajanan", "Kebab Labuhan", "Labuhan Ratu", 4.1),
        WarungMakan("Pecel Lele Bar-Bar", 15000, "Makanan", "Lele Rajabasa", "Rajabasa", 1.8),
        WarungMakan("Capcay Ayam", 17000, "Makanan", "Chinese Food Kedaton", "Kedaton", 4.4),
        WarungMakan("Seblak Tulang", 13000, "Jajanan", "Seblak Labuhan", "Labuhan Ratu", 3.1),
    ]
    
    data_bisa_disimpan = [{"nama": i.nama, "harga": i.harga, "kategori": i.kategori, "nama_warung": i.nama_warung, "lokasi": i.lokasi, "rating": i.rating} for i in dummy]
    with open(FILE_DB, "w", encoding="utf-8") as f:
        json.dump(data_bisa_disimpan, f, indent=4)
    return dummy
