import tkinter as tk
from tkinter import ttk

class InterfaceAnakKost:
    def __init__(self, root, app_controller):
        self.root = root
        self.app = app_controller
        
        self.root.title("Sistem Rekomendasi Makanan Anak Kost Unila")
        self.root.geometry("1000x680")

        self.tab_control = ttk.Notebook(root)
        self.tab_admin = ttk.Frame(self.tab_control)
        self.tab_user = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab_admin, text='Admin')
        self.tab_control.add(self.tab_user, text='Menu Anak Kost')
        self.tab_control.pack(expand=1, fill="both")

        self.bangun_layout_admin()
        self.bangun_layout_user()
        
   def bangun_layout_admin(self):
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
        self.ent_kategori = ttk.Combobox(frame_input, values=["Makanan", "Minuman", "Jajanan"], width=22, state="readonly")
        self.ent_kategori.grid(row=2, column=3, padx=5, pady=5)
        self.ent_kategori.set("Makanan")
 
        frame_aksi = tk.Frame(self.tab_admin)
        frame_aksi.pack(pady=5)

        tk.Button(frame_aksi, text="Tambah", command=self.app.crud_create, bg="green", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(frame_aksi, text="Perbarui", command=self.app.crud_update, bg="orange", width=12).pack(side="left", padx=5)
        tk.Button(frame_aksi, text="Hapus", command=self.app.crud_delete, bg="red", fg="white", width=12).pack(side="left", padx=5)

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
        
        self.tabel_admin.bind("<<TreeviewSelect>>", self.app.ambil_data_klik)

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
           def bangun_layout_user(self):
        frame_fitur = tk.LabelFrame(self.tab_user, text=" Fitur Pencarian & Filter ")
        frame_fitur.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_fitur, text="Budget Maks (Rp):").pack(side="left", padx=2)
        self.ent_budget = tk.Entry(frame_fitur, width=12); self.ent_budget.pack(side="left", padx=2)
        
        tk.Label(frame_fitur, text="Kategori:").pack(side="left", padx=5)
        self.cmb_kategori_user = ttk.Combobox(frame_fitur, values=["Makanan", "Minuman", "Jajanan"], width=12, state="readonly")
        self.cmb_kategori_user.pack(side="left", padx=2)
        self.cmb_kategori_user.set("Makanan")

        tk.Button(frame_fitur, text="Filter Budget", command=self.app.fitur_bst_filter, bg="#b3e6ff").pack(side="left", padx=5)
        tk.Button(frame_fitur, text="Rekomendasi Terbaik", command=self.app.fitur_rekomendasi_terbaik, bg="#ff9999", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(frame_fitur, text="Urut Rating", command=self.app.fitur_sort_rating, bg="#ffcc99").pack(side="right", padx=5)

       frame_baris2 = tk.Frame(self.tab_user); frame_baris2.pack(fill="x", padx=10)
        tk.Label(frame_baris2, text="Cari Nama Warung:").pack(side="left", padx=2)
        self.ent_cari_warung = tk.Entry(frame_baris2, width=20); self.ent_cari_warung.pack(side="left", padx=2)
        tk.Button(frame_baris2, text="Cari", command=self.app.fitur_binary_search, bg="#b3ffb3").pack(side="left", padx=5)
        tk.Button(frame_baris2, text="Reset Tampilan", command=self.app.reset_tampilan_user).pack(side="left", padx=5)
        tk.Button(frame_baris2, text="❤️ Tambah Favorit", command=self.app.tambah_ke_favorit, bg="#ffb3d9").pack(side="right", padx=5)

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
        tk.Button(frame_bawah, text="Lihat Riwayat Klik", command=self.app.lihat_riwayat, bg="lightblue").pack(side="right", padx=5)
        tk.Button(frame_bawah, text="⭐ Buka Daftar Favorit", command=self.app.lihat_favorit, bg="#ffe680").pack(side="right", padx=5)
        
        self.list_user.bind("<<TreeviewSelect>>", self.app.catat_riwayat_klik)
