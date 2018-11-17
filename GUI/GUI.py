
# coding: utf-8

# In[100]:

import sys
sys.path.append('../')
import pandas as pd
from copy import deepcopy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
import tkinter as tk
from tkinter import font  as tkfont 
from tkinter.ttk import Combobox
from time import sleep
from PIL import Image, ImageTk
from modules.basic import *
import os
import random


# In[101]:

stocks_data = pd.read_csv("../stocks.csv")
stocks_data['Date'] = stocks_data['Date'].astype('datetime64[ns]')
stocks_data = stocks_data.set_index('Date')


# In[102]:

stocks_data_2016 = stocks_data['2016']


# In[103]:

companies = deepcopy(stocks_data_2016.Company)
companies.drop_duplicates(inplace=True)
companies.reset_index(drop=True,inplace=True)


# In[104]:

comp_list = list(companies)


# In[105]:

comp_stocks=pd.read_csv("../datasets/filtered_companies.csv")
comp_stocks['Symbol']=comp_stocks.Symbol.str.lower()


# In[110]:

# data_words = pd.read_csv("../datasets/words_dates_list_cw.csv")
# data_words.drop_duplicates(inplace=True)
# data_words.reset_index(drop=True,inplace=True)
# word_data = deepcopy(data_words.keyword)
# word_data.drop_duplicates(inplace=True)
# word_data.reset_index(drop=True,inplace=True)
# # word_list = sorted(map(str, list(word_data)))
# word_list = list(map(str, list(word_data)))

data_words = pd.read_csv("../datasets/words_dates_list_cw.csv")
data_words.drop_duplicates(inplace=True)
data_words.reset_index(drop=True,inplace=True)
key_count = data_words.groupby(["keyword"], sort=False).count().reset_index()
key_count = key_count.loc[key_count['freq'] >= 3]
word_data = deepcopy(key_count.keyword)
# word_list = sorted(map(str, list(word_data)))
word_list = list(map(str, list(word_data)))


# In[111]:

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


# In[112]:

# Signal extention
def extend_signal(data):
    i = 0
    while(i < len(data) - 1 and pd.isna(data[i])):
        i += 1
    j = 0
    while(i > 0):
        data[i-1] = data[i+j]
        if i+j+2 <= len(data):
            j += 2
        i -= 1
    return data.fillna(0)


# In[115]:

# GUI for stock details
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background='#ffffff')

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        

# screen 1
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        l = tk.Label(self, text="Stock Details of a Company",font='Sans-serif 30 bold',justify=tk.CENTER)
        l.configure(background='#ffffff')
        l.grid(row=0, column=0,columnspan=30,pady=(5,5), padx=(10,10))
        
        self.canvas = tk.Canvas(self, bg="white", height=500, width=900)
        self.canvas.grid(row=1,rowspan=10,padx=40)
        
        self.c1= tk.Canvas(self, bg="white", height=170, width=320)
        self.c1.grid(row=6,column=1,columnspan=5,padx=0, pady=4)
        
        self.c = tk.Canvas(self, bg="white", height=170, width=320)
        self.c.grid(row=8,column=1,columnspan=5,padx=0, pady=5)
                
        self.var = tk.StringVar(self)
        self.var.set(random.choice(comp_list))

        lbl1 = tk.Label(self, text="Company",font='Helvetica 12 bold')
        lbl1.configure(background='#ffffff')
        lbl1.grid(row=2,column=1,padx=0)

        combo = Combobox(self,textvariable=self.var)
        combo['values']= comp_list
        combo.grid(row=2,column=2,padx=20)

        lbl2 = tk.Label(self, text="Keywords",font='Helvetica 12 bold')
        lbl2.configure(background='#ffffff')
        lbl2.grid(row=3,column=1,padx=20)


        sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        global lb
        lb = tk.Listbox(self,selectmode=tk.MULTIPLE, yscrollcommand=sb.set)
        lb.insert(tk.END,*word_list)
        sb.grid(row=4,column=2,sticky=(tk.NS,tk.W))
        sb.config(command=lb.yview)
        lb.grid(row=4,column=1,sticky=tk.E)

        button = tk.Button(self, text="submit",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.select, width = 8)
        button.grid(row=4,column=2)

        w = tk.Label(self, text="Test for Stationarity", font=("Helvetica", 16),justify=tk.LEFT)
        w.configure(background='#ffffff')
        w.grid(row=5,column=2)
        
        gotobtnright = tk.Button(self, text="Go to Dashboard",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageOne"),width=20)
        gotobtnright.grid(row=11,column=0)
        
        
    # graph plot
    def plot(self,company,keys):
        cp = pd.DataFrame(stocks_data_2016[stocks_data_2016.Company==company].Close,columns={'Close'})
        scaled_cp = pd.DataFrame(scaler.fit_transform(cp),columns={'Close'})
        scaled_cp.set_index(cp.index,inplace=True)

        temp = []
        for word in keys:
            word_count_data= data_words[data_words['keyword']==word]
            word_count_data['Date'] = word_count_data['Date'].astype('datetime64[ns]')
            word_count_data= word_count_data.set_index('Date')
            word_count = pd.DataFrame(word_count_data.freq,columns={'freq'})
            
            # Smoothing and signal extension
            result = moving_average(word_count,3)
            ext_result = extend_signal(result.freq)
            ext_result=pd.DataFrame(ext_result,columns={'freq'})
            # Scaling
            scaled_word_count = pd.DataFrame(scaler.fit_transform(ext_result),columns={word})
            scaled_word_count.set_index(word_count.index,inplace=True)
            # Smoothing
            result = moving_average(scaled_word_count,3)
            ext_result = extend_signal(result[word])
            ext_result=pd.DataFrame(ext_result,columns={word})
            temp.append(ext_result)
        print(temp)

        plt.figure(figsize = (10,5))
        plt.plot(scaled_cp,label=company)
        for i,word in zip(temp,keys):
            plt.plot(i,label=word)
        plt.title("company : "+ company,fontsize=20)
        plt.xlabel("Date")
        plt.legend(loc = 4)
        if not os.path.exists("graph_images"):
            os.mkdir("graph_images/")
        PATH = "graph_images/"+company+".jpeg"
        plt.savefig(PATH)
        plt.cla()
        plt.close('all')
        return PATH,cp
    
    
    def select(self):
        def insert_into_entry():
            items = list(map(int, lb.curselection()))
            if items != ():
                selected_item=[lb.get(items[i]) for i in range(len(items))]
                return (selected_item)

        comp = self.var.get()
        keys = insert_into_entry()
        print(comp)
        print(keys)
        path,cp = self.plot(comp,keys)
        self.canvas.delete("all")
        self.c.delete('all')
        self.c1.delete('all')
        # graph
        image = Image.open(path)
        img = ImageTk.PhotoImage(image)
        self.canvas.create_image(450,250, image=img)
        label = tk.Label(image=img)
        label.image = img 
        image.close()

        """# company details
        x = comp_stocks[comp_stocks.Symbol==comp]
        x.reset_index(drop=True,inplace=True)
        if(x.empty):
            self.c.create_text(120,35,fill="Black",font="Times 13 italic bold",
                                text="Company details not found")

        else:
            self.c.create_text(30,15,fill="Black",font="Times 10 bold",
                                text="Name:")

            self.c.create_text(180,15,fill="Black",font="Times 10",
                                text=x.Name[0])

            self.c.create_text(40,40,fill="Black",font="Times 10 bold",
                                text="LastSale:")

            self.c.create_text(105,40,fill="Black",font="Times 10",
                                text=x.LastSale[0])

            self.c.create_text(47,70,fill="Black",font="Times 10 bold",
                                text="MarketCap:")

            self.c.create_text(125,70,fill="Black",font="Times 10",
                                text=x.MarketCap[0])

            self.c.create_text(40,100,fill="Black",font="Times 10 bold",
                                text="IPOyear:")

            self.c.create_text(107,100,fill="Black",font="Times 10",
                                text=x.IPOyear[0])

            self.c.create_text(35,130,fill="Black",font="Times 10 bold",
                                text="Sector:")

            self.c.create_text(112,130,fill="Black",font="Times 10",
                                text=x.Sector[0])
        """        
        # Dickey Fuller test and KPSS test
        df_res = aDickeyFuller(cp.Close)
        kpss_res = kpss_test(cp.Close)

        # dfuller
        self.c1.create_text(58,15,fill="Black",font="Times 10 bold",
                                text="Dickey Fuller Test", justify = "center")
#         self.c1.create_text(115,35,fill="Black",font="Times 10",
#                                 text="ADF Statistics :  " + str(df_res["ADF Statistics"]) )
#         self.c1.create_text(115,55,fill="Black",font="Times 10",
#                                 text="p value :  " + str(df_res["p value"]) )
#         self.c1.create_text(82,75,fill="Black",font="Times 10",
#                                 text="Number of lags used : " + str(df_res["Number of Lags Used"]) )
#         self.c1.create_text(62,95,fill="Black",font="Times 10",
#                                 text="Critical values : ")
#         self.c1.create_text(100,115,fill="Black",font="Times 10",
#                                 text="1% :  " + str(df_res["Critical values"]['1%']))
#         self.c1.create_text(100,135,fill="Black",font="Times 10",
#                                 text="5% :  " + str(df_res["Critical values"]['5%']))
#         self.c1.create_text(100,155,fill="Black",font="Times 10",
#                                 text="10% :  " + str(df_res["Critical values"]['10%']))
        Text = "\n".join(["{0} :{1}".format(key, df_res[key]) for key in df_res if key != "Critical values"])
        for key in df_res["Critical values"]:
            Text += ("\n \t {0} : {1}".format(key, df_res["Critical values"][key]))
        self.c1.create_text(135, 80, fill = "Black", font = "Times 10", text = Text, justify='left')
        
        #kpss
        self.c.create_text(38,15,fill="Black",font="Times 10 bold",
                                text="KPSS Test")
#         self.c.create_text(135,35,fill="Black",font="Times 10",
#                                 text="KPSS Statistics : " + str(kpss_res["KPSS Statistics"]) )
#         self.c.create_text(120,55,fill="Black",font="Times 10",
#                                 text="p value :  " + str(kpss_res["p value"]) )
#         self.c.create_text(98,75,fill="Black",font="Times 10",
#                                 text="Number of lags used : " + str(kpss_res["Number of Lags Used"]) )
#         self.c.create_text(74,95,fill="Black",font="Times 10",
#                                 text="Critical values : ")
#         self.c.create_text(90,115,fill="Black",font="Times 10",
#                                 text="1% :  " + str(kpss_res["Critical values"]['1%']))
#         self.c.create_text(90,135,fill="Black",font="Times 10",
#                                 text="5% :  " + str(kpss_res["Critical values"]['5%']))
#         self.c.create_text(90,155,fill="Black",font="Times 10",
#                                 text="10% :  " + str(kpss_res["Critical values"]['10%']))
        
        Text_kpss = "\n".join(["{0} :{1}".format(key, kpss_res[key]) for key in kpss_res if key != "Critical values"])
        for key in kpss_res["Critical values"]:
            Text_kpss += ("\n \t {0} : {1}".format(key, kpss_res["Critical values"][key]))
        self.c.create_text(135, 80, fill = "Black", font = "Times 10", text = Text_kpss, justify='left')
        


# screen 2        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        gotobtnleft = tk.Button(self, text="<",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("StartPage"),width=5)
        gotobtnleft.grid(row=21,column=0)
        
        gotobtnright = tk.Button(self, text=">",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageTwo"),width=5)
        gotobtnright.grid(row=21,column=1)
        

# screen 3
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()



if __name__ == "__main__":
    window = App()
    window.configure(background='#ffffff')
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.title("Stock Details")
    window.mainloop()


# In[ ]:




# In[ ]:




# In[ ]:



