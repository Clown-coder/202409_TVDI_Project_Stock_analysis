import pandas as pd
import numpy as np
import requests
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import outsources
import datasource
import mplfinance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Stock Analysis")
        self.geometry('1800x600')
        
        #==========STYLE===========
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        style.configure('All.TButton',font=('Helvetica',14))
        #==========END style============
        
        #===========RightFrame=============
        self.rightFrame= ttk.Frame(self,borderwidth=2,relief='groove',width=1200, height=600)

        #===========canvas area=============
        self.canvas_area = tk.Canvas(self.rightFrame,width=1200, height=600, bg="white")
        
        self.current = self.add_image(self.rightFrame,'stock.jpg')
    
        self.canvas_area.pack()
         #===========end canvas area=============
        self.rightFrame.pack(side='right',padx=10,pady=10)
        #=========RightFrame END===========

        
        #===========leftFrame=============
        self.leftFrame = ttk.Frame(self)

                #==TOPFRAME=====
        self.topFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.topFrame,text='台積電股票預測',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(pady=10)
        self.icon_button = outsources.ImageButton(self.topFrame,command=lambda: (print('clicked'), datasource.download_data())[1])
        self.icon_button.pack(pady=7,side='right',padx=5)
        ttk.Label(self.topFrame,text=' 起始數據: 2020-01-01',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(ipadx=5,pady=10)
        self.topFrame.pack(fill='x')
                #==TOPFRAME END=====
           #=== 分析方法===
        self.analysisFrame = ttk.Frame(self.leftFrame)
        self.linear_btn = ttk.Button(self.analysisFrame,text='線性回歸分析',style='All.TButton',command=self.plot_regression)
        self.linear_btn.grid(row=0,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='RSI',style='All.TButton',command=self.plot_rsi)
        self.linear_btn.grid(row=0,column=1,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='MACD',style='All.TButton',command=self.plot_macd)
        self.linear_btn.grid(row=1,column=0,padx=5,pady=5)
        self.linear_btn = ttk.Button(self.analysisFrame,text='MA',style='All.TButton',command=self.plot_sma)
        self.linear_btn.grid(row=1,column=1,padx=5,pady=5)

        self.analysisFrame.pack(fill='x',pady=10)

           #=== 分析方法end===
            #===預測分析=====
        self.resultFrame = ttk.Frame(self.leftFrame)
        ttk.Label(self.resultFrame,text='預測分析',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid()
        ttk.Label(self.resultFrame,text='明日股價',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid(row=0,column=0,padx=5,pady=5)
        self.result_entry = ttk.Entry(self.resultFrame)
        
        self.result_entry.grid(row=0,column=1,padx=15,pady=5)
        self.resultFrame.pack(fill='x', pady=10)
                #=== 預測分析 end===

           


        self.leftFrame.pack(side='left',fill='y',padx=10,pady=10)


        #=========leftFrame END===========



    def add_image(self,frame,image_path):
        
        img = Image.open('stock.jpg')
        resized_img = img.resize((1200, 600), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img)

        img_label = tk.Label(frame,image=photo)
        img_label.image = photo
        img_label.pack()
        
    
    def plot_regression(self):
        fig = datasource.linear_regression()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)

    def plot_rsi(self):
        fig = datasource.rsi()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)
    
    def plot_sma(self):
        fig = datasource.sma()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)

    def plot_macd(self):
        fig = datasource.macd()

        for widget in self.rightFrame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig,master=self.rightFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both',expand=True)







    

def main():
    def on_closing():
        print("Exiting...")
        window.destroy()
        sys.exit()
    window= Window(theme='arc')
    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()
    


if __name__ == '__main__':
    main()

