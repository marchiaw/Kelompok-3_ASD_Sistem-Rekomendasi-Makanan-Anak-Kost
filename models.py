class Kuliner:
    def __init__(self, nama, harga, kategori):
        self.nama = nama
        self.harga = int(harga)
        self.kategori = kategori

class WarungMakan(Kuliner):
    def __init__(self, nama, harga, kategori, nama_warung, lokasi, rating):
        super().__init__(nama, harga, kategori)
        self.nama_warung = nama_warung
        self.lokasi = lokasi
