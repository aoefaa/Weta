import tkinter as tk

class Weta(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (InputPage, ResultPage):
            page_name = F.__name__
            frame = F(parent = container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InputPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class InputPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = '#ffffff')
        self.controller = controller
        controller.geometry('300x400')

        # Spinbox Provinsi
        sbProvinsi = tk.Spinbox(self, 
                                    from_ = 0,
                                    to = 150,
                                    width = 20)
        sbProvinsi.place(x = 50,
                                y = 170)

        # Spinbox Kabupaten
        sbKabupaten = tk.Spinbox(self, 
                                    from_ = 0,
                                    to = 150,
                                    width = 20)
        sbKabupaten.place(x = 50,
                                y = 240)

        def start():
            controller.show_frame('ResultPage')

        btStart = tk.Button(self, 
                            text = 'S T A R T',
                            command = start,
                            width = 10)
        btStart.place(x = 100,
                            y = 310)

class ResultPage(tk.Frame):
    def __init__(self, parent ,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.geometry('600x600')

        # Tanggal
        txTanggal = tk.Label(text = '19 Januari 2020')
        txTanggal.place(x = 80,
                        y = 172)
        
        def reset():
            controller.show_frame('InputPage')

        btReset = tk.Button(self, 
                            text = 'R E S E T',
                            command = reset,
                            width = 10)

        btReset.place(x = 100,
                            y = 310)

if __name__ == "__main__":
    app = Weta()
    app.mainloop()