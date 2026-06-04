class Kuliner:
    def __init__(self, nama, harga, kategori):
        self.nama = nama
        self.harga = int(harga)
        self.kategori = kategori

class WarungMakan(Kuliner):
    def __init__(self, nama, harga, kategori, nama_warung, lokasi, rating):
