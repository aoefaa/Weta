import tkinter as tk
from tkinter import *
import tkinter.font as font
import requests
from bs4 import BeautifulSoup as bs
import json
from bmkg.wilayah import Wilayah
from bmkg.req import simple_get

class UI:
    fnStyle = 'Amiko'
    fnButton = f"{fnStyle} 12 bold"
    fnBody = f"{fnStyle} 12" # Hari, alamat, dan awan
    fnTanggal = f"{fnStyle} 14"
    fnCelcius = f"{fnStyle} 30 bold"
    fnJam = f"{fnStyle} 24 bold"
    fnAlamat = f"{fnStyle} 10"

class Weta(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        # Label Provinsi
        self.txProvinsi = Label(root,
                                text = 'Provinsi :',
                                font = UI.fnBody)
        self.txProvinsi.place(x = 80,
                            y = 155)

        # Entry Provinsi
        self.inpProvinsi = Entry(root,
                                width = 22,
                                font = UI.fnBody)
        self.inpProvinsi.place(x = 80,
                            y = 180)

        # Label Kabupaten
        self.txKabupaten = Label(root,
                                text = 'Kabupaten/Kota :',
                                font = UI.fnBody)
        self.txKabupaten.place(x = 80,
                            y = 255)

        # Entry Kabupaten
        self.inpKabupaten = Entry(root, 
                                text = 'Kabupaten/Kota',
                                width = 22,
                                font = UI.fnBody)
        self.inpKabupaten.place(x = 80,
                            y = 280)

        # Button Start
        self.btStart = Button(root, 
                            text = 'S T A R T',
                            width = 10,
                            command = self.proses,
                            font = UI.fnButton,
                            height = 2)
        self.btStart.place(x = 127,
                        y = 330)

        # Tanggal
        self.txTanggal = Label(root,
                                text = '19 Januari 2020',
                                font = UI.fnTanggal)
        self.txTanggal.place(x = 370,
                        y = 142)

        # Hari
        self.txHari = Label(root,
                            text = 'Selasa',
                            font = UI.fnBody)
        self.txHari.place(x = 370,
                        y = 167)

        # Jam
        self.txJam = Label(root,
                            text = '19:00',
                            font = UI.fnJam)
        self.txJam.place(x = 540,
                        y = 150)

        # Celcius
        self.txCelcius = Label(root,
                                text = '27',
                                font = UI.fnCelcius)
        self.txCelcius.place(x = 400,
                        y = 210)

        # Awan
        self.txAwan = Label(root,
                            text = 'Berawan',
                            font = UI.fnBody)
        self.txAwan.place(x = 450,
                        y = 370)

        # Alamat
        self.txAlamat = Label(root,
                                text = 'Hulu Sungai Tengah, Kalimantan Selatan',
                                font = UI.fnAlamat)
        self.txAlamat.place(x = 475,
                        y = 420,
                        anchor = CENTER)
        
        self.btReset = Button(root, 
                            text = 'R E S E T',
                            width = 10,
                            font = UI.fnButton,
                            height = 2)
        self.btReset.place(x = 440,
                        y = 500)
    def proses(self):
        valProvinsi = self.inpProvinsi.get()
        valKabupaten = self.inpKabupaten.get()

        provinsi = []
        kabupaten = []
        results = []

        wil = Wilayah()
        provList = wil.get_provinsi()
        kabList = wil.get_kabupaten()

        for i in provList:
            if i['name'] == valProvinsi:
                provinsi.append(i)

        for i in kabList:
            if i['name'] == valKabupaten:
                kabupaten.append(i)

        namaKab = kabupaten[0]['name']
        namaProv = provinsi[0]['name']
        urlKab = kabupaten[0]['url']
        
        raw_html = simple_get(urlKab)
        html = bs(raw_html, 'html.parser')
        kab = html.find('div', {'class': 'prakicu-kabkota'})

        for li in kab.ul.findAll('li'):
            by_id = kab.find('div', {'id': li.a['href'].replace('#', '')})
            for kota in by_id.findAll('div', {'class': 'prakicu-kota'}):

                kiri = kota.find('div', {'class': 'kiri'})
                cuaca = kiri.p.text
                kanan = kota.find('div', {'class': 'kanan'})
                suhu = kanan.h2.text
                p = kanan.findAll('p')
                p_atas = p[0] if len(p) >= 2 else None

                for i in p_atas.findAll('i'):
                    i.replaceWith(" ")

                p_atas = str(u''.join(p_atas.text).encode('utf-8').strip()).split(' ')

                p_bawah = p[1] if len(p) >= 2 else None
                p_bawah.br.replaceWith("-")
                for i in p_bawah.findAll('i'):
                    i.replaceWith(" ")

                p_bawah = str(u''.join(p_bawah.text).encode('utf-8').strip()).split('-')

                results.append({
                    "cuaca": cuaca,
                    "suhu": suhu,
                })

        cuacaKab = results[0]['cuaca']
        suhuKab = results[0]['suhu']

        valAlamat = namaKab + ', ' + namaProv

        self.txAlamat.configure(text = valAlamat)
        self.txCelcius.configure(text = suhuKab)
        self.txAwan.configure(text = cuacaKab)
            
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Kalkulator BMI Sederhana')
    Weta(root)
    root.geometry("700x600")
    root.mainloop()