import numpy as np
import skfuzzy as fuzz
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FormatStrFormatter
import mplcursors

# Fungsi untuk menghitung jumlah produksi
def hitung_produksi():
    try:
        minta = int(entry_minta.get())
        sedia = int(entry_sedia.get())

        if not (0 <= minta <= 6000):
            raise ValueError("Permintaan harus antara 0 dan 6000.")
        if not (0 <= sedia <= 700):
            raise ValueError("Persediaan harus antara 0 dan 700.")

        # Keanggotaan fuzzy
        x = []
        x.append(fuzz.interp_membership(permintaan, permintaan_turun, minta))
        x.append(fuzz.interp_membership(permintaan, permintaan_naik, minta))

        y = []
        y.append(fuzz.interp_membership(persediaan, persediaan_sedikit, sedia))
        y.append(fuzz.interp_membership(persediaan, persediaan_banyak, sedia))

        # Rule base
        apred1 = np.fmin(x[1], y[1])
        z1 = (apred1 * 5000) + 2000

        apred2 = np.fmin(x[0], y[0])
        z2 = 7000 - (apred2 * 5000)

        apred3 = np.fmin(x[0], y[1])
        z3 = 7000 - (apred3 * 5000)

        apred4 = np.fmin(x[1], y[0])
        z4 = (apred4 * 5000) + 2000

        # Defuzzifikasi
        z = round((apred1 * z1 + apred2 * z2 + apred3 * z3 + apred4 * z4) / (apred1 + apred2 + apred3 + apred4))

        # Menampilkan hasil
        hasil_label.config(text=f"Perhitungan Produksi: {z}", foreground="green")

        # Menampilkan grafik di GUI
        update_graph(minta, sedia, z)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk memperbarui grafik
def update_graph(minta, sedia, hasil):
    fig.clear()

    # Grafik Permintaan
    ax0 = fig.add_subplot(311)
    line0, = ax0.plot(permintaan, permintaan_turun, 'b', linewidth=1.5, label='Turun')
    line1, = ax0.plot(permintaan, permintaan_naik, 'r', linewidth=1.5, label='Naik')
    ax0.axvline(x=minta, color='g', linestyle='--', label=f'Permintaan: {minta}')
    ax0.set_title('Permintaan')
    ax0.legend(fontsize=6, loc='right', frameon=True)  # Ukuran kecil
    ax0.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))  # Format sumbu X
    ax0.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  # Format sumbu Y

    # Grafik Persediaan
    ax1 = fig.add_subplot(312)
    line2, = ax1.plot(persediaan, persediaan_sedikit, 'b', linewidth=1.5, label='Sedikit')
    line3, = ax1.plot(persediaan, persediaan_banyak, 'r', linewidth=1.5, label='Banyak')
    ax1.axvline(x=sedia, color='g', linestyle='--', label=f'Persediaan: {sedia}')
    ax1.set_title('Persediaan')
    ax1.legend(fontsize=6, loc='right', frameon=True)  # Ukuran kecil
    ax1.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))  # Format sumbu X
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  # Format sumbu Y

    # Grafik Produksi
    ax2 = fig.add_subplot(313)
    line4, = ax2.plot(produksi, produksi_berkurang, 'b', linewidth=1.5, label='Kurang')
    line5, = ax2.plot(produksi, produksi_bertambah, 'r', linewidth=1.5, label='Tambah')
    ax2.axvline(x=hasil, color='g', linestyle='--', label=f'Produksi: {hasil}')
    ax2.set_title('Produksi')
    ax2.legend(fontsize=6, loc='right', frameon=True)  # Ukuran kecil
    ax2.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))  # Format sumbu X
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))  # Format sumbu Y

    # Tambahkan kursor untuk semua garis
    mplcursors.cursor([line0, line1, line2, line3, line4, line5], hover=True)

    # Atur margin antar subplot
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5)

    # Render ulang canvas
    canvas.draw()

# Fungsi membership
permintaan = np.arange(0, 6000, 1)
persediaan = np.arange(0, 700, 1)
produksi = np.arange(0, 9000, 1)

permintaan_turun = fuzz.trapmf(permintaan, [0, 0, 1000, 5000])
permintaan_naik = fuzz.trapmf(permintaan, [1000, 5000, 6000, 6000])

persediaan_sedikit = fuzz.trapmf(persediaan, [0, 0, 100, 600])
persediaan_banyak = fuzz.trapmf(persediaan, [100, 600, 700, 700])

produksi_berkurang = fuzz.trapmf(produksi, [0, 0, 2000, 7000])
produksi_bertambah = fuzz.trapmf(produksi, [2000, 7000, 9000, 9000])

# Membuat GUI Tkinter
root = tk.Tk()
root.title("Sistem Fuzzy Produksi")
root.geometry("800x600")
root.configure(bg="#f8f9fa")

frame_input = tk.Frame(root, bg="#f8f9fa", padx=10, pady=10)
frame_input.pack(side=tk.LEFT, fill="y")

frame_output = tk.Frame(root, bg="#f8f9fa", padx=10, pady=10)
frame_output.pack(side=tk.RIGHT, fill="both", expand=True)

title_label = tk.Label(frame_input, text="Sistem Fuzzy Produksi", font=("Arial", 16, "bold"), bg="#f8f9fa", fg="#343a40")
title_label.pack(pady=10)

tk.Label(frame_input, text="Permintaan (0 - 6000):", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
entry_minta = ttk.Entry(frame_input, width=10, font=("Arial", 12))
entry_minta.pack(pady=5)

tk.Label(frame_input, text="Persediaan (0 - 700):", font=("Arial", 12), bg="#f8f9fa").pack(pady=5)
entry_sedia = ttk.Entry(frame_input, width=10, font=("Arial", 12))
entry_sedia.pack(pady=5)

hitung_button = ttk.Button(frame_input, text="Hitung", command=hitung_produksi)
hitung_button.pack(pady=15)

hasil_label = tk.Label(frame_input, text="Perhitungan Produksi: ", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#343a40")
hasil_label.pack(pady=10)

# Grafik Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_output)
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()
