import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt



sure_txt = filedialog.askopenfile(filetypes=(('text files', 'txt'),))
oncelik_txt = filedialog.askopenfile(filetypes=(('text files', 'txt'),))

is_sayisi = int(input("Is sayisini giriniz: "))
#is_sayisi = 32

c_suresi = int(input("Çevrim süresini veriniz: "))
#c_suresi = 1500*


# sure_text = open("sure.txt", "r")
# oncelik_txt = open("oncelik.txt", "r")

sureler = [satir.rstrip("\n") for satir in sure_txt]
oncelik = [satir.rstrip("\n") for satir in oncelik_txt]


def hesapla(sureler, oncelik):
    sureler = sureler
    oncelik = oncelik
    oncelikler = []
    for i in range(0, len(oncelik)):
        yazi = oncelik[i]
        liste = [int(a) if a.isdigit() else a for a in yazi.split(',')]
        oncelikler.append(liste)

    sureler = list(map(int, sureler))


    pw = []
    for i in range(0, is_sayisi - 1):
        total = 0
        sonrakiler = []

        # ilk elemanın ardıllarının sorgulanması
        for j in range(0, len(oncelikler)):
            if oncelikler[j][0] == i+1:
                if oncelikler[j][0] not in sonrakiler:
                    sonrakiler.append(oncelikler[j][0])
                if oncelikler[j][1] not in sonrakiler:
                    sonrakiler.append(oncelikler[j][1])

        # sonraki elemanların ardıllarının sorgulanması
        sayac = 0
        while sayac < len(sonrakiler):
            sorgu = sonrakiler[sayac]
            for j in range(0, len(oncelikler)):
                if oncelikler[j][0] == sorgu:
                    if oncelikler[j][0] not in sonrakiler:
                        sonrakiler.append(oncelikler[j][0])
                    if oncelikler[j][1] not in sonrakiler:
                        sonrakiler.append(oncelikler[j][1])
            sayac += 1

        # i. elemana ait pw'nin hesaplanması
        for k in range(0, len(sonrakiler)):
            indeks = sonrakiler[k]
            agirlik = sureler[indeks - 1]
            total = total + agirlik

        pw.append(total)
        if i == is_sayisi-2:
            pw.append(sureler[-1])


    istasyon_df = pd.DataFrame({
        "isler": list(range(1, is_sayisi + 1)),
        "pos_weight": pw})

    istasyon_df.sort_values(by=["pos_weight"], ascending=False, inplace=True)
    istasyon_df.reset_index(drop=True, inplace=True)

    isler = list(range(1, is_sayisi + 1))
    oncelik_kontrol = []
    for i in range(1,len(isler)+1):
        oncelik_k = []
        for j in range(0, len(oncelikler)):
            if oncelikler[j][1] == i:
                oncelik_k.append((oncelikler[j][0]))
        oncelik_kontrol.append(oncelik_k)


    istasyonlar = []
    istasyonlar_agirlik = []
    isler_ = []
    while isler != []:
        alt_istasyon = []
        alt_istasyon_agirlik = []
        i = 0
        while len(istasyon_df) != 0:
            if isler == []:
                istasyonlar.append(alt_istasyon)
                break
            a = istasyon_df.iloc[i, 0]
            b = sureler[a-1]

            kontrol = all(deger in isler_ for deger in oncelik_kontrol[a - 1])
            if kontrol == True and (sum(alt_istasyon_agirlik) + b) <= c_suresi:
                alt_istasyon.append(a)
                alt_istasyon_agirlik.append(b)
                isler_.append(a)
                isler.remove(a)
                istasyon_df.drop(i, axis=0, inplace=True)
                istasyon_df.reset_index(drop=True, inplace=True)

            elif kontrol == True and (sum(alt_istasyon_agirlik) + b) > c_suresi:
                kontrol2 = len(alt_istasyon)
                j = 0
                while j < len(istasyon_df) - 1:
                    c = istasyon_df.iloc[j+1, 0]
                    d = sureler[c-1]
                    kontrol = all(deger in isler_ for deger in oncelik_kontrol[c - 1])
                    if kontrol == True and (sum(alt_istasyon_agirlik) + d) < c_suresi:
                        alt_istasyon.append(c)
                        alt_istasyon_agirlik.append(d)
                        isler_.append(c)
                        isler.remove(c)
                        istasyon_df.drop(j+1, axis=0, inplace=True)
                        istasyon_df.reset_index(drop=True, inplace=True)
                        j = j -1
                    if j == len(istasyon_df) - 2:
                        istasyonlar.append(alt_istasyon)
                        alt_istasyon = []
                        istasyonlar_agirlik.append(alt_istasyon_agirlik)
                        alt_istasyon_agirlik = []
                    j += 1
                istasyon_df.reset_index(drop=True, inplace=True)
                if kontrol2 == len(alt_istasyon):
                    istasyonlar.append(alt_istasyon)
                    alt_istasyon = []
                    istasyonlar_agirlik.append(alt_istasyon_agirlik)
                    alt_istasyon_agirlik = []
        istasyonlar.append(alt_istasyon)
        istasyonlar_agirlik.append((alt_istasyon_agirlik))
    c_toplam = []
    for i in range(0, len(istasyonlar)):
        a = sum(istasyonlar_agirlik[i])
        c_toplam.append(a)

    return istasyonlar,istasyonlar_agirlik, c_toplam

istasyonlar, istasyonlar_agirlik, c_toplam= hesapla(sureler, oncelik)

def doluluk_cizdir(c_suresi, c_toplam):
    doluluk_oran = []
    is_istasyonlari = list(range(1, len(c_toplam) + 1))
    for i in range(0, len(c_toplam)):
        doluluk_oran.append(c_toplam[i]/c_suresi)
    plt.bar(is_istasyonlari,doluluk_oran)
    for i in range(len(c_toplam)):
        plt.text(i,c_toplam[i],c_toplam[i])
    plt.show()

def hat_etkinligi(c_suresi, c_toplam):
    total = sum(c_toplam)
    ist_sayisi = len(c_toplam)
    formul = (100*total)/(ist_sayisi*c_suresi)
    return formul

def denge_gecikmesi(c_suresi, c_toplam):
    c_eksi = []
    for i in range(0,len(c_toplam)):
        a = c_suresi - c_toplam[i]
        c_eksi.append(a)
    total = sum(c_eksi)
    ist_sayisi = len(c_toplam)
    formul = (100*total)/(ist_sayisi*c_suresi)
    return formul

def duzgunluk_indeksi(c_suresi, c_toplam):
    c_eksi_kare = []
    for i in range(0,len(c_toplam)):
        a = c_suresi - c_toplam[i]
        a = a*a
        c_eksi_kare.append(a)
    total = sum(c_eksi_kare)
    formul = total**(1/2)
    return formul


hat_etkinlik = hat_etkinligi(c_suresi=c_suresi, c_toplam=c_toplam)
denge_gecikme = denge_gecikmesi(c_suresi=c_suresi, c_toplam=c_toplam)
duzgunluk_indeks = duzgunluk_indeksi(c_suresi=c_suresi, c_toplam=c_toplam)

print("Hat etkinliği: ", hat_etkinlik)
print("Denge gecikmesi: ", denge_gecikme)
print("Düzgünlük indeksi: ", duzgunluk_indeks)

doluluk_cizdir(c_suresi=c_suresi, c_toplam=c_toplam)








