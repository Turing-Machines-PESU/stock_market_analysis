
# coding: utf-8

# In[32]:


import sys
sys.path.append('../')
import pandas as pd
import warnings
from copy import deepcopy
from time import sleep
from PIL import Image, ImageTk
import matplotlib
import datetime
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")
import tkinter as tk
from tkinter import font  as tkfont 
from tkinter.ttk import Combobox
from time import sleep
from modules.basic import *
from modules.forecast import *
import os
import random
warnings.filterwarnings('ignore')


# In[15]:


stocks_data = pd.read_csv("../stocks.csv")
stocks_data['Date'] = stocks_data['Date'].astype('datetime64[ns]')
stocks_data = stocks_data.set_index('Date')


# In[22]:


stocks_data_2016 = stocks_data['2016']


# In[23]:


companies = deepcopy(stocks_data_2016.Company)
companies.drop_duplicates(inplace=True)
companies.reset_index(drop=True,inplace=True)


# In[24]:


comp_list = list(companies)


# In[25]:


comp_stocks=pd.read_csv("../datasets/filtered_companies.csv")
comp_stocks['Symbol']=comp_stocks.Symbol.str.lower()


# In[26]:


data_words = pd.read_csv("../datasets/words_dates_list_cw.csv")
data_words.drop_duplicates(inplace=True)
data_words.reset_index(drop=True,inplace=True)
key_count = data_words.groupby(["keyword"], sort=False).count().reset_index()
key_count = key_count.loc[key_count['freq'] >= 5]
word_data = deepcopy(key_count.keyword)
word_list = list(map(str, list(word_data)))


# In[27]:


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()


# In[28]:


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


# In[47]:


# GUI for stock details
comp = "xxx"
keys ="xxx"
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
        folder='graph_images'
        if os.path.exists(folder):
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    pass

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
    def get_page(self, page_name):
        for page in self.frames.values():
            if str(page.__class__.__name__) == page_name:
                return page
        return None 
        

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

        self.subbtn = tk.Button(self, text="submit",fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.select, width = 8)
        self.subbtn.grid(row=4,column=2)

        w = tk.Label(self, text="Test for Stationarity", font=("Helvetica", 16),justify=tk.LEFT)
        w.configure(background='#ffffff')
        w.grid(row=5,column=2)
        
        self.gotobtnright = tk.Button(self, state = tk.DISABLED, text="Go to Dashboard",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageOne"),width=20)
        self.gotobtnright.grid(row=11,column=0)
    
      
        
    def smooth_keys(self,keys):
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
        return temp
        
    # graph plot
    def plot(self,company,keys):
        cp = pd.DataFrame(stocks_data_2016[stocks_data_2016.Company==company].Close,columns={'Close'})
        scaled_cp = pd.DataFrame(scaler.fit_transform(cp),columns={'Close'})
        scaled_cp.set_index(cp.index,inplace=True)
        temp = self.smooth_keys(keys)
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
        try:
            self.gotobtnright.config(state = "normal")
            def insert_into_entry():
                items = list(map(int, lb.curselection()))
                if items != ():
                    global selected_item
                    selected_item=[lb.get(items[i]) for i in range(len(items))]
                    return (selected_item)
            global comp
            comp = self.var.get()
            global keys
            keys = insert_into_entry()

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

        except:
            self.gotobtnright.config(state = "disabled")
            pass
        


# screen 2        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
       
        self.canvas = tk.Canvas(self, bg="white", height=480, width=900)
        self.canvas.grid(row=0,rowspan=15,columnspan=10,padx=40,pady=5)
        
        self.c= tk.Canvas(self, bg="white", height=170, width=320)
        self.c.grid(row=0,rowspan=5,column=11,padx=10, pady=15)
        
        self.c1 = tk.Canvas(self, bg="white", height=170, width=320)
        self.c1.grid(row=6,rowspan=5,column=11,padx=10, pady=15)
        
        l1 = tk.Label(self, text="Granger Test",font='Helvetica 11 bold',justify=tk.CENTER)
        l1.configure(background='#ffffff')
        l1.grid(row=11,rowspan=2,column=11,pady=0)

        vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        self.c2 = tk.Canvas(self, bg="white", height=220, width=320,yscrollcommand=vbar.set)
        self.c2.grid(row=13,rowspan=5,column=11,padx=0, pady=5,sticky=tk.E)
        win = tk.Frame(self.c2)
        self.c2.create_window(0,0, window = win, anchor = "nw")
        win.update_idletasks()
        self.c2.configure(scrollregion = (1,1,win.winfo_width(),win.winfo_height()))

        vbar.grid(row=13,rowspan=5,column=12,sticky=(tk.NS,tk.W))
        vbar.config(command=self.c2.yview)
        
        
        self.c3 = tk.Canvas(self, bg="white", height=130, width=320)
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
        sm_fun = [exp_smoothing, simple_exp_smoothing, moving_average]
        self.sm_dict ={}
        for m,fun in zip(smooth_methods,sm_fun):
            self.sm_dict[m] = fun     
        self.var1 = tk.StringVar(self)
        self.var1.set(smooth_methods[0])
        
        combo1 = Combobox(self,textvariable=self.var1,width=25)
        combo1['values']= smooth_methods
        combo1.grid(row=17,column=2,padx=20,pady=30)
        
        l4 = tk.Label(self, text="Filtering techniques",font='Helvetica 11 bold',justify=tk.CENTER)
        l4.configure(background='#ffffff')
        l4.grid(row=18,column=1)
        
        filter_methods = ['Baxter King','Hodrick Prescott','Random Walk']
        fm_fun = [baxter_king, hodrick_prescott, random_walk_filter]
        self.fm_dict ={}
        for m,fun in zip(filter_methods,fm_fun):
            self.fm_dict[m] = fun
        self.var2 = tk.StringVar(self)
        self.var2.set(filter_methods[0])
        
        combo2 = Combobox(self,textvariable=self.var2,width=25)
        combo2['values']= filter_methods
        combo2.grid(row=18,column=2,padx=20)
        
        subbtn = tk.Button(self, text="submit",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.selectvalue,width=8)
        subbtn.grid(row=17,column=5)
        
        gotobtnleft = tk.Button(self, text="<",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("StartPage"),width=5)
        gotobtnleft.grid(row=19,column=5)
        
        self.gotobtnright = tk.Button(self, text=">",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageTwo"),width=5)
        self.gotobtnright.grid(row=19,column=6)
     
    def impute_keycount(self,keys,cp):
        
        temp = []
        for word in keys:
            word_count_data= data_words[data_words['keyword']==word]
            word_count_data['Date'] = word_count_data['Date'].astype('datetime64[ns]')
            word_count_data= word_count_data.set_index('Date')
            word_count = pd.DataFrame(word_count_data.freq,columns={'freq'})
            date=[i.split()[0] for i in list(map(str,cp.index))]
            word_count = impute_points(word_count,date)

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
            
        return temp
        
    
    def plotvalues(self,company,cp,keys):
                
        startpage = self.controller.get_page('StartPage')
        temp = self.impute_keycount(keys,cp)

        plt.figure(figsize = (10,5))
        plt.plot(cp,label=company)
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
        return PATH,temp
        
        
        
    def selectvalue(self):
        
        cp = pd.DataFrame(stocks_data_2016[stocks_data_2016.Company==comp].Close,columns={'Close'})
        tfm = self.var.get()
        sm = self.var1.get()
        fm = self.var2.get()
        
        temp_cp = deepcopy(cp)
        if tfm == 'Log Transformation':
            temp_cp = np.log(cp.Close)
            
        elif tfm == '1st order Differencing':
            temp_cp = cp.Close - cp.Close.shift()
        elif tfm == '2nd order Differencing':
            temp_cp = cp.Close - 2*cp.Close.shift()+ cp.Close.shift(periods=2)
            temp_cp = extend_signal(temp_cp)
        
        try:
            temp_cp = self.sm_dict[sm](temp_cp)
            temp_cp.rename(columns={0 : 'Close'},inplace=True)
            temp_cp = extend_signal(temp_cp.Close)
            temp_cp = self.fm_dict[fm](temp_cp)
            temp_cp = pd.DataFrame(temp_cp,columns=['Close'])

            # Scaling
            scaled_cp = pd.DataFrame(scaler.fit_transform(temp_cp),columns={'Close'})
            scaled_cp.set_index(temp_cp.index,inplace=True)

            path,imputed_key = self.plotvalues(comp,scaled_cp,keys)
            self.canvas.delete("all")
            self.c.delete('all')
            self.c1.delete('all')
            self.c2.delete('all')
            self.c3.delete('all')

            # graph
            image = Image.open(path)
            img = ImageTk.PhotoImage(image)
            self.canvas.create_image(450,230, image=img)
            label = tk.Label(image=img)
            label.image = img 
            image.close()

            # Dickey Fuller test and KPSS test
            df_res = aDickeyFuller(scaled_cp.Close)
            kpss_res = kpss_test(scaled_cp.Close)

            # dfuller
            self.c.create_text(58,15,fill="Black",font="Times 10 bold",
                                    text="Dickey Fuller Test", justify = "center")
            Text = "\n".join(["{0} :  {1}".format(key, df_res[key]) for key in df_res if key != "Critical values"])
            for key in df_res["Critical values"]:
                Text += ("\n \t {0} :  {1}".format(key, df_res["Critical values"][key]))
            self.c.create_text(135, 80, fill = "Black", font = "Times 10", text = Text, justify='left')

            #kpss
            self.c1.create_text(38,15,fill="Black",font="Times 10 bold",
                                    text="KPSS Test",justify = "center")
            Text_kpss = "\n".join(["{0} :  {1}".format(key, kpss_res[key]) for key in kpss_res if key != "Critical values"])
            for key in kpss_res["Critical values"]:
                Text_kpss += ("\n \t {0} :  {1}".format(key, kpss_res["Critical values"][key]))
            self.c1.create_text(135, 80, fill = "Black", font = "Times 10", text = Text_kpss, justify='left')

            RMSE={}
            res_granger = {}
            for key_data,word in zip(imputed_key,keys):
                x=pd.concat([scaled_cp,key_data],axis=1)
                RMSE[word]=rmse(x.Close,x[word])
                lags=50
                try:                
                    res = granger_test(x)
                    pvalues = {}
                    for i in range(10,lags+1,10):
                        pvalues["lag "+str(i)]=res[i][0]['ssr_ftest'][1]
                    res_granger[word]=pvalues 
                except Exception as e:
                    lags = int(str(e).split()[-1])
                    res = granger_test(x,lags)
                    pvalues = {}
                    s = 1
                    e = lags+1
                    if lags < 10 :
                        skip = 2
                    elif lags < 30:
                        skip = 4
                    elif lags < 50:
                        skip = 10          
                    for i in range(s,lags+1,skip):
                        pvalues["lag "+str(i)]=res[i][0]['ssr_ftest'][1]
                    res_granger[word]=pvalues


            #RMSE
            self.c3.create_text(90,15,fill="Black",font="Times 10 bold",
                                    text="Root Mean Square Error",justify = "center")
            Text_rmse = "\n".join(["{0} :  {1}".format(key, RMSE[key]) for key in RMSE])
            self.c3.create_text(105, 70, fill = "Black", font = "Times 10", text =Text_rmse , justify='left')

            #Granger test
            Text_rmse=""
            self.c2.create_text(150,20, fill = "Black", font = "Times 11 bold", text = "*Lower is better*", justify='left')
            for word in keys:
                Text_rmse += word+" :\n"
                Text_rmse+= "   p value :\n"
                Text_rmse += "\n".join(["         {0} :  {1}".format(lag, res_granger[word][lag]) for lag in res_granger[word]])
                Text_rmse+="\n"
            self.c2.create_text(120, 120, fill = "Black", font = "Times 10", text =Text_rmse , justify='left')
        except:
            pass



# screen 3
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.rmse = {}
        l = tk.Label(self, text="Stock Prediction",font='Sans-serif 30 bold',justify=tk.CENTER)
        l.configure(background='#ffffff')
        l.grid(row=0, column=0,columnspan=30,pady=(5,5), padx=(10,10))
        
        self.canvas = tk.Canvas(self, bg="white", height=550, width=1000)
        self.canvas.grid(row=1,rowspan=15,columnspan=10,padx=35,pady=20)
        
        self.c = tk.Canvas(self, bg="white", height=120, width=260)
        self.c.grid(row=10,rowspan=3,column=12,padx=0, pady=5)
        
        lstmbtn = tk.Button(self, text="LSTM",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.lstm,width=20)
        lstmbtn.grid(row=5,column=12)
        
        prophetbtn = tk.Button(self, text="Prophet",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.prophet,width=20)
        prophetbtn.grid(row=6,column=12)
        
        arimabtn = tk.Button(self, text="AUTO_ARIMAX",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.auto_arimax,width=20)
        arimabtn.grid(row=7,column=12)
        
        lrbtn = tk.Button(self, text="Linear Regression",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=self.linear_regression,width=20)
        lrbtn.grid(row=8,column=12)

        
        
        gotobtnleft = tk.Button(self, text="<",font='Helvetica 9 bold',fg='white', bg='#13ade0',relief=tk.GROOVE,activebackground='#1da1f2',activeforeground='white',command=lambda: controller.show_frame("PageOne"),width=5)
        gotobtnleft.grid(row=17,column=5)
        
    def load_image(self,path):
        # graph
        
        self.canvas.delete('all')
        image = Image.open(path)
        self.image = ImageTk.PhotoImage(image)
        self.img_id = self.canvas.create_image(480,300, image=self.image)
        self.canvas.update_idletasks()
        label = tk.Label(image=self.image)
        label.image = self.image 
        image.close()
        
    def create_canvas_img(self,rmse,company,method=""):
        PATH = "graph_images/"+company+"_"+method+".jpeg"  
        plt.title("company : "+ company,fontsize=10)
        plt.xlabel("Date")
        plt.legend()
        fig = plt.gcf()
        fig.set_size_inches(10,5)
        plt.savefig(PATH)
        plt.cla()
        plt.close('all') 
        
        self.canvas.delete('all')
        self.c.delete("all")
        # graph
        image = Image.open(PATH)
        self.img = ImageTk.PhotoImage(image)
        self.canvas.create_image(480,300, image=self.img)
        label = tk.Label(image=self.img)
        label.image = self.img 
        image.close()
        
        #RMSE
        self.c.create_text(90,15,fill="Black",font="Times 10 bold",
                                text="Root Mean Square Error",justify = "center")
       
        self.c.create_text(105, 50, fill = "Black", font = "Times 10", text =rmse , justify='left')

    
    def scale_cp(self,cp):
        cp =np.log(cp)
        scaled_cp = pd.DataFrame(scaler.fit_transform(cp),columns={'Close'})
        scaled_cp.set_index(cp.index,inplace=True)
        return scaled_cp
    
    def is_img_exists(self,PATH,rmse):
        self.canvas.delete('all')
        self.c.delete("all")
        # graph
        image = Image.open(PATH)
        self.img = ImageTk.PhotoImage(image)
        self.canvas.create_image(480,300, image=self.img)
        label = tk.Label(image=self.img)
        label.image = self.img 
        image.close()
        
        #RMSE
        self.c.create_text(90,15,fill="Black",font="Times 10 bold",
                                text="Root Mean Square Error",justify = "center")
       
        self.c.create_text(105, 50, fill = "Black", font = "Times 10", text =rmse , justify='left')

        
    def linear_regression(self):
        
        stocks_data_2016_end = stocks_data['2016':]
        cp = pd.DataFrame(stocks_data_2016_end[stocks_data_2016_end.Company==comp].Close,columns={'Close'})
        scaled_cp =self.scale_cp(cp)
        PATH = "loading.jpg"
        grp_img_path = "graph_images/"+comp+"_lr"+".jpeg"
        if not os.path.exists(grp_img_path):
            self.load_image(PATH)
            self.rmse[comp+'lr'] = regression_model(scaled_cp)
            self.create_canvas_img(self.rmse[comp+'lr'],comp,"lr")
        else:
            self.is_img_exists(grp_img_path,self.rmse[comp+'lr'])
            
        
        
    def auto_arimax(self):
        stocks_data_2016_end = stocks_data['2016':]
        cp = pd.DataFrame(stocks_data_2016_end[stocks_data_2016_end.Company==comp].Close,columns={'Close'})
        scaled_cp =self.scale_cp(cp)
        PATH = "loading.jpg"
        grp_img_path = "graph_images/"+comp+"_arimax"+".jpeg"
        if not os.path.exists(grp_img_path):
            self.load_image(PATH)
            self.rmse[comp+'arimax'] = auto_arimax(scaled_cp)
            self.create_canvas_img(self.rmse[comp+'arimax'],comp,"arimax")
        else:
            self.is_img_exists(grp_img_path,self.rmse[comp+'arimax'])
    
    def lstm(self):
        stocks_data_2016_end = stocks_data['2016':]
        cp = pd.DataFrame(stocks_data_2016_end[stocks_data_2016_end.Company==comp].Close,columns={'Close'})
        scaled_cp =self.scale_cp(cp)
        PATH = "loading.jpg"
        grp_img_path = "graph_images/"+comp+"_lstm"+".jpeg"
        if not os.path.exists(grp_img_path):
            self.load_image(PATH)
            self.rmse[comp+'lstm'] = shallow_lstm(scaled_cp)
            self.create_canvas_img(self.rmse[comp+'lstm'],comp,"lstm")
        else:
            self.is_img_exists(grp_img_path,self.rmse[comp+'lstm'])
    
        

    def prophet(self):
        stocks_data_2016_end = stocks_data['2016':]
        cp = pd.DataFrame(stocks_data_2016_end[stocks_data_2016_end.Company==comp].Close,columns={'Close'})
        scaled_cp =self.scale_cp(cp)
        PATH = "loading.jpg"
        grp_img_path = "graph_images/"+comp+"_p"+".jpeg"
        if not os.path.exists(grp_img_path):
            self.load_image(PATH)
            self.rmse[comp+'p'] = prophet(scaled_cp)
            self.create_canvas_img(self.rmse[comp+'p'],comp,"p")
        else:
            self.is_img_exists(grp_img_path,self.rmse[comp+'p'])
            

if __name__ == "__main__":
    window = App()
    window.configure(background='#ffffff')
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))
    window.title("Stock Details")
    window.mainloop()

