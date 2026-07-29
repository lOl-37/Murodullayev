import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import os

# Ovozni aniqlash funksiyasi (bizning asosiy mantiq)
def sirena_aniqla(audio_fayl_yo_li):
    try:
        y, sr = librosa.load(audio_fayl_yo_li, sr=None)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        tsiklik_o_zgarish = np.std(spectral_centroids)
        return tsiklik_o_zgarish
    except Exception as e:
        return None

# Tugma bosilganda faylni tanlash va tahlil qilish funksiyasi
def fayl_tanlash_va_tahlil():
    # Kompyuterdan audio faylni tanlash oynasini ochish
    fayl_yo_li = filedialog.askopenfilename(
        title="Audio faylni tanlang",
        filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.flac")]
    )
    
    if not fayl_yo_li:
        return  # Agar fayl tanlanmasa, funksiyadan chiqish
        
    fayl_nomi_label.config(text=f"Tanlangan fayl: {os.path.basename(fayl_yo_li)}")
    natija_label.config(text="Tahlil qilinmoqda, kuting...", fg="blue")
    oyna.update() # Oynani yangilab turish
    
    # Tahlilni boshlash
    qiymat = sirena_aniqla(fayl_yo_li)
    
    if qiymat is None:
        natija_label.config(text="Xato: Audio faylni o'qib bo'lmadi!", fg="red")
        return
        
    SIRENA_LIMITI = 300 # O'zingiz moslashtirgan chegara qiymat
    
    # Natijani ekranga chiqarish
    tahlil_matni = f"Chastota tebranishi: {qiymat:.2f}\n\n"
    if qiymat > SIRENA_LIMITI:
        tahlil_matni += "⚠️ DIQQAT: Noqonuniy sirena ovozi aniqlandi!"
        natija_label.config(text=tahlil_matni, fg="red")
        messagebox.showwarning("Ogohlantirish", "Noqonuniy sirena ovozi aniqlandi!")
    else:
        tahlil_matni += "✅ Tinchlik: Bu oddiy avtomobil signali yoki shovqin."
        natija_label.config(text=tahlil_matni, fg="green")
        messagebox.showinfo("Natija", "Tinchlik. Muammo aniqlanmadi.")

# --- GRAFIK OYNA QISMI (UI) ---
oyna = tk.Tk()
oyna.title("Sirena Detektor Ilovasi")
oyna.geometry("450x350")
oyna.configure(bg="#f0f0f0")

# Sarlavha
sarlavha = tk.Label(oyna, text="Ovozli Sirena Analizatori", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
sarlavha.pack(pady=20)

# Yo'riqnoma matni
fayl_nomi_label = tk.Label(oyna, text="Hali fayl tanlanmadi", font=("Arial", 10, "italic"), bg="#f0f0f0", fg="#666")
fayl_nomi_label.pack(pady=10)

# Fayl yuklash tugmasi
yuklash_tugmasi = tk.Button(
    oyna, 
    text="Audio Fayl Yuklash", 
    command=fayl_tanlash_va_tahlil, 
    font=("Arial", 11, "bold"), 
    bg="#4CAF50", 
    fg="white", 
    padx=10, 
    pady=5,
    activebackground="#45a049"
)
yuklash_tugmasi.pack(pady=15)

# Natija chiqadigan joy
natija_label = tk.Label(oyna, text="", font=("Arial", 11, "bold"), bg="#f0f0f0", justify="center")
natija_label.pack(pady=20)

# Oynani doimiy yoqib qo'yish
oyna.mainloop()