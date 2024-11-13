import pandas as pd
import numpy as np
import requests
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
import datasource
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Stock Analysis")
        #==========STYLE===========
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        style.configure('All.TButton',font=('Helvetica',14))
        #==========END style============
        
        #===========RightFrame=============
        rightFrame= ttk.Frame(self,borderwidth=2,relief='groove')

        #添加圖表
        # figure = plt.Figure(figsize =(5,4),dpi=100)
        # ax = figure.add_subplot(111)
        # ax.plot([1,2,3,4,5],[10,20,30,45])
        # ax.set_title('股票分析')

        # canvas = FigureCanvasTkAgg(figure,rightFrame)
        # canvas.get_tk_widget().pack(fill='both',expand=True)
        
        rightFrame.pack(side='right',fill='both',expand=True,padx=10,pady=10)
        #=========RightFrame END===========

        
        #===========leftFrame=============
        leftFrame = ttk.Frame(self)

                #==TOPFRAME=====
        topFrame = ttk.Frame(leftFrame)
        ttk.Label(topFrame,text='台積電股票預測',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(pady=10)
        ttk.Button(topFrame,text='refresh').pack(anchor='e',pady=5)
        ttk.Label(topFrame,text=' 起始數據: 2020-01-01',style='TopFrame.TLabel',borderwidth=2,relief='groove').pack(ipadx=5,pady=10)
        topFrame.pack(fill='x')
                #==TOPFRAME END=====
           #=== 分析方法===
        analysisFrame = ttk.Frame(leftFrame)
        linear_btn = ttk.Button(analysisFrame,text='線性回歸分析',style='All.TButton')
        linear_btn.grid(row=0,column=0,padx=5,pady=5)
        linear_btn = ttk.Button(analysisFrame,text='RSI',style='All.TButton')
        linear_btn.grid(row=0,column=1,padx=5,pady=5)
        linear_btn = ttk.Button(analysisFrame,text='MACD',style='All.TButton')
        linear_btn.grid(row=1,column=0,padx=5,pady=5)
        linear_btn = ttk.Button(analysisFrame,text='MA',style='All.TButton')
        linear_btn.grid(row=1,column=1,padx=5,pady=5)

        analysisFrame.pack(fill='x',pady=10)

           #=== 分析方法end===
            #===預測分析=====
        resultFrame = ttk.Frame(leftFrame)
        ttk.Label(resultFrame,text='預測分析',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid()
        ttk.Label(resultFrame,text='明日股價',borderwidth=2,relief='groove',style='TopFrame.TLabel').grid(row=0,column=0,padx=5,pady=5)
        result_entry = ttk.Entry(resultFrame)
        
        result_entry.grid(row=0,column=1,padx=15,pady=5)
        resultFrame.pack(fill='x', pady=10)
                #=== 預測分析 end===

           


        leftFrame.pack(side='left',fill='y',padx=10,pady=10)


        #=========leftFrame END===========


        #=========bottomFrame ===========
       
        #=========bottomFrame END===========








def main():
    window= Window(theme='arc')
    window.mainloop()


if __name__ == '__main__':
    main()

