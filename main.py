import tkinter as tk
from tkinter import ttk, messagebox
import math

from structures import WarungMakan, QueueHistoryLinkedList, StackFavoriteLinkedList, BSTHarga
from algorithms import binary_search_warung, merge_sort_rating
import database

class AplikasiRekomendasiAnakKost:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Rekomendasi Makanan Anak Kost Unila")
        self.root.geometry("1000x680") 

        self.riwayat_cari = QueueHistoryLinkedList()  
        self.daftar_favorit = StackFavoriteLinkedList() 
        self.objek_terpilih = None 

        # Memanggil modul database luar
        self.database_warung = database.load_semua_data(self.riwayat_cari, self.daftar_favorit)

        self.tab_control = ttk.Notebook(root)
        self.tab_admin = ttk.Frame(self.tab_control)
        self.tab_user = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_admin, text='Admin')
        self.tab_control.add(self.tab_user, text='Menu Anak Kost')
        self.tab_control.pack(expand=1, fill="both")

        self.buat_halaman_admin()
        self.buat_halaman_user()
        self.hitung_statistik() 

    def simpan_state(self):
        database.simpan_semua_data(self.database_warung, self.daftar_favorit, self.riwayat_cari)

    def hitung_statistik(self):
        if not self.database_warung:
            self.lbl_total_menu.config(text="Total Menu : 0")
            self.lbl_rata_harga.config(text="Harga Rata-rata : Rp0")
            self.lbl_rata_rating.config(text="Rating Rata-rata : 0.0")
            self.lbl_menu_terbaik.config(text="Menu Terbaik : -")
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

        self.lbl_total_menu.config(text=f"Total Menu : {total_menu}")
        self.lbl_rata_harga.config(text=f"Harga Rata-rata : Rp {rata_harga:,.0f}")
        self.lbl_rata_rating.config(text=f"Rating Rata-rata : {rata_rating:.1f}")
        self.lbl_menu_terbaik.config(text=f"Menu Terbaik : {terbaik.nama} ({terbaik.nama_warung})")

    def buat_halaman_admin(self):
        frame_input = tk.LabelFrame(self.tab_admin, text=" Kelola Data Makanan ")
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Nama Makanan:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_nama = tk.Entry(frame_input, width=25); self.ent_nama.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Harga (Rp):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_harga = tk.Entry(frame_input, width=25); self.ent_harga.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="Nama Warung:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_warung = tk.Entry(frame_input, width=25); self.ent_warung.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Lokasi:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_lokasi = tk.Entry(frame_input, width=25); self.ent_lokasi.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(frame_input, text="Rating (1-5):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ent_rating = tk.Entry(frame_input, width=25); self.ent_rating.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_input, text="Kategori:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.ent_kategori = tk.Entry(frame_input, width=25); self.ent_kategori.grid(row=2, column=3, padx=5, pady=5)

        frame_aksi = tk.Frame(self.tab_admin)
        frame_aksi.pack(pady=5)

        tk.Button(frame_aksi, text="Tambah", command=self.crud_create, bg="green", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(frame_aksi, text="Perbarui", command=self.crud_update, bg="orange", width=12).pack(side="left", padx=5)
        tk.Button(frame_aksi, text="Hapus", command=self.crud_delete, bg="red", fg="white", width=12).pack(side="left", padx=5)

        frame_tabel = tk.Frame(self.tab_admin)
        frame_tabel.pack(fill="both", expand=True, padx=10, pady=5)

        self.tabel_admin = ttk.Treeview(frame_tabel, columns=("Nama", "Warung", "Harga", "Rating", "Kategori", "Lokasi"), show="headings")
        self.tabel_admin.heading("Nama", text="Nama Makanan")
        self.tabel_admin.heading("Warung", text="Nama Warung")
        self.tabel_admin.heading("Harga", text="Harga")
        self.tabel_admin.heading("Rating", text="Rating")
        self.tabel_admin.heading("Kategori", text="Kategori")
        self.tabel_admin.heading("Lokasi", text="Lokasi")
        
        scroll_admin = ttk.Scrollbar(frame_tabel, orient="vertical", command=self.tabel_admin.yview)
        self.tabel_admin.configure(yscrollcommand=scroll_admin.set)
        
        self.tabel_admin.pack(side="left", fill="both", expand=True)
        scroll_admin.pack(side="right", fill="y")
        
        self.tabel_admin.bind("<<TreeviewSelect>>", self.ambil_data_klik)

        frame_stats = tk.LabelFrame(self.tab_admin, text=" Ringkasan Dashboard Data Kuliner ")
        frame_stats.pack(fill="x", padx=10, pady=5)

        self.lbl_total_menu = tk.Label(frame_stats, text="Total Menu : Calculating...", font=("Arial", 10, "bold"))
        self.lbl_total_menu.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.lbl_rata_harga = tk.Label(frame_stats, text="Harga Rata-rata : Calculating...", font=("Arial", 10, "bold"))
        self.lbl_rata_harga.grid(row=0, column=1, padx=20, pady=5, sticky="w")

        self.lbl_rata_rating = tk.Label(frame_stats, text="Rating Rata-rata : Calculating...", font=("Arial", 10, "bold"))
        self.lbl_rata_rating.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.lbl_menu_terbaik = tk.Label(frame_stats, text="Menu Terbaik : Calculating...", font=("Arial", 10, "bold"), fg="darkgreen")
        self.lbl_menu_terbaik.grid(row=1, column=1, padx=20, pady=5, sticky="w")

        self.refresh_tabel_admin(self.database_warung)

    def refresh_tabel_admin(self, data_list):
        for i in self.tabel_admin.get_children():
            self.tabel_admin.delete(i)
        for item in data_list:
            self.tabel_admin.insert("", "end", values=(item.nama, item.nama_warung, item.harga, item.rating, item.kategori, item.lokasi))

    def ambil_data_klik(self, event):
        item_terpilih = self.tabel_admin.focus()
        if item_terpilih:
            val = self.tabel_admin.item(item_terpilih, "values")
            self.ent_nama.delete(0, tk.END); self.ent_nama.insert(0, val[0])
            self.ent_warung.delete(0, tk.END); self.ent_warung.insert(0, val[1])
            self.ent_harga.delete(0, tk.END); self.ent_harga.insert(0, val[2])
            self.ent_rating.delete(0, tk.END); self.ent_rating.insert(0, val[3])
            self.ent_kategori.delete(0, tk.END); self.ent_kategori.insert(0, val[4])
            self.ent_lokasi.delete(0, tk.END); self.ent_lokasi.insert(0, val[5])
            
            for warung in self.database_warung:
                if warung.nama == val[0] and warung.nama_warung == val[1]:
                    self.objek_terpilih = warung
                    break

    def crud_create(self):
        try:
            nama = self.ent_nama.get().strip()
            harga_str = self.ent_harga.get().strip()
            warung = self.ent_warung.get().strip()
            lokasi = self.ent_lokasi.get().strip()
            rating_str = self.ent_rating.get().strip()
            kategori = self.ent_kategori.get().strip()

            if not (nama and harga_str and warung and lokasi and rating_str):
                return messagebox.showwarning("Peringatan", "Mohon isi semua data yang diperlukan!")

            if rating_str.lower() == "nan" or "nan" in rating_str.lower():
                return messagebox.showerror("Pesan Keamanan", "Input Rating dilarang bernilai NaN!")

            harga = int(harga_str)
            rating = float(rating_str)

            if math.isnan(rating):
                return messagebox.showerror("Pesan Keamanan", "Input Rating dilarang bernilai NaN!")

            if harga <= 0:
                return messagebox.showwarning("Peringatan", "Harga makanan tidak boleh minus atau Rp 0!")

            if rating < 1.0 or rating > 5.0:
                return messagebox.showwarning("Peringatan", "Rating harus berada di rentang 1 hingga 5!")

            for item in self.database_warung:
                if item.nama.lower() == nama.lower() and item.nama_warung.lower() == warung.lower():
                    return messagebox.showerror("Data Ganda", f"Menu '{nama}' dari '{warung}' sudah terdaftar!")

            baru = WarungMakan(nama, harga, kategori if kategori else "Umum", warung, lokasi, rating)
            self.database_warung.append(baru)
            
            self.simpan_state()  
            self.refresh_tabel_admin(self.database_warung)
            self.tampilkan_di_list_user(self.database_warung)
            self.hitung_statistik() 
            self.bersihkan_form()
            messagebox.showinfo("Sukses", "Data Berhasil Ditambahkan!")
        except ValueError:
            messagebox.showerror("Error", "Input Harga/Rating harus berupa angka!")

    def crud_update(self):
        if not self.objek_terpilih: 
            return messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
        
        try:
            nama = self.ent_nama.get().strip()
            warung = self.ent_warung.get().strip()
            harga_str = self.ent_harga.get().strip()
            rating_str = self.ent_rating.get().strip()
            lokasi = self.ent_lokasi.get().strip() 

            if not (nama and harga_str and warung and rating_str and lokasi):
                 return messagebox.showwarning("Peringatan", "Kolom data tidak boleh kosong / berisi spasi saja!")

            if rating_str.lower() == "nan" or "nan" in rating_str.lower():
                return messagebox.showerror("Pesan Keamanan", "Input Rating dilarang bernilai NaN!")

            harga = int(harga_str)
            rating = float(rating_str)

            if math.isnan(rating):
                return messagebox.showerror("Pesan Keamanan", "Input Rating dilarang bernilai NaN!")

            if harga <= 0:
                return messagebox.showwarning("Peringatan", "Gagal memperbarui! Harga makanan tidak boleh minus atau Rp 0.")

            if rating < 1.0 or rating > 5.0:
                return messagebox.showwarning("Peringatan", "Rating harus berada di rentang 1 hingga 5!")

            for item in self.database_warung:
                if item != self.objek_terpilih:
                    if item.nama.lower() == nama.lower() and item.nama_warung.lower() == warung.lower():
                        return messagebox.showerror("Data Ganda", "Kombinasi menu sudah ada di data lain.")

            teks_fav_lama = f"{self.objek_terpilih.nama} ({self.objek_terpilih.nama_warung}) - Rp{self.objek_terpilih.harga}"

            self.objek_terpilih.nama = nama
            self.objek_terpilih.harga = harga
            self.objek_terpilih.nama_warung = warung
            self.objek_terpilih.lokasi = lokasi
            self.objek_terpilih.rating = rating
            self.objek_terpilih.kategori = self.ent_kategori.get().strip() if self.ent_kategori.get().strip() else "Umum"

            if self.daftar_favorit.is_exist(teks_fav_lama):
                self.daftar_favorit.remove_item(teks_fav_lama)
                teks_fav_baru = f"{nama} ({warung}) - Rp{harga}"
                self.daftar_favorit.push(teks_fav_baru)

            self.simpan_state()  
            self.refresh_tabel_admin(self.database_warung)
            self.tampilkan_di_list_user(self.database_warung)
            self.hitung_statistik() 
            self.bersihkan_form()
            self.objek_terpilih = None
            messagebox.showinfo("Sukses", "Data Berhasil Diperbarui!")
        except ValueError:
            messagebox.showerror("Error", "Gagal memperbarui, pastikan input angka benar!")

    def crud_delete(self):
        if not self.objek_terpilih: 
            return messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
        
        tanya = messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus '{self.objek_terpilih.nama}'?")
        if not tanya:
            return

        teks_fav_target = f"{self.objek_terpilih.nama} ({self.objek_terpilih.nama_warung}) - Rp{self.objek_terpilih.harga}"
        self.daftar_favorit.remove_item(teks_fav_target)
        
        self.database_warung.remove(self.objek_terpilih)
        
        self.simpan_state()  
        self.refresh_tabel_admin(self.database_warung)
        self.tampilkan_di_list_user(self.database_warung)
        self.hitung_statistik() 
        self.bersihkan_form()
        self.objek_terpilih = None
        messagebox.showinfo("Sukses", "Data Berhasil Dihapus dari Database & Daftar Favorit!")

    def bersihkan_form(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_harga.delete(0, tk.END)
        self.ent_warung.delete(0, tk.END)
        self.ent_lokasi.delete(0, tk.END)
        self.ent_rating.delete(0, tk.END)
        self.ent_kategori.delete(0, tk.END)

    def buat_halaman_user(self):
        frame_fitur = tk.LabelFrame(self.tab_user, text=" Fitur Pencarian & Filter ")
        frame_fitur.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_fitur, text="Budget Maks (Rp):").pack(side="left", padx=2)
        self.ent_budget = tk.Entry(frame_fitur, width=12); self.ent_budget.pack(side="left", padx=2)
        tk.Button(frame_fitur, text="Filter Budget", command=self.fitur_bst_filter, bg="#b3e6ff").pack(side="left", padx=5)

        tk.Button(frame_fitur, text="Rekomendasi Terbaik", command=self.fitur_rekomendasi_terbaik, bg="#ff9999", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(frame_fitur, text="Urut Rating", command=self.fitur_sort_rating, bg="#ffcc99").pack(side="right", padx=5)

        frame_baris2 = tk.Frame(self.tab_user); frame_baris2.pack(fill="x", padx=10)
        tk.Label(frame_baris2, text="Cari Nama Warung:").pack(side="left", padx=2)
        self.ent_cari_warung = tk.Entry(frame_baris2, width=20); self.ent_cari_warung.pack(side="left", padx=2)
        tk.Button(frame_baris2, text="Cari", command=self.fitur_binary_search, bg="#b3ffb3").pack(side="left", padx=5)
        tk.Button(frame_baris2, text="Reset Tampilan", command=lambda: self.tampilkan_di_list_user(self.database_warung)).pack(side="left", padx=5)

        tk.Button(frame_baris2, text="❤️ Tambah Favorit", command=self.tambah_ke_favorit, bg="#ffb3d9").pack(side="right", padx=5)

        frame_tabel_user = tk.Frame(self.tab_user)
        frame_tabel_user.pack(padx=10, pady=10, fill="both", expand=True)

        self.list_user = ttk.Treeview(frame_tabel_user, columns=("Nama", "Warung", "Harga", "Rating", "Kategori", "Lokasi"), show="headings")
        self.list_user.heading("Nama", text="Nama Makanan")
        self.list_user.heading("Warung", text="Nama Warung")
        self.list_user.heading("Harga", text="Harga")
        self.list_user.heading("Rating", text="Rating")
        self.list_user.heading("Kategori", text="Kategori")
        self.list_user.heading("Lokasi", text="Lokasi")
        
        scroll_user = ttk.Scrollbar(frame_tabel_user, orient="vertical", command=self.list_user.yview)
        self.list_user.configure(yscrollcommand=scroll_user.set)

        self.list_user.pack(side="left", fill="both", expand=True)
        scroll_user.pack(side="right", fill="y")

        frame_bawah = tk.Frame(self.tab_user); frame_bawah.pack(fill="x", padx=10, pady=5)
        tk.Button(frame_bawah, text="Lihat Riwayat Klik", command=self.lihat_riwayat, bg="lightblue").pack(side="right", padx=5)
        tk.Button(frame_bawah, text="⭐ Buka Daftar Favorit", command=self.lihat_favorit, bg="#ffe680").pack(side="right", padx=5)
        
        self.list_user.bind("<<TreeviewSelect>>", self.catat_riwayat_klik)
        self.tampilkan_di_list_user(self.database_warung)

    def fitur_bst_filter(self):
        pohon_harga = BSTHarga()
        for w in self.database_warung: pohon_harga.insert(w)
        try:
            budget = int(self.ent_budget.get())
            if budget <= 0:
                return messagebox.showwarning("Peringatan", "Budget filter harus lebih dari Rp 0!")
            self.tampilkan_di_list_user(pohon_harga.cari_di_bawah_harga(budget))
        except ValueError: 
            messagebox.showerror("Error", "Masukkan nominal angka budget!")

    def fitur_rekomendasi_terbaik(self):
        try:
            budget_str = self.ent_budget.get().strip()
            if not budget_str:
                return messagebox.showwarning("Sistem Rekomendasi", "Silakan masukkan nominal budget Anda di kolom 'Budget Maks (Rp)' terlebih dahulu!")
            
            budget = int(budget_str)
            if budget <= 0:
                return messagebox.showwarning("Sistem Rekomendasi", "Nominal budget harus berupa angka positif!")

            pohon_harga = BSTHarga()
            for w in self.database_warung: 
                pohon_harga.insert(w)
            
            daftar_lolos_budget = pohon_harga.cari_di_bawah_harga(budget)

            if not daftar_lolos_budget:
                return messagebox.showinfo("Sistem Rekomendasi", f"Maaf, tidak ada menu makanan yang masuk budget Rp {budget:,} Anda.")

            menu_rekomendasi = daftar_lolos_budget[0]
            for item in daftar_lolos_budget:
                if item.rating > menu_rekomendasi.rating:
                    menu_rekomendasi = item
                elif item.rating == menu_rekomendasi.rating:
                    if item.harga < menu_rekomendasi.harga:
                        menu_rekomendasi = item

            self.tampilkan_di_list_user(daftar_lolos_budget)
            
            pesan_rekomendasi = (
                f"REKOMENDASI MENU TERBAIK ANAK KOST\n\n"
                f"Nama Makanan : {menu_rekomendasi.nama}\n"
                f"Nama Warung : {menu_rekomendasi.nama_warung}\n"
                f"Harga Menu  : Rp {menu_rekomendasi.harga:,}\n"
                f"Rating Toko  : {menu_rekomendasi.rating} / 5.0\n"
                f"Lokasi Toko  : {menu_rekomendasi.lokasi}\n\n"
                f"*Kriteria: Menu yang masuk budget Anda dengan rating tertinggi dan harga paling ekonomis."
            )
            messagebox.showinfo("Rekomendasi Cerdas Otomatis", pesan_rekomendasi)

        except ValueError:
            messagebox.showerror("Error", "Input parameter budget anak kost wajib diisi angka murni!")

    def fitur_sort_rating(self):
        data_copy = list(self.database_warung)
        merge_sort_rating(data_copy)
        self.tampilkan_di_list_user(data_copy)

    def fitur_binary_search(self):
        target = self.ent_cari_warung.get().strip()
        if not target: return messagebox.showwarning("Peringatan", "Masukkan nama warung!")
        
        data_diurutkan = sorted(self.database_warung, key=lambda x: x.nama_warung.lower())
        indeks = binary_search_warung(data_diurutkan, target)
        
        if indeks != -1:
            warung_ketemu = data_diurutkan[indeks].nama_warung.lower()
            self.tampilkan_di_list_user([w for w in self.database_warung if warung_ketemu == w.nama_warung.lower()])
        else: 
            messagebox.showwarning("Tidak Ditemukan", f"Warung '{target}' tidak terdaftar.")

    def catat_riwayat_klik(self, event):
        item_terpilih = self.list_user.focus()
        if item_terpilih: 
            val = self.list_user.item(item_terpilih, "values")
            teks_riwayat = f"[{val[1]}] {val[0]} - Rp{val[2]} | Rating: {val[3]} ({val[4]})"
            riwayat_sekarang = self.riwayat_cari.get_all()
            if riwayat_sekarang and riwayat_sekarang[0] == teks_riwayat:
                return
            self.riwayat_cari.add_history_queue(teks_riwayat)
            self.simpan_state()

    def lihat_riwayat(self):
        riwayat = self.riwayat_cari.get_all()
        teks_box = f"Riwayat Klik Terakhir\n\n"
        if riwayat:
            teks_box += "\n".join([f"{i+1}. {item}" for i, item in enumerate(riwayat)])
        else:
            teks_box += "Belum ada riwayat klik menu."
        messagebox.showinfo("Riwayat Anda", teks_box)

    def tambah_ke_favorit(self):
        item_terpilih = self.list_user.focus()
        if not item_terpilih:
            return messagebox.showwarning("Peringatan", "Pilih menu makanan di tabel dulu untuk dijadikan favorit!")
        
        val = self.list_user.item(item_terpilih, "values")
        teks_fav = f"{val[0]} ({val[1]}) - Rp{val[2]}"

        if self.daftar_favorit.is_exist(teks_fav):
            self.daftar_favorit.remove_item(teks_fav)
            self.simpan_state()
            messagebox.showinfo("Favorit Diubah", f"'{val[0]}' dihapus dari daftar favorit.")
        else:
            self.daftar_favorit.push(teks_fav)
            self.simpan_state()
            messagebox.showinfo("Favorit Ditambahkan", f"'{val[0]}' berhasil masuk daftar favorit!")

    def lihat_favorit(self):
        fav_list = self.daftar_favorit.get_all()
        teks_box = "⭐ DAFTAR MAKANAN FAVORIT ANDA:\n\n"
        if fav_list:
            teks_box += "\n".join([f"📌 {item}" for item in fav_list])
            teks_box += "\n\n*Catatan: Makanan yang paling baru ditambah berada di urutan teratas."
        else:
            teks_box += "Belum ada makanan favorit yang disimpan."
        
        if fav_list:
            opsi_pop = messagebox.askyesno("Daftar Favorit", teks_box + "\n\nApakah Anda ingin menghapus item teratas?")
            if opsi_pop:
                item_terhapus = self.daftar_favorit.pop()
                if item_terhapus:
                    self.simpan_state() 
                    messagebox.showinfo("Stack", f"Berhasil menghapus item teratas: '{item_terhapus}' telah dihapus.")
        else:
            messagebox.showinfo("Daftar Favorit", teks_box)

    def tampilkan_di_list_user(self, daftar):
        for i in self.list_user.get_children():
            self.list_user.delete(i)
        for w in daftar: 
            self.list_user.insert("", "end", values=(w.nama, w.nama_warung, w.harga, w.rating, w.kategori, w.lokasi))

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiRekomendasiAnakKost(root)
    root.mainloop()
