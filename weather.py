import tkinter as tk
from tkinter import *
import tkinter.font as font
import requests
from bs4 import BeautifulSoup as bs
import json
from bmkg.wilayah import Wilayah
from bmkg.req import simple_get
import time

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
        
        self.wil = Wilayah()
        self.itemProvinsi = self.wil.get_provinsi()
        self.listKabupaten = []
        self.listProvinsi = []
        for i in self.itemProvinsi:
            self.listProvinsi.append(i['name'])

        # Label Provinsi
        self.txProvinsi = Label(root,
                                text = 'Provinsi :',
                                font = UI.fnBody)
        self.txProvinsi.place(x = 80,
                            y = 155)

        # Entry Kabupaten
        self.inpKabupaten = Spinbox(root,
                                value = ['Cek Kab/kota Provinsi !'],
                                width = 22,
                                font = UI.fnBody)
        self.inpKabupaten.place(x = 80,
                            y = 280)

        # Entry Provinsi
        self.inpProvinsi = Spinbox(root,
                                value = self.listProvinsi,
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

        # Button Get Kabupaten
        self.btGetKabupaten = Button(root,
                                    command = self.getKabupaten,
                                    text = 'Cek')
        self.btGetKabupaten.place(x = 290,
                                    y = 182)

        # Tanggal
        self.txTanggal = Label(root,
                                text = '',
                                font = UI.fnTanggal)
        self.txTanggal.place(x = 370,
                        y = 142)

        # Hari
        self.txHari = Label(root,
                            text = '',
                            font = UI.fnBody)
        self.txHari.place(x = 370,
                        y = 167)

        # Jam
        self.txJam = Label(root,
                            text = '',
                            font = UI.fnJam)
        self.txJam.place(x = 540,
                        y = 150)

        # Celcius
        self.txCelcius = Label(root,
                                text = '',
                                font = UI.fnCelcius)
        self.txCelcius.place(x = 400,
                        y = 210)

        # Awan
        self.txAwan = Label(root,
                            text = '',
                            font = UI.fnBody)
        self.txAwan.place(x = 485,
                            y = 370,
                            anchor = CENTER)

        # Alamat
        self.txAlamat = Label(root,
                                text = '',
                                font = UI.fnAlamat)
        self.txAlamat.place(x = 480,
                        y = 420,
                        anchor = CENTER)

        # Button Start
        self.btStart = Button(root, 
                            text = 'S T A R T',
                            width = 10,
                            command = self.proses,
                            font = UI.fnButton,
                            height = 2)
        self.btStart.place(x = 127,
                        y = 350)
        
        # Button Reset
        self.btReset = Button(root, 
                            text = 'R E S E T',
                            width = 10,
                            command = self.reset,
                            font = UI.fnButton,
                            height = 2)
        self.btReset.place(x = 440,
                        y = 470)

    def getKabupaten(self):
        
        idProv = None

        valProvinsi = self.inpProvinsi.get()
        itemKabupaten = self.wil.get_kabupaten()
        
        for i in self.itemProvinsi:
            self.listProvinsi.append(i['name'])

        for i in self.listProvinsi:
            if i == valProvinsi:
                idProv = str(self.listProvinsi.index(valProvinsi) + 1).zfill(2)

        for i in itemKabupaten:
            if i['prov'] == idProv:
                self.listKabupaten.append(i['name'])

        self.inpKabupaten.configure(value = self.listKabupaten)

    def proses(self):
        self.valProvinsi = self.inpProvinsi.get()
        self.valKabupaten = self.inpKabupaten.get()

        provinsi = []
        kabupaten = []
        results = []

        wil = Wilayah()
        self.itemProvinsi = self.wil.get_provinsi()
        kabList = wil.get_kabupaten()

        for i in self.itemProvinsi:
            if i['name'] == self.valProvinsi:
                provinsi.append(i)

        for i in kabList:
            if i['name'] == self.valKabupaten:
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
        
        jam = time.strftime('%H:%M')
        tanggal = time.strftime('%d %B %Y')
        hari = time.strftime('%A')

        cuacaKab = results[0]['cuaca']
        suhuKab = results[0]['suhu']

        valAlamat = namaKab + ', ' + namaProv

        self.txAlamat.configure(text = valAlamat)
        self.txCelcius.configure(text = suhuKab)
        self.txAwan.configure(text = cuacaKab)
        self.txJam.configure(text = jam)
        self.txTanggal.configure(text = tanggal)
        self.txHari.configure(text = hari)

    def reset(self):
        self.txTanggal.configure(text = '')
        self.txHari.configure(text = '')
        self.txCelcius.configure(text = '')
        self.txJam.configure(text = '')
        self.txAwan.configure(text = '')
        self.txAlamat.configure(text = '')
        self.inpKabupaten.configure(value = ['Cek Kab/kota Provinsi !'])

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Weta')
    Weta(root)
    root.geometry("700x600")
    root.mainloop()