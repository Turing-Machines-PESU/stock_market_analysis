
# coding: utf-8

# In[1]:


import sys
sys.path.append('../')
import pandas as pd
from copy import deepcopy
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import tkinter as tk
from tkinter import font  as tkfont 
from tkinter.ttk import Combobox
from time import sleep
from PIL import Image, ImageTk
from modules.basic import *
import os
import random


# In[2]:


stocks_data = pd.read_csv("../stocks.csv")
stocks_data['Date'] = stocks_data['Date'].astype('datetime64[ns]')
stocks_data = stocks_data.set_index('Date')


# In[8]:


stocks_data_2016 = stocks_data['2016']


# In[9]:


companies = deepcopy(stocks_data_2016.Company)
companies.drop_duplicates(inplace=True)
companies.reset_index(drop=True,inplace=True)


# In[10]:


comp_list = list(companies)


# In[11]:


comp_stocks=pd.read_csv("../datasets/filtered_companies.csv")
comp_stocks['Symbol']=comp_stocks.Symbol.str.lower()


# In[12]:


data_words = pd.read_csv("../datasets/words_dates_list_cw.csv")
data_words.drop_duplicates(inplace=True)
data_words.reset_index(drop=True,inplace=True)
key_count = data_words.groupby(["keyword"], sort=False).count().reset_index()
key_count = key_count.loc[key_count['freq'] >= 3]
word_data = deepcopy(key_count.keyword)
#word_list = sorted(map(str, list(word_data)))
word_list = list(map(str, list(word_data)))


# In[13]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


# In[14]:


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


# In[206]:


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
        self.pages = (StartPage, PageOne, PageTwo)
        for F in self.pages:
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

        subbtn = tk.Button(self, text="submit",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.select, width = 8)
        subbtn.grid(row=4,column=2)

        w = tk.Label(self, text="Test for Stationarity", font=("Helvetica", 16),justify=tk.LEFT)
        w.configure(background='#ffffff')
        w.grid(row=5,column=2)
        
        gotobtnright = tk.Button(self, text="Go to Dashboard",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageOne"),width=20)
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
        #print(temp)

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
                global selected_item
                selected_item=[lb.get(items[i]) for i in range(len(items))]
                return (selected_item)

        comp = self.var.get()
        keys = insert_into_entry()
        #print(comp)
        #print(keys)
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
        Text = "\n".join(["{0} :  {1}".format(key, df_res[key]) for key in df_res if key != "Critical values"])
        for key in df_res["Critical values"]:
            Text += ("\n \t {0} :  {1}".format(key, df_res["Critical values"][key]))
        self.c1.create_text(135, 80, fill = "Black", font = "Times 10", text = Text, justify='left')
        
        #kpss
        self.c.create_text(38,15,fill="Black",font="Times 10 bold",
                                text="KPSS Test",justify = "center")
        Text_kpss = "\n".join(["{0} :  {1}".format(key, kpss_res[key]) for key in kpss_res if key != "Critical values"])
        for key in kpss_res["Critical values"]:
            Text_kpss += ("\n \t {0} :  {1}".format(key, kpss_res["Critical values"][key]))
        self.c.create_text(135, 80, fill = "Black", font = "Times 10", text = Text_kpss, justify='left')
        


# screen 2        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.canvas = tk.Canvas(self, bg="white", height=450, width=900)
        self.canvas.grid(row=0,rowspan=15,columnspan=10,padx=40,pady=5)
        
        self.c= tk.Canvas(self, bg="white", height=170, width=320)
        self.c.grid(row=0,rowspan=5,column=11,padx=10, pady=15)
        
        self.c1 = tk.Canvas(self, bg="white", height=170, width=320)
        self.c1.grid(row=6,rowspan=5,column=11,padx=10, pady=15)
        
        l1 = tk.Label(self, text="Granger Test",font='Helvetica 11 bold',justify=tk.CENTER)
        l1.configure(background='#ffffff')
        l1.grid(row=11,rowspan=2,column=11,pady=0)

        self.c2 = tk.Canvas(self, bg="white", height=200, width=320)
        self.c2.grid(row=13,rowspan=5,column=11,padx=10, pady=5)
        
        self.c3 = tk.Canvas(self, bg="white", height=100, width=320)
        self.c3.grid(row=16,rowspan=3,column=8,padx=0, pady=5)
        
        l2 = tk.Label(self, text="Data Transformation",font='Helvetica 11 bold',justify=tk.CENTER)
        l2.configure(background='#ffffff')
        l2.grid(row=16,column=1)
        
        tf_methods = ['Raw Data','Log Transformation','1st order Differencing','2nd order Differencing']
        self.var = tk.StringVar(self)
        self.var.set(tf_methods[0])
        
        combo = Combobox(self,textvariable=self.var,width=25)
        combo['values']= tf_methods
        combo.grid(row=16,column=2,padx=20)
        
        l3 = tk.Label(self, text="Smoothing techniques",font='Helvetica 11 bold',justify=tk.CENTER)
        l3.configure(background='#ffffff')
        l3.grid(row=17,column=1,pady=30)
        
        smooth_methods = ['Exponential Smoothing','Simple Exponential Smoothing','Moving Average']
        self.var1 = tk.StringVar(self)
        self.var1.set(smooth_methods[0])
        
        combo1 = Combobox(self,textvariable=self.var1,width=25)
        combo1['values']= smooth_methods
        combo1.grid(row=17,column=2,padx=20,pady=30)
        
        l4 = tk.Label(self, text="Filter techniques",font='Helvetica 11 bold',justify=tk.CENTER)
        l4.configure(background='#ffffff')
        l4.grid(row=18,column=1)
        
        filter_methods = ['Baxter King','Hodrick Prescott','Random Walk']
        self.var2 = tk.StringVar(self)
        self.var2.set(filter_methods[0])
        
        combo2 = Combobox(self,textvariable=self.var2,width=25)
        combo2['values']= filter_methods
        combo2.grid(row=18,column=2,padx=20)
        
        subbtn = tk.Button(self, text="submit",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',width=8)
        subbtn.grid(row=17,column=5)
        
        gotobtnleft = tk.Button(self, text="<",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("StartPage"),width=5)
        gotobtnleft.grid(row=19,column=5)
        
        gotobtnright = tk.Button(self, text=">",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageTwo"),width=5)
        gotobtnright.grid(row=19,column=6)
        

# screen 3
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        l = tk.Label(self, text="Stock Prediction",font='Sans-serif 30 bold',justify=tk.CENTER)
        l.configure(background='#ffffff')
        l.grid(row=0, column=0,columnspan=30,pady=(5,5), padx=(10,10))
        
        self.canvas = tk.Canvas(self, bg="white", height=500, width=950)
        self.canvas.grid(row=1,rowspan=15,columnspan=10,padx=40,pady=20)
        
        lrbtn = tk.Button(self, text="Linear Regression",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',width=20)
        lrbtn.grid(row=5,column=13)
        
        arimabtn = tk.Button(self, text="ARIMA",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',width=20)
        arimabtn.grid(row=6,column=13)
        
        lstmbtn = tk.Button(self, text="LSTM",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',width=20)
        lstmbtn.grid(row=7,column=13)

        prophetbtn = tk.Button(self, text="Prophet",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',width=20)
        prophetbtn.grid(row=8,column=13)
        
        gotobtnleft = tk.Button(self, text="<",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageOne"),width=5)
        gotobtnleft.grid(row=17,column=5)



if __name__ == "__main__":
    window = App()
    window.configure(background='#ffffff')
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.title("Stock Details")
    window.mainloop()

