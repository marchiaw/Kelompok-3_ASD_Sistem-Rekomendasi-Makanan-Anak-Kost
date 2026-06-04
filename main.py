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

    def refresh_tabel_admin(self, data_list):
        for i in self.ui.tabel_admin.get_children():
            self.ui.tabel_admin.delete(i)
        for item in data_list:
            self.ui.tabel_admin.insert("", "end", values=(item.nama, item.nama_warung, item.harga, item.rating, item.kategori, item.lokasi))

    def tampilkan_di_list_user(self, daftar):
        for i in self.ui.list_user.get_children():
            self.ui.list_user.delete(i)
        for w in daftar: 
            self.ui.list_user.insert("", "end", values=(w.nama, w.nama_warung, w.harga, w.rating, w.kategori, w.lokasi))

    def reset_tampilan_user(self):
        self.tampilkan_di_list_user(self.database_warung)

    def ambil_data_klik(self, event):
        item_terpilih = self.ui.tabel_admin.focus()
        if item_terpilih:
            val = self.ui.tabel_admin.item(item_terpilih, "values")
            self.ui.ent_nama.delete(0, tk.END); self.ui.ent_nama.insert(0, val[0])
            self.ui.ent_harga.delete(0, tk.END); self.ui.ent_harga.insert(0, val[2])
            self.ui.ent_warung.delete(0, tk.END); self.ui.ent_warung.insert(0, val[1])
            self.ui.ent_lokasi.delete(0, tk.END); self.ui.ent_lokasi.insert(0, val[5])
            self.ui.ent_rating.delete(0, tk.END); self.ui.ent_rating.insert(0, val[3])
            self.ui.ent_kategori.set(val[4])
            
            for warung in self.database_warung:
                if warung.nama == val[0] and warung.nama_warung == val[1]:
                    self.objek_terpilih = warung
                    break

    def crud_create(self):
        try:
            nama = self.ui.ent_nama.get().strip()
            harga_str = self.ui.ent_harga.get().strip()
            warung = self.ui.ent_warung.get().strip()
            lokasi = self.ui.ent_lokasi.get().strip()
            rating_str = self.ui.ent_rating.get().strip()
            kategori = self.ui.ent_kategori.get()

            if not (nama and harga_str and warung and lokasi and rating_str):
                return messagebox.showwarning("Peringatan", "Mohon isi semua data!")

            harga = int(harga_str)
            rating = float(rating_str)

            if harga <= 0 or rating < 1.0 or rating > 5.0:
                return messagebox.showwarning("Peringatan", "Batas input nominal / skala rating tidak valid!")

            baru = WarungMakan(nama, harga, kategori, warung, lokasi, rating)
            self.database_warung.append(baru)
            
            self.trigger_sinkronisasi()  
            self.refresh_tabel_admin(self.database_warung)
            self.tampilkan_di_list_user(self.database_warung)
            self.hitung_statistik() 
            messagebox.showinfo("Sukses", "Data Berhasil Ditambahkan!")
        except ValueError:
            messagebox.showerror("Error", "Input Harga/Rating harus angka murni!")

    def crud_update(self):
        if not self.objek_terpilih: return messagebox.showwarning("Peringatan", "Pilih data tabel dulu!")
        try:
            nama = self.ui.ent_nama.get().strip()
            warung = self.ui.ent_warung.get().strip()
            harga_str = self.ui.ent_harga.get().strip()
            rating_str = self.ui.ent_rating.get().strip()
            lokasi = self.ui.ent_lokasi.get().strip() 
            kategori = self.ui.ent_kategori.get()

            teks_fav_lama = f"{self.objek_terpilih.nama} ({self.objek_terpilih.nama_warung}) - Rp{self.objek_terpilih.harga}"

            self.objek_terpilih.nama = nama
            self.objek_terpilih.harga = int(harga_str)
            self.objek_terpilih.nama_warung = warung
            self.objek_terpilih.lokasi = lokasi
            self.objek_terpilih.rating = float(rating_str)
            self.objek_terpilih.kategori = kategori

            if self.daftar_favorit.is_exist(teks_fav_lama):
                self.daftar_favorit.remove_item(teks_fav_lama)
                self.daftar_favorit.push(f"{nama} ({warung}) - Rp{harga_str}")

            self.trigger_sinkronisasi()  
            self.refresh_tabel_admin(self.database_warung)
            self.tampilkan_di_list_user(self.database_warung)
            self.hitung_statistik() 
            messagebox.showinfo("Sukses", "Data Berhasil Diperbarui!")
        except ValueError:
            messagebox.showerror("Error", "Gagal konversi angka!")

    def crud_delete(self):
        if not self.objek_terpilih: return messagebox.showwarning("Peringatan", "Pilih data dulu!")
        teks_fav_target = f"{self.objek_terpilih.nama} ({self.objek_terpilih.nama_warung}) - Rp{self.objek_terpilih.harga}"
        self.daftar_favorit.remove_item(teks_fav_target)
        self.database_warung.remove(self.objek_terpilih)
        self.trigger_sinkronisasi()  
        self.refresh_tabel_admin(self.database_warung)
        self.tampilkan_di_list_user(self.database_warung)
        self.hitung_statistik() 
        self.objek_terpilih = None
        messagebox.showinfo("Sukses", "Data Terhapus!")

    def fitur_bst_filter(self):
        pohon_harga = BSTHarga()
        for w in self.database_warung: pohon_harga.insert(w)
        try:
            budget_str = self.ui.ent_budget.get().strip()
            if not budget_str: return messagebox.showwarning("Peringatan", "Masukkan nominal budget!")
            budget = int(budget_str)
            kat_terpilih = self.ui.cmb_kategori_user.get()

            daftar_lolos = pohon_harga.cari_di_bawah_harga(budget)
            daftar_final = [item for item in daftar_lolos if item.kategori.lower() == kat_terpilih.lower()]
            self.tampilkan_di_list_user(daftar_final)
        except ValueError: messagebox.showerror("Error", "Budget harus berupa nominal angka!")

    def fitur_rekomendasi_terbaik(self):
        try:
            budget_str = self.ui.ent_budget.get().strip()
            kat_terpilih = self.ui.cmb_kategori_user.get()
            if not budget_str: return messagebox.showwarning("Sistem", "Isi kolom budget!")
            
            budget = int(budget_str)
            pohon_harga = BSTHarga()
            for w in self.database_warung: pohon_harga.insert(w)
            
            daftar_lolos = pohon_harga.cari_di_bawah_harga(budget)
            daftar_final = [item for item in daftar_lolos if item.kategori.lower() == kat_terpilih.lower()]

            if not daftar_final: return messagebox.showinfo("Sistem", f"Kategori {kat_terpilih} Rp {budget:,} kosong.")

            menu_rekomendasi = daftar_final[0]
            for item in daftar_final:
                if item.rating > menu_rekomendasi.rating: menu_rekomendasi = item
                elif item.rating == menu_rekomendasi.rating and item.harga < menu_rekomendasi.harga: menu_rekomendasi = item

            self.tampilkan_di_list_user(daftar_final)
            pesan = f"REKOMENDASI AUTOMATIC\n\n Menu: {menu_rekomendasi.nama}\nWarung: {menu_rekomendasi.nama_warung}\nHarga: Rp {menu_rekomendasi.harga:,}\nRating: {menu_rekomendasi.rating}"
            messagebox.showinfo("Sukses", pesan)
        except ValueError: messagebox.showerror("Error", "Input nominal salah!")








