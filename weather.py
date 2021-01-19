import tkinter as tk
import pyglet, os
import tkinter.font as font

class Weta(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F, geometry in zip((InputPage, ResultPage), ('300x400', '600x600')):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = (frame, geometry)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InputPage")

    def show_frame(self, page_name):
        frame, geometry = self.frames[page_name]
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()

class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#5CDB94')
        self.controller = controller

        # Label Provinsi
        txProvinsi = tk.Label(self,
                                text = 'Provinsi :',
                                font = UI.fnBody)
        txProvinsi.place(x = 50,
                            y = 140)
        # Entry Provinsi
        inpProvinsi = tk.Entry(self,
                                    width = 22,
                                    font = UI.fnBody)
        inpProvinsi.place(x = 50,
                            y = 170)

        # Label Kabupaten
        txKabupaten = tk.Label(self,
                                text = 'Kabupaten/Kota :',
                                font = UI.fnBody)
        txKabupaten.place(x = 50,
                            y = 210)

        # Entry Kabupaten
        inpKabupaten = tk.Entry(self, 
                                    text = 'Kabupaten/Kota',
                                    width = 22,
                                    font = UI.fnBody)
        inpKabupaten.place(x = 50,
                            y = 240)

        def start():
            controller.show_frame('ResultPage')

        btStart = tk.Button(self, 
                            text = 'S T A R T',
                            command = start,
                            width = 10,
                            font = UI.fnButton)
        btStart.place(x = 100,
                            y = 310)

class ResultPage(tk.Frame):
    def __init__(self, parent ,controller):
        tk.Frame.__init__(self, parent, bg = '#5CDB94')
        self.controller = controller
        self.controller.geometry('600x600')

        # Tanggal
        txTanggal = tk.Label(self,
                                text = '19 Januari 2020',
                                font = UI.fnTanggal)
        txTanggal.place(x = 80,
                        y = 170)

        # Hari
        txHari = tk.Label(self,
                            text = 'Selasa',
                            font = UI.fnBody)
        txHari.place(x = 80,
                    y = 200)

        # Jam
        txJam = tk.Label(self,
                            text = '19:00',
                            font = UI.fnJam)
        txJam.place(x = 450,
                        y = 180)

        # Celcius
        txCelcius = tk.Label(self,
                                text = '27',
                                font = UI.fnCelcius)
        txCelcius.place(x = 121,
                        y = 267)

        # Awan
        txAwan = tk.Label(self,
                            text = 'Awan Petir',
                            font = UI.fnBody)
        txAwan.place(x = 128,
                        y = 352)

        # Alamat
        txAlamat = tk.Label(self,
                                text = 'Hulu Sungai Tengah, Kalimantan Selatan',
                                font = UI.fnBody)
        txAlamat.place(x = 168,
                        y = 447)
        
        def reset():
            controller.show_frame('InputPage')

        btReset = tk.Button(self, 
                            text = 'R E S E T',
                            command = reset,
                            width = 10,
                            font = UI.fnButton)

        btReset.place(x = 250,
                        y = 522)
    
class UI:
    fnStyle = 'Amiko'
    fnButton = f"{fnStyle} 12 bold"
    fnBody = f"{fnStyle} 12" # Hari, alamat, dan awan
    fnTanggal = f"{fnStyle} 14"
    fnCelcius = f"{fnStyle} 60 bold"
    fnJam = f"{fnStyle} 24 bold"

class Engine:
    def ()

if __name__ == "__main__":
    app = Weta()
    app.mainloop()