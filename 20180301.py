# -*- coding: utf-8 -*-
import sys
import tkinter.messagebox as box
from tkinter.filedialog import asksaveasfile
if sys.version_info[0] >= 3:
    import tkinter as tk
    import tkinter.ttk as ttk
else:
    import Tkinter as tk
import sqlite3
from tkinter import *

class windowclass(tk.Frame): #建立視窗實體
    def __init__(self, master):         
        tk.Frame.__init__(self, master = None)
        self.master = master
        self.init_window()

    def set_db1(self):
        self.get_data('leed.db')
    def set_db2(self):
        self.get_data()
		
    #初始視窗的創建
    def init_window(self):
        self.master.title("綠建築查詢系統")           		
        self.master.geometry("750x600")
		
		#建立一個選單實體
        menubar = Menu(self.master)
        self.master.config(menu = menubar)
		
		#建立檔案物件
        filemenu = Menu(menubar, tearoff=0)
        #添加一個命令到選單選項，呼叫它來離開，而命令，它在client_exit事件執行
        filemenu.add_command(label = 'LEED' , command = self.set_db1)
        filemenu.add_command(label = 'EEWH', command = self.set_db2)
        filemenu.add_separator()
        filemenu.add_command(label="Exit" , command=self.master.quit)
        menubar.add_cascade(label="System", menu=filemenu)

        #self.dict2 = {['第一組','第二組','第三組']}
        self.lb1 = tk.Label(self.master,text='依指標選擇')
        self.lb1.place(x=0,y=0)
        self.lb2 = tk.Label(self.master,text='依屬性選擇')
        self.lb2.place(x=250,y=0)
        self.lb3 = tk.Label(self.master,text='依變數值選擇')
        self.lb3.place(x=500,y=0)
        self.lb3 = tk.Label(self.master,text='儲存紀錄')
        self.lb3.place(x=60,y=290)	
		
    def get_data(self, database_path = 'outputnew.db'):
        con=sqlite3.connect(database_path)
        cur=con.cursor()
        cur.execute("SELECT name FROM sqlite_master Where Type In ('table')")
        tb_names=cur.fetchall()
        con.commit()		

        self.dict = {}
        self.dict1= {}
        for i in range(0, len(tb_names)):
            cur.execute("PRAGMA table_info(" + tb_names[i][0] + ")")
            field_names=cur.fetchall()
            con.commit()
            arr=[]
            for j in range(1, len(field_names)):
                arr.append(field_names[j][1])
                #print("SELECT DISTINCT " + field_names[j][1] + " FROM '" + tb_names[i][0] + "'")
                cur.execute("SELECT DISTINCT " + field_names[j][1] + " FROM '" + tb_names[i][0] + "'")
                field_values=cur.fetchall()
                brr=[]
                for k in range(0, len(field_values)):
                    brr.append(field_values[k][0])
                self.dict1[field_names[j][1]]=brr
            self.dict[tb_names[i][0]]=arr
        con.close()        
		
        # Initialize comboboxes
        self.combobox_a = ttk.Combobox(self.master, values=list(self.dict.keys()), state='readonly')
        if (database_path == 'outputnew.db'):
            self.combobox_b = ttk.Combobox(self.master, values=self.dict['CO2減量'], state='readonly')
            self.combobox_c = ttk.Combobox(self.master, values=self.dict1['構造形式'], state='readonly')
        elif (database_path == 'leed.db'):
            self.combobox_b = ttk.Combobox(self.master, values=self.dict['室內環境品質'], state='readonly')
            self.combobox_c = ttk.Combobox(self.master, values=self.dict1['得分項目'], state='readonly')            
		
        # Select 0 element
        self.combobox_a.current(0)
        self.combobox_b.current(0)
        self.combobox_c.current(0)
        # Add event to update variables on combobox's value change event
        self.combobox_a.bind("<<ComboboxSelected>>", lambda f1: self.fun())
        self.combobox_b.bind("<<ComboboxSelected>>", lambda f2: self.fun2())
        self.combobox_c.bind("<<ComboboxSelected>>", lambda f3: self.fun3())
        # Initialize variables
        self.area = self.combobox_a.get()
        self.last_area = self.country = self.combobox_b.get()
        self.last_country = self.twon = self.combobox_c.get()
        # Place all controls to frame
        self.combobox_a.place(x=0,y=25)
        self.combobox_b.place(x=250,y=25)
        self.combobox_c.place(x=500,y=25)

        #self.combobox_d = ttk.Combobox(master, values=['第一組','第二組','第三組','第四組','第五組','第六組','第七組','第八組','第九組','第十組'], state='readonly')
        #self.combobox_d.place(x=60,y=315)
		
		
        self.lb4 = tk.Label(self.master,text='已選擇條件')
        self.lb4.place(x=0,y=60)
        self.listb_a = tk.Listbox(self.master,width=30,selectmode = EXTENDED)
        self.items = self.listb_a.curselection()
        self.listb_a.place(x=0,y=80)
        
        self.listb_b = tk.Listbox(self.master,width=30,selectmode = EXTENDED)
        self.listb_b.place(x=250,y=80)
        self.listb_c = tk.Listbox(self.master,width=30,selectmode = EXTENDED)
        self.listb_c.place(x=500,y=80)
        self.btn = tk.Button(self.master , text = "刪除" , command = self.del_list_item )
        self.btn.place(x=650,y=250)
        
        self.btn1 = tk.Button(self.master , text = "查詢" , command =self.button_case)
        self.btn1.place(x=650,y=300)

        self.btn1 = tk.Button(self.master , text = "儲存" , command =self.button_case)
        self.btn1.place(x=650,y=550)

        self.recordbtn = tk.Button(self.master,text= '紀錄' , command = self.immediately)
        self.recordbtn.place(x=0,y=320)
        all_items =self.listb_a.get(0, tk.END)
        self.recordlistb_a=tk.Listbox(self.master, width=30)
        self.recordlistb_a.place(x=0,y=340)
        self.recordlistb_b=tk.Listbox(self.master, width=30)
        self.recordlistb_b.place(x=250,y=340)
        self.recordlistb_c=tk.Listbox(self.master, width=30)
        self.recordlistb_c.place(x=500,y=340)

    def del_list_item(self):
        sel_a = self.listb_a.curselection()
        for index in sel_a[::-1]:
            self.listb_a.delete(index)
        sel_b = self.listb_b.curselection()
        for index in sel_b[::-1]:
            self.listb_b.delete(index)
        sel_c = self.listb_c.curselection()
        for index in sel_c[::-1]:
            self.listb_c.delete(index)

    def immediately(self):
        sel_a = self.listb_a.curselection()
        for index in sel_a[::+1]:
            self.listb_a.insert(index)
        sel_b = self.listb_b.curselection()
        for index in sel_b[::+1]:
            self.listb_b.insert(index)
        sel_c = self.listb_c.curselection()
        for index in sel_c[::+1]:
            self.listb_c.insert(index)
		
    def fun(self):
        print("changed 1-st combobox value to: " + self.combobox_a.get())
        if self.last_area != self.combobox_a.get():
            self.combobox_b['values']=self.dict[self.combobox_a.get()]
            self.combobox_b.current(0)
            self.country = self.combobox_b.get()
        self.last_area = self.area = self.combobox_a.get()
        global XX
        XX = self.combobox_a.get()
        self.listb_a.insert(END,XX)
        self.recordlistb_a.insert(END,XX)

    def fun2(self):
        print("changed 2-nd combobox value to: " + self.combobox_b.get())
        if self.last_country != self.combobox_b.get():
            self.combobox_c['values']=self.dict1[self.combobox_b.get()]
            self.combobox_c.current(0)
            self.twon = self.combobox_c.get()
        self.last_country = self.country = self.combobox_b.get()
        global YY
        YY = self.combobox_b.get()
        self.listb_b.insert(END,YY)
        self.recordlistb_b.insert(END,YY)
        
    def fun3(self):
        print("changed 3-rd combobox value to: " + self.combobox_c.get())
        self.twon = self.combobox_c.get()
        global ZZ
        ZZ = self.combobox_c.get()
        self.listb_c.insert(END,ZZ)
        self.recordlistb_c.insert(END,ZZ)

    def button_case(self):
        global XX
        XX = self.combobox_a.get()
        if XX=='照明節能':
            """
            self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass1(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
            # print(self.app.tempList)
        elif XX=='外殼節能':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass2(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='空調節能':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass3(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='CO2減量':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass4(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='基地保水':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass5(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='綠化設計':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass6(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='室內環境':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass7(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='污水垃圾':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass8(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='廢棄物減量':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass9(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        elif XX=='水資源':
            """self.newWindow = tk.Toplevel(self.master)"""
            self.app = windowclass10(self.master)
            self.newWindow0 = tk.Toplevel(self.master)
            self.app0 = windowclass0(self.newWindow0, self.app.tempList)
        else:
            print('error')
            self.newWindow = tk.Toplevel(self.master)
            self.app = windowclass0(self.newWindow, self.app.tempList)
 
class windowclass0(tk.Frame):
    
    tempList_a = []
    tup_list=[]
    #bList=['外殼設計方案','空調設計方案','照明設計方案','CO2減量方案','廢棄物減量方案','室內環境設計方案','生物多樣性方案','綠化量設計方案','基地保水設計方案','水資源節省方案','污水垃圾改善方案']
    def __init__(self , master, aList):
        tk.Frame.__init__(self, master)
        master.title("SUMMARY")
        self.master.geometry("660x1080")
        #self.backButton2 = tk.Button(master, text = '上一頁', width = 15)
        #self.backButton2.place(x=0,y=650)
        #self.nextButton2 = tk.Button(master, text = '下一頁', width = 15)
        #self.nextButton2.place(x=100,y=650)
        self.quitButton2 = tk.Button(master, text = 'Quit', width = 15 , command = self.close_window2)
        self.quitButton2.place(x=100,y=650)
        self.dataButton2 = tk.Button(master, text = '顯示', width = 10, command = self.windowclass13)
        self.dataButton2.place(x=300,y=650)
        
        self.frame2 = tk.Frame(master)
        self.frame2.place(x=0, y=0, width=600, height=640)

        #滚动条
        self.scrollBar2 = Scrollbar(self.frame2)
        self.scrollBar2.pack(side=RIGHT, fill=Y,)
        self.scrollBar3 = Scrollbar(self.frame2,orient=HORIZONTAL)
        self.scrollBar3.pack(side=BOTTOM, fill=X)

        self.tree2 = ttk.Treeview(self.frame2,
                    columns=('c1','c2','c3','c4'),
                    show="headings",
                    yscrollcommand=self.scrollBar2.set,
                    xscrollcommand=self.scrollBar3.set)
                
        #设置每列宽度和对齐方式
        self.tree2.column('c1', width=100, anchor='center')
        self.tree2.column('c2', width=150, anchor='center')
        self.tree2.column('c3', width=150, anchor='center')
        self.tree2.column('c4', width=150, anchor='center')

        #设置每列表头标题文本
        self.tree2.heading('c1', text='編號')
        self.tree2.heading('c2', text='總成本(元)')
        self.tree2.heading('c3', text='單位成本(元/坪)')
        self.tree2.heading('c4', text='單位成本(元/平方公尺)')
        
        self.tree2.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2.config(command=self.tree2.yview)
        self.scrollBar3.config(command=self.tree2.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        #print(aList)

        #sql ='select * from "成本" where "'+ XX +'" = ?', (item, )

        for item in aList:
            
            #print(item)
            #sql='select * from "成本" where "'+ XX +'" = ?', (item, )
            #ct='select count(*) from "成本"'
            c.execute('select "編號","總成本_元","單位成本_元每坪","單位成本_元每平方公尺" from "成本" where "'+ XX +'" = ?', (item, ))
            
            rows=c.fetchall()

            for r in c.execute('select "編號","總成本_元","單位成本_元每坪","單位成本_元每平方公尺" from "成本" where "'+ XX +'" = ?', (item, )):
                
                    #self.tempList_a=list(set(self.tempList_a))
                    #print(self.tempList_a)
                #print(r)
                self.tree2.insert("","end",values=r)

            for tup in rows:
                #self.tempList_a.append(tup)
                self.tup_list.append(tup[1])
                #print(list(set(self.tup_list)))

        """===================================右邊第一個表格==================================
                
        self.frame2_1 = tk.Frame(master)
        self.frame2_1.place(x=700, y=0, width=600, height=60)

        self.scrollBar2_1 = Scrollbar(self.frame2_1)
        self.scrollBar2_1.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_1 = Scrollbar(self.frame2_1,orient=HORIZONTAL)
        self.scrollBar3_1.pack(side=BOTTOM, fill=X)

        self.tree2_1 = ttk.Treeview(self.frame2_1,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_1.set,
                    xscrollcommand=self.scrollBar3_1.set)
                
        #设置每列宽度和对齐方式
        self.tree2_1.column('c1', width=100, anchor='center')
        self.tree2_1.column('c2', width=150, anchor='center')
        self.tree2_1.column('c3', width=150, anchor='center')
        self.tree2_1.column('c4', width=150, anchor='center')
        self.tree2_1.column('c5', width=150, anchor='center')
        self.tree2_1.column('c6', width=150, anchor='center')
        self.tree2_1.column('c7', width=150, anchor='center')
        self.tree2_1.column('c8', width=150, anchor='center')
        self.tree2_1.column('c9', width=150, anchor='center')
        self.tree2_1.column('c10', width=150, anchor='center')
        self.tree2_1.column('c11', width=150, anchor='center')

        #设置每列表头标题文本
        self.tree2_1.heading('c1', text='外殼節能')
        self.tree2_1.heading('c2', text='空調節能')
        self.tree2_1.heading('c3', text='照明節能')
        self.tree2_1.heading('c4', text='CO2減量')
        self.tree2_1.heading('c5', text='廢棄物減量')
        self.tree2_1.heading('c6', text='室內環境')
        self.tree2_1.heading('c7', text='生物多樣性方案')
        self.tree2_1.heading('c8', text='綠化設計')
        self.tree2_1.heading('c9', text='基地保水')
        self.tree2_1.heading('c10', text='水資源')
        self.tree2_1.heading('c11', text='污水垃圾')
        
        self.tree2_1.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_1.config(command=self.tree2_1.yview)
        self.scrollBar3_1.config(command=self.tree2_1.xview)

        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select "外殼節能","空調節能","照明節能","CO2減量","廢棄物減量","室內環境","生物多樣性方案","綠化設計","基地保水","水資源","污水垃圾" from "成本" where "編號"="199"')
        rows=c.fetchall()

        for r in rows:
            self.tree2_1.insert("","end",values=r)"""

    def close_window2(self):
            self.master.destroy()

    def windowclass13(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = windowclass13(self.newWindow)

class windowclass13(tk.Frame):
    
    tempList_a = []
    tup_list=[]
    #bList=['外殼設計方案','空調設計方案','照明設計方案','CO2減量方案','廢棄物減量方案','室內環境設計方案','生物多樣性方案','綠化量設計方案','基地保水設計方案','水資源節省方案','污水垃圾改善方案']
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("方案內容")
        self.master.geometry("700x700")


        """===================================右邊第二個表格(外殼)=================================="""

        self.frame2_2 = tk.Frame(master)
        self.frame2_2.place(x=0, y=65, width=600, height=60)

        self.scrollBar2_2 = Scrollbar(self.frame2_2)
        self.scrollBar2_2.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_2 = Scrollbar(self.frame2_2,orient=HORIZONTAL)
        self.scrollBar3_2.pack(side=BOTTOM, fill=X)

        self.tree2_2 = ttk.Treeview(self.frame2_2,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_2.set,
                    xscrollcommand=self.scrollBar3_2.set)
                
        #设置每列宽度和对齐方式
        self.tree2_2.column('c1', width=100, anchor='center')
        self.tree2_2.column('c2', width=150, anchor='center')
        self.tree2_2.column('c3', width=150, anchor='center')
        self.tree2_2.column('c4', width=150, anchor='center')
        self.tree2_2.column('c5', width=150, anchor='center')
        self.tree2_2.column('c6', width=150, anchor='center')
        self.tree2_2.column('c7', width=150, anchor='center')
        self.tree2_2.column('c8', width=150, anchor='center')
        self.tree2_2.column('c9', width=150, anchor='center')

        #设置每列表头标题文本
        self.tree2_2.heading('c1', text='方案')
        self.tree2_2.heading('c2', text='屋頂材質')
        self.tree2_2.heading('c3', text='外牆材質')
        self.tree2_2.heading('c4', text='開窗率(%)')
        self.tree2_2.heading('c5', text='玻璃熱傳透率')
        self.tree2_2.heading('c6', text='玻璃外遮陽x日射透過率')
        self.tree2_2.heading('c7', text='總立面開窗面積')
        self.tree2_2.heading('c8', text='總立面實牆面積')
        self.tree2_2.heading('c9', text='指標得分')
        
        self.tree2_2.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_2.config(command=self.tree2_2.yview)
        self.scrollBar3_2.config(command=self.tree2_2.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "外殼節能" where "方案"= "1" ')
        rows=c.fetchall()

        for r in rows:
            self.tree2_2.insert("","end",values=r)

        """===================================右邊第三個表格(照明)=================================="""

        self.frame2_3 = tk.Frame(master)
        self.frame2_3.place(x=0, y=130, width=600, height=60)

        self.scrollBar2_3 = Scrollbar(self.frame2_3)
        self.scrollBar2_3.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_3 = Scrollbar(self.frame2_3,orient=HORIZONTAL)
        self.scrollBar3_3.pack(side=BOTTOM, fill=X)

        self.tree2_3 = ttk.Treeview(self.frame2_3,
                    columns=('c1','c2','c3','c4','c5','c6','c7'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_3.set,
                    xscrollcommand=self.scrollBar3_3.set)
                
        #设置每列宽度和对齐方式
        self.tree2_3.column('c1', width=100, anchor='center')
        self.tree2_3.column('c2', width=150, anchor='center')
        self.tree2_3.column('c3', width=150, anchor='center')
        self.tree2_3.column('c4', width=150, anchor='center')
        self.tree2_3.column('c5', width=150, anchor='center')
        self.tree2_3.column('c6', width=150, anchor='center')
        self.tree2_3.column('c7', width=150, anchor='center')

        #设置每列表头标题文本
        self.tree2_3.heading('c1', text='方案')
        self.tree2_3.heading('c2', text='燈具系統')
        self.tree2_3.heading('c3', text='燈具效率係數(IER)')
        self.tree2_3.heading('c4', text='照明功率係數(IDR)')
        self.tree2_3.heading('c5', text='再生能源節能比例(%)')
        self.tree2_3.heading('c6', text='建築能源管理系統效率(Beta2)')
        self.tree2_3.heading('c7', text='指標得分')
        
        self.tree2_3.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_3.config(command=self.tree2_3.yview)
        self.scrollBar3_3.config(command=self.tree2_3.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "照明節能" where "方案"="313"')
        rows=c.fetchall()

        for r in rows:
            self.tree2_3.insert("","end",values=r)


        """===================================右邊第四個表格(空調)=================================="""

        self.frame2_4 = tk.Frame(master)
        self.frame2_4.place(x=0, y=195, width=600, height=60)

        self.scrollBar2_4 = Scrollbar(self.frame2_4)
        self.scrollBar2_4.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_4 = Scrollbar(self.frame2_4,orient=HORIZONTAL)
        self.scrollBar3_4.pack(side=BOTTOM, fill=X)

        self.tree2_4 = ttk.Treeview(self.frame2_4,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17','c18','c19','c20','c21','c22','c23'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_4.set,
                    xscrollcommand=self.scrollBar3_4.set)
                
        #设置每列宽度和对齐方式
        self.tree2_4.column('c1', width=100, anchor='center')
        self.tree2_4.column('c2', width=150, anchor='center')
        self.tree2_4.column('c3', width=150, anchor='center')
        self.tree2_4.column('c4', width=150, anchor='center')
        self.tree2_4.column('c5', width=150, anchor='center')
        self.tree2_4.column('c6', width=150, anchor='center')
        self.tree2_4.column('c7', width=150, anchor='center')
        self.tree2_4.column('c8', width=150, anchor='center')
        self.tree2_4.column('c9', width=150, anchor='center')
        self.tree2_4.column('c10', width=150, anchor='center')
        self.tree2_4.column('c11', width=150, anchor='center')
        self.tree2_4.column('c12', width=150, anchor='center')
        self.tree2_4.column('c13', width=150, anchor='center')
        self.tree2_4.column('c14', width=150, anchor='center')
        self.tree2_4.column('c15', width=150, anchor='center')
        self.tree2_4.column('c16', width=150, anchor='center')
        self.tree2_4.column('c17', width=150, anchor='center')
        self.tree2_4.column('c18', width=150, anchor='center')
        self.tree2_4.column('c19', width=150, anchor='center')
        self.tree2_4.column('c20', width=150, anchor='center')
        self.tree2_4.column('c21', width=150, anchor='center')
        self.tree2_4.column('c22', width=150, anchor='center')
        self.tree2_4.column('c23', width=150, anchor='center')

        #设置每列表头标题文本
        self.tree2_4.heading('c1', text='方案')
        self.tree2_4.heading('c2', text='空調主機')
        self.tree2_4.heading('c3', text='最大空調容量(USRT)')
        self.tree2_4.heading('c4', text='主機效率係數')
        self.tree2_4.heading('c5', text='熱源系統功率比PRs')
        self.tree2_4.heading('c6', text='送風系統功率比PRf')
        self.tree2_4.heading('c7', text='送水系統功率比PRp')
        self.tree2_4.heading('c8', text='冰水主機台數控制系統')
        self.tree2_4.heading('c9', text='儲冰空調系統')
        self.tree2_4.heading('c10', text='吸收式或熱泵式冷凍機')
        self.tree2_4.heading('c11', text='變冷媒量熱源VRV')
        self.tree2_4.heading('c12', text='變頻主機')
        self.tree2_4.heading('c13', text='CO2濃度外氣量控制系統')
        self.tree2_4.heading('c14', text='全熱交換器系統')
        self.tree2_4.heading('c15', text='外氣冷房系統')
        self.tree2_4.heading('c16', text='空調風扇並用系統')
        self.tree2_4.heading('c17', text='送風系統節能技術')
        self.tree2_4.heading('c18', text='送水系統-一次冰水變頻系統')
        self.tree2_4.heading('c19', text='送水系統-變頻無段變速')
        self.tree2_4.heading('c20', text='送水系統-冰水泵台數控制')
        self.tree2_4.heading('c21', text='再生能源節能比例(%)')
        self.tree2_4.heading('c22', text='建築能源管理系統效率(Beta2)')
        self.tree2_4.heading('c23', text='指標得分')
        
        self.tree2_4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_4.config(command=self.tree2_4.yview)
        self.scrollBar3_4.config(command=self.tree2_4.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "空調節能" where "方案"="11929"')
        rows=c.fetchall()
        
        for r in rows:
            self.tree2_4.insert("","end",values=r)
            

        """===================================右邊第四個表格(CO2)=================================="""

        self.frame2_4 = tk.Frame(master)
        self.frame2_4.place(x=0, y=260, width=600, height=60)

        self.scrollBar2_4 = Scrollbar(self.frame2_4)
        self.scrollBar2_4.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_4 = Scrollbar(self.frame2_4,orient=HORIZONTAL)
        self.scrollBar3_4.pack(side=BOTTOM, fill=X)

        self.tree2_4 = ttk.Treeview(self.frame2_4,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_4.set,
                    xscrollcommand=self.scrollBar3_4.set)
                
        #设置每列宽度和对齐方式
        self.tree2_4.column('c1', width=100, anchor='center')
        self.tree2_4.column('c2', width=150, anchor='center')
        self.tree2_4.column('c3', width=150, anchor='center')
        self.tree2_4.column('c4', width=150, anchor='center')
        self.tree2_4.column('c5', width=150, anchor='center')
        self.tree2_4.column('c6', width=150, anchor='center')
        self.tree2_4.column('c7', width=150, anchor='center')
        self.tree2_4.column('c8', width=150, anchor='center')
        self.tree2_4.column('c9', width=150, anchor='center')
        self.tree2_4.column('c10', width=150, anchor='center')
        self.tree2_4.column('c11', width=150, anchor='center')
        self.tree2_4.column('c12', width=150, anchor='center')
        self.tree2_4.column('c13', width=150, anchor='center')
        self.tree2_4.column('c14', width=150, anchor='center')


        #设置每列表头标题文本
        self.tree2_4.heading('c1', text='方案')
        self.tree2_4.heading('c2', text='構造形式')
        self.tree2_4.heading('c3', text='隔間牆形式')
        self.tree2_4.heading('c4', text='外牆形式')
        self.tree2_4.heading('c5', text='預鑄整體衛浴')
        self.tree2_4.heading('c6', text='耐震力升級設計')
        self.tree2_4.heading('c7', text='RC梁柱保護層增加量')
        self.tree2_4.heading('c8', text='RC樓版保護層增加量')
        self.tree2_4.heading('c9', text='屋頂防水層')
        self.tree2_4.heading('c10', text='空調設備管路')
        self.tree2_4.heading('c11', text='電器通信線路')
        self.tree2_4.heading('c12', text='變頻主機')
        self.tree2_4.heading('c13', text='再生建材使用係數')
        self.tree2_4.heading('c14', text='指標得分')

        
        self.tree2_4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_4.config(command=self.tree2_4.yview)
        self.scrollBar3_4.config(command=self.tree2_4.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "CO2減量" where "方案"="152"')
        rows=c.fetchall()
        
        for r in rows:
            self.tree2_4.insert("","end",values=r)


        """===================================右邊第四個表格(廢棄物)=================================="""

        self.frame2_4 = tk.Frame(master)
        self.frame2_4.place(x=0, y=325, width=600, height=60)

        self.scrollBar2_4 = Scrollbar(self.frame2_4)
        self.scrollBar2_4.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_4 = Scrollbar(self.frame2_4,orient=HORIZONTAL)
        self.scrollBar3_4.pack(side=BOTTOM, fill=X)

        self.tree2_4 = ttk.Treeview(self.frame2_4,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_4.set,
                    xscrollcommand=self.scrollBar3_4.set)
                
        #设置每列宽度和对齐方式
        self.tree2_4.column('c1', width=100, anchor='center')
        self.tree2_4.column('c2', width=150, anchor='center')
        self.tree2_4.column('c3', width=150, anchor='center')
        self.tree2_4.column('c4', width=150, anchor='center')
        self.tree2_4.column('c5', width=150, anchor='center')
        self.tree2_4.column('c6', width=150, anchor='center')
        self.tree2_4.column('c7', width=150, anchor='center')
        self.tree2_4.column('c8', width=150, anchor='center')
        self.tree2_4.column('c9', width=150, anchor='center')
        self.tree2_4.column('c10', width=150, anchor='center')
        self.tree2_4.column('c11', width=150, anchor='center')



        #设置每列表头标题文本
        self.tree2_4.heading('c1', text='方案')
        self.tree2_4.heading('c2', text='構造形式')
        self.tree2_4.heading('c3', text='系統模版')
        self.tree2_4.heading('c4', text='預鑄外牆')
        self.tree2_4.heading('c5', text='預鑄梁柱')
        self.tree2_4.heading('c6', text='預鑄樓版')
        self.tree2_4.heading('c7', text='預鑄浴廁')
        self.tree2_4.heading('c8', text='乾式隔間')
        self.tree2_4.heading('c9', text='粒狀污染物防制效率')
        self.tree2_4.heading('c10', text='再生建材使用率')
        self.tree2_4.heading('c11', text='指標得分')

        
        self.tree2_4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_4.config(command=self.tree2_4.yview)
        self.scrollBar3_4.config(command=self.tree2_4.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "廢棄物減量" where "方案"="1"')
        rows=c.fetchall()
        
        for r in rows:
            self.tree2_4.insert("","end",values=r)


        """===================================右邊第四個表格(室內環境)=================================="""

        self.frame2_4 = tk.Frame(master)
        self.frame2_4.place(x=0, y=390, width=600, height=60)

        self.scrollBar2_4 = Scrollbar(self.frame2_4)
        self.scrollBar2_4.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_4 = Scrollbar(self.frame2_4,orient=HORIZONTAL)
        self.scrollBar3_4.pack(side=BOTTOM, fill=X)

        self.tree2_4 = ttk.Treeview(self.frame2_4,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_4.set,
                    xscrollcommand=self.scrollBar3_4.set)
                
        #设置每列宽度和对齐方式
        self.tree2_4.column('c1', width=100, anchor='center')
        self.tree2_4.column('c2', width=150, anchor='center')
        self.tree2_4.column('c3', width=150, anchor='center')
        self.tree2_4.column('c4', width=150, anchor='center')
        self.tree2_4.column('c5', width=150, anchor='center')
        self.tree2_4.column('c6', width=150, anchor='center')
        self.tree2_4.column('c7', width=150, anchor='center')
        self.tree2_4.column('c8', width=150, anchor='center')
        self.tree2_4.column('c9', width=150, anchor='center')
        self.tree2_4.column('c10', width=150, anchor='center')



        #设置每列表头标题文本
        self.tree2_4.heading('c1', text='方案')
        self.tree2_4.heading('c2', text='外牆厚度')
        self.tree2_4.heading('c3', text='窗厚度')
        self.tree2_4.heading('c4', text='樓版厚度')
        self.tree2_4.heading('c5', text='可見光透光率')
        self.tree2_4.heading('c6', text='人工照明狀況')
        self.tree2_4.heading('c7', text='建築裝修量')
        self.tree2_4.heading('c8', text='綠建材使用率')
        self.tree2_4.heading('c9', text='生態建材項目')
        self.tree2_4.heading('c10', text='指標得分')

        
        self.tree2_4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_4.config(command=self.tree2_4.yview)
        self.scrollBar3_4.config(command=self.tree2_4.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "室內環境" where "方案"="6"')
        rows=c.fetchall()
        
        for r in rows:
            self.tree2_4.insert("","end",values=r)

        """===================================右邊第四個表格(基地保水)=================================="""

        self.frame2_4 = tk.Frame(master)
        self.frame2_4.place(x=0, y=455, width=600, height=60)

        self.scrollBar2_4 = Scrollbar(self.frame2_4)
        self.scrollBar2_4.pack(side=RIGHT, fill=Y,)

        self.scrollBar3_4 = Scrollbar(self.frame2_4,orient=HORIZONTAL)
        self.scrollBar3_4.pack(side=BOTTOM, fill=X)

        self.tree2_4 = ttk.Treeview(self.frame2_4,
                    columns=('c1','c2','c3','c4','c5','c6','c7'),
                    show="headings",
                    yscrollcommand=self.scrollBar2_4.set,
                    xscrollcommand=self.scrollBar3_4.set)
                
        #设置每列宽度和对齐方式
        self.tree2_4.column('c1', width=100, anchor='center')
        self.tree2_4.column('c2', width=150, anchor='center')
        self.tree2_4.column('c3', width=150, anchor='center')
        self.tree2_4.column('c4', width=150, anchor='center')
        self.tree2_4.column('c5', width=150, anchor='center')
        self.tree2_4.column('c6', width=150, anchor='center')
        self.tree2_4.column('c7', width=150, anchor='center')




        #设置每列表头标题文本
        self.tree2_4.heading('c1', text='方案')
        self.tree2_4.heading('c2', text='保水設計方法')
        self.tree2_4.heading('c3', text='設計變數')
        self.tree2_4.heading('c4', text='設計值')
        self.tree2_4.heading('c5', text='設計變數')
        self.tree2_4.heading('c6', text='設計值')
        self.tree2_4.heading('c7', text='指標得分')

        
        self.tree2_4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar2_4.config(command=self.tree2_4.yview)
        self.scrollBar3_4.config(command=self.tree2_4.xview)

        
        conndb = sqlite3.connect(database_path)
        c = conndb.cursor()
        c.execute('select * from "基地保水" where "方案"="4"')
        rows=c.fetchall()
        
        for r in rows:
            self.tree2_4.insert("","end",values=r)            

            
    def close_window2(self):
            self.master.destroy()

    def windowclass13(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = windowclass13(self.newWindow)

    def btn_click(self, event=None):
        '''
        choose frm
        '''
        btn_text = event.widget['text']
        if btn_text == "1":
            #self.show_label_0.pack(fill="both", expand=1, padx=300, pady=300)
            self.tree5.pack(side=LEFT, fill=Y)
            self.tree2.pack_forget()
            self.tree.pack_forget()
        elif btn_text == "基地保水":
            #self.show_label_0.pack_forget()
            self.tree5.pack_forget()
            self.tree2.pack_forget()
            self.tree.pack_forget() 

"""--------------------------------------照明節能--------------------------------------"""
class windowclass1(windowclass,tk.Frame):

    tempList = []
    def __init__(self , master):
        self.master = master
        self.frame = tk.Frame(master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window)
        self.quitButton.place(x=400,y=250)
        self.frame1 = tk.Frame(master)
        self.frame1.place(x=0, y=25, width=800 ,height=750)

        #滚动条
        self.scrollBar = Scrollbar(self.frame1)
        self.scrollBar.pack(side=RIGHT, fill=Y,)
        self.scrollBar1 = Scrollbar(self.frame1,orient=HORIZONTAL)
        self.scrollBar1.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(self.frame1,
                    columns=('c1','c2','c3','c4','c5','c6','c7'),
                    show="headings",
                    yscrollcommand=self.scrollBar.set,
                    xscrollcommand=self.scrollBar1.set)
                
        #设置每列宽度和对齐方式
        self.tree.column('c1', width=100, anchor='center')
        self.tree.column('c2', width=150, anchor='center')
        self.tree.column('c3', width=150, anchor='center')
        self.tree.column('c4', width=150, anchor='center')
        self.tree.column('c5', width=150, anchor='center')
        self.tree.column('c6', width=180, anchor='center')
        self.tree.column('c7', width=100, anchor='center')

        #设置每列表头标题文本
        self.tree.heading('c1', text='方案')
        self.tree.heading('c2', text='燈具系統')
        self.tree.heading('c3', text='燈具效率係數(IER)')
        self.tree.heading('c4', text='照明功率係數(IDR)')
        self.tree.heading('c5', text='再生能源節能比例(%)')
        self.tree.heading('c6', text='建築能源管理系統效率(Beta2)')
        self.tree.heading('c7', text='指標得分')
        self.tree.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合
        self.scrollBar.config(command=self.tree.yview)
        self.scrollBar1.config(command=self.tree.xview)
        
        #插入演示数据
        
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'
        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])
            #print(list(set(self.tempList)))
            


        for row in rows:
            self.tree.insert("","end",values=row)
                       
    def close_window(self):
            self.master.destroy()
       
"""--------------------------------------外殼節能--------------------------------------"""
class windowclass2(tk.Frame):
    
    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton3 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window3)
        self.quitButton3.place(x=400,y=250)
        self.frame3 = tk.Frame(master)
        self.frame3.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar4 = Scrollbar(self.frame3)
        self.scrollBar4.pack(side=RIGHT, fill=Y,)
        self.scrollBar5 = Scrollbar(self.frame3,orient=HORIZONTAL)
        self.scrollBar5.pack(side=BOTTOM, fill=X)

        self.tree3 = ttk.Treeview(self.frame3,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9'),
                    show="headings",
                    yscrollcommand=self.scrollBar4.set,
                    xscrollcommand=self.scrollBar5.set)
                
        #设置每列宽度和对齐方式
        self.tree3.column('c1', width=100, anchor='center')
        self.tree3.column('c2', width=150, anchor='center')
        self.tree3.column('c3', width=150, anchor='center')
        self.tree3.column('c4', width=150, anchor='center')
        self.tree3.column('c5', width=150, anchor='center')
        self.tree3.column('c6', width=180, anchor='center')
        self.tree3.column('c7', width=100, anchor='center')
        self.tree3.column('c8', width=100, anchor='center')
        self.tree3.column('c9', width=100, anchor='center')


        #设置每列表头标题文本
        self.tree3.heading('c1', text='方案')
        self.tree3.heading('c2', text='屋頂材質')
        self.tree3.heading('c3', text='外牆材質')
        self.tree3.heading('c4', text='開窗率(%)')
        self.tree3.heading('c5', text='玻璃熱傳透率')
        self.tree3.heading('c6', text='玻璃外遮陽x日射透過率')
        self.tree3.heading('c7', text='總立面開窗面積')
        self.tree3.heading('c8', text='總立面實牆面積')
        self.tree3.heading('c9', text='指標得分')

        
        self.tree3.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar4.config(command=self.tree3.yview)
        self.scrollBar5.config(command=self.tree3.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree3.insert("","end",values=row)

    def close_window3(self):
            self.master.destroy()

"""--------------------------------------空調節能--------------------------------------"""
class windowclass3(tk.Frame):
    
    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton4 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window4)
        self.quitButton4.place(x=400,y=250)
        self.frame4 = tk.Frame(master)
        self.frame4.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar6 = Scrollbar(self.frame4)
        self.scrollBar6.pack(side=RIGHT, fill=Y,)
        self.scrollBar7 = Scrollbar(self.frame4,orient=HORIZONTAL)
        self.scrollBar7.pack(side=BOTTOM, fill=X)

        self.tree4 = ttk.Treeview(self.frame4,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17','c18','c19','c20','c21','c22','c23'),
                    show="headings",
                    yscrollcommand=self.scrollBar6.set,
                    xscrollcommand=self.scrollBar7.set)
                
        #设置每列宽度和对齐方式
        self.tree4.column('c1', width=100, anchor='center')
        self.tree4.column('c2', width=150, anchor='center')
        self.tree4.column('c3', width=150, anchor='center')
        self.tree4.column('c4', width=150, anchor='center')
        self.tree4.column('c5', width=150, anchor='center')
        self.tree4.column('c6', width=180, anchor='center')
        self.tree4.column('c7', width=100, anchor='center')
        self.tree4.column('c8', width=100, anchor='center')
        self.tree4.column('c9', width=100, anchor='center')
        self.tree4.column('c10', width=100, anchor='center')
        self.tree4.column('c11', width=100, anchor='center')
        self.tree4.column('c12', width=100, anchor='center')
        self.tree4.column('c13', width=100, anchor='center')
        self.tree4.column('c14', width=100, anchor='center')
        self.tree4.column('c15', width=100, anchor='center')
        self.tree4.column('c16', width=100, anchor='center')
        self.tree4.column('c17', width=100, anchor='center')
        self.tree4.column('c18', width=100, anchor='center')
        self.tree4.column('c19', width=100, anchor='center')
        self.tree4.column('c20', width=100, anchor='center')
        self.tree4.column('c21', width=100, anchor='center')
        self.tree4.column('c22', width=100, anchor='center')
        self.tree4.column('c23', width=100, anchor='center')

        #设置每列表头标题文本
        self.tree4.heading('c1', text='方案')
        self.tree4.heading('c2', text='空調主機')
        self.tree4.heading('c3', text='最大空調容量(USRT)')
        self.tree4.heading('c4', text='主機效率係數')
        self.tree4.heading('c5', text='熱源系統功率比PRs')
        self.tree4.heading('c6', text='送風系統功率比PRf')
        self.tree4.heading('c7', text='送水系統功率比PRp')
        self.tree4.heading('c8', text='冰水主機台數控制系統')
        self.tree4.heading('c9', text='儲冰空調系統')
        self.tree4.heading('c10', text='吸收式或熱泵式冷凍機')
        self.tree4.heading('c11', text='變冷媒量熱源VRV')
        self.tree4.heading('c12', text='變頻主機')
        self.tree4.heading('c13', text='CO2濃度外氣量控制系統')
        self.tree4.heading('c14', text='全熱交換器系統')
        self.tree4.heading('c15', text='外氣冷房系統')
        self.tree4.heading('c16', text='空調風扇並用系統')
        self.tree4.heading('c17', text='送風系統節能技術')
        self.tree4.heading('c18', text='送水系統-一次冰水變頻系統')
        self.tree4.heading('c19', text='送水系統-變頻無段變速')
        self.tree4.heading('c20', text='送水系統-冰水泵台數控制')
        self.tree4.heading('c21', text='再生能源節能比例(%)')
        self.tree4.heading('c22', text='建築能源管理系統效率(Beta2)')
        self.tree4.heading('c23', text='指標得分')
        self.tree4.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar6.config(command=self.tree4.yview)
        self.scrollBar7.config(command=self.tree4.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree4.insert("","end",values=row)
    def close_window4(self):
            self.master.destroy()

"""--------------------------------------CO2減量--------------------------------------"""
class windowclass4(tk.Frame):
    
    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton5 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window5)
        self.quitButton5.place(x=400,y=250)
        self.frame5 = tk.Frame(master)
        self.frame5.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar8 = Scrollbar(self.frame5)
        self.scrollBar8.pack(side=RIGHT, fill=Y,)
        self.scrollBar9 = Scrollbar(self.frame5,orient=HORIZONTAL)
        self.scrollBar9.pack(side=BOTTOM, fill=X)

        self.tree5 = ttk.Treeview(self.frame5,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14'),
                    show="headings",
                    yscrollcommand=self.scrollBar8.set,
                    xscrollcommand=self.scrollBar9.set)
                
        #设置每列宽度和对齐方式
        self.tree5.column('c1', width=100, anchor='center')
        self.tree5.column('c2', width=150, anchor='center')
        self.tree5.column('c3', width=150, anchor='center')
        self.tree5.column('c4', width=150, anchor='center')
        self.tree5.column('c5', width=150, anchor='center')
        self.tree5.column('c6', width=180, anchor='center')
        self.tree5.column('c7', width=100, anchor='center')
        self.tree5.column('c8', width=100, anchor='center')
        self.tree5.column('c9', width=100, anchor='center')
        self.tree5.column('c10', width=100, anchor='center')
        self.tree5.column('c11', width=100, anchor='center')
        self.tree5.column('c12', width=100, anchor='center')
        self.tree5.column('c13', width=100, anchor='center')
        self.tree5.column('c14', width=100, anchor='center')

        #设置每列表头标题文本
        self.tree5.heading('c1', text='方案')
        self.tree5.heading('c2', text='構造形式')
        self.tree5.heading('c3', text='隔間牆形式')
        self.tree5.heading('c4', text='外牆形式')
        self.tree5.heading('c5', text='預鑄整體衛浴')
        self.tree5.heading('c6', text='耐震力升級設計')
        self.tree5.heading('c7', text='RC梁柱保護層增加量')
        self.tree5.heading('c8', text='RC樓版保護層增加量')
        self.tree5.heading('c9', text='屋頂防水層')
        self.tree5.heading('c10', text='空調設備管路')
        self.tree5.heading('c11', text='給排水衛生設備管路')
        self.tree5.heading('c12', text='電器通信線路')
        self.tree5.heading('c13', text='再生建材使用係數')
        self.tree5.heading('c14', text='指標得分')
        self.tree5.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar8.config(command=self.tree5.yview)
        self.scrollBar9.config(command=self.tree5.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree5.insert("","end",values=row)

    def close_window5(self):
            self.master.destroy()

"""--------------------------------------基地保水--------------------------------------"""
class windowclass5(tk.Frame):

    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton6 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window6)
        self.quitButton6.place(x=400,y=250)
        self.frame6 = tk.Frame(master)
        self.frame6.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar10 = Scrollbar(self.frame6)
        self.scrollBar10.pack(side=RIGHT, fill=Y,)
        self.scrollBar11 = Scrollbar(self.frame6,orient=HORIZONTAL)
        self.scrollBar11.pack(side=BOTTOM, fill=X)

        self.tree6 = ttk.Treeview(self.frame6,
                    columns=('c1','c2','c3','c4','c5','c6','c7'),
                    show="headings",
                    yscrollcommand=self.scrollBar10.set,
                    xscrollcommand=self.scrollBar11.set)
                
        #设置每列宽度和对齐方式
        self.tree6.column('c1', width=100, anchor='center')
        self.tree6.column('c2', width=150, anchor='center')
        self.tree6.column('c3', width=150, anchor='center')
        self.tree6.column('c4', width=150, anchor='center')
        self.tree6.column('c5', width=150, anchor='center')
        self.tree6.column('c6', width=180, anchor='center')
        self.tree6.column('c7', width=100, anchor='center')

        #设置每列表头标题文本
        self.tree6.heading('c1', text='方案')
        self.tree6.heading('c2', text='保水設計方法')
        self.tree6.heading('c3', text='設計變數1')
        self.tree6.heading('c4', text='設計值1')
        self.tree6.heading('c5', text='設計變數2')
        self.tree6.heading('c6', text='設計值2')
        self.tree6.heading('c7', text='指標得分')
        self.tree6.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar10.config(command=self.tree6.yview)
        self.scrollBar11.config(command=self.tree6.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree6.insert("","end",values=row)

    def close_window6(self):
            self.master.destroy()

"""-------------------------------------綠化設計--------------------------------------"""
class windowclass6(tk.Frame):

    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton7 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window7)
        self.quitButton7.place(x=400,y=250)
        self.frame7 = tk.Frame(master)
        self.frame7.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar12 = Scrollbar(self.frame7)
        self.scrollBar12.pack(side=RIGHT, fill=Y,)
        self.scrollBar13 = Scrollbar(self.frame7,orient=HORIZONTAL)
        self.scrollBar13.pack(side=BOTTOM, fill=X)

        self.tree7 = ttk.Treeview(self.frame7,
                    columns=('c1','c2','c3','c4','c5','c6'),
                    show="headings",
                    yscrollcommand=self.scrollBar12.set,
                    xscrollcommand=self.scrollBar13.set)
                
        #设置每列宽度和对齐方式
        self.tree7.column('c1', width=100, anchor='center')
        self.tree7.column('c2', width=150, anchor='center')
        self.tree7.column('c3', width=150, anchor='center')
        self.tree7.column('c4', width=150, anchor='center')
        self.tree7.column('c5', width=150, anchor='center')
        self.tree7.column('c6', width=180, anchor='center')

        #设置每列表头标题文本
        self.tree7.heading('c1', text='方案')
        self.tree7.heading('c2', text='植栽位置')
        self.tree7.heading('c3', text='植栽種類')
        self.tree7.heading('c4', text='植栽面積(平方公尺)')
        self.tree7.heading('c5', text='原生或誘鳥誘蝶植物比例(%)')
        self.tree7.heading('c6', text='指標得分')
        self.tree7.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar12.config(command=self.tree7.yview)
        self.scrollBar13.config(command=self.tree7.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree7.insert("","end",values=row)

    def close_window7(self):
            self.master.destroy()

"""--------------------------------------室內環境--------------------------------------"""
class windowclass7(tk.Frame):
    
    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton8 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window8)
        self.quitButton8.place(x=400,y=250)
        self.frame8 = tk.Frame(master)
        self.frame8.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar14 = Scrollbar(self.frame8)
        self.scrollBar14.pack(side=RIGHT, fill=Y,)
        self.scrollBar15 = Scrollbar(self.frame8,orient=HORIZONTAL)
        self.scrollBar15.pack(side=BOTTOM, fill=X)

        self.tree8 = ttk.Treeview(self.frame8,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10'),
                    show="headings",
                    yscrollcommand=self.scrollBar14.set,
                    xscrollcommand=self.scrollBar15.set)
                
        #设置每列宽度和对齐方式
        self.tree8.column('c1', width=100, anchor='center')
        self.tree8.column('c2', width=150, anchor='center')
        self.tree8.column('c3', width=150, anchor='center')
        self.tree8.column('c4', width=150, anchor='center')
        self.tree8.column('c5', width=150, anchor='center')
        self.tree8.column('c6', width=180, anchor='center')
        self.tree8.column('c7', width=100, anchor='center')
        self.tree8.column('c8', width=100, anchor='center')
        self.tree8.column('c9', width=100, anchor='center')
        self.tree8.column('c10', width=100, anchor='center')
        #设置每列表头标题文本
        self.tree8.heading('c1', text='方案')
        self.tree8.heading('c2', text='外牆厚度')
        self.tree8.heading('c3', text='窗厚度')
        self.tree8.heading('c4', text='樓版厚度')
        self.tree8.heading('c5', text='可見光透光率')
        self.tree8.heading('c6', text='人工照明狀況')
        self.tree8.heading('c7', text='建築裝修量')
        self.tree8.heading('c8', text='綠建材使用率')
        self.tree8.heading('c9', text='生態建材項目')
        self.tree8.heading('c10', text='指標得分')
        self.tree8.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar14.config(command=self.tree8.yview)
        self.scrollBar15.config(command=self.tree8.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree8.insert("","end",values=row)

    def close_window8(self):
            self.master.destroy()
            
"""--------------------------------------污水垃圾--------------------------------------"""
class windowclass8(tk.Frame):

    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton9 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window9)
        self.quitButton9.place(x=400,y=250)
        self.frame9 = tk.Frame(master)
        self.frame9.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar16 = Scrollbar(self.frame9)
        self.scrollBar16.pack(side=RIGHT, fill=Y,)
        self.scrollBar17 = Scrollbar(self.frame9,orient=HORIZONTAL)
        self.scrollBar17.pack(side=BOTTOM, fill=X)

        self.tree9 = ttk.Treeview(self.frame9,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13'),
                    show="headings",
                    yscrollcommand=self.scrollBar16.set,
                    xscrollcommand=self.scrollBar17.set)
                
        #设置每列宽度和对齐方式
        self.tree9.column('c1', width=100, anchor='center')
        self.tree9.column('c2', width=150, anchor='center')
        self.tree9.column('c3', width=150, anchor='center')
        self.tree9.column('c4', width=150, anchor='center')
        self.tree9.column('c5', width=150, anchor='center')
        self.tree9.column('c6', width=180, anchor='center')
        self.tree9.column('c7', width=100, anchor='center')
        self.tree9.column('c8', width=100, anchor='center')
        self.tree9.column('c9', width=100, anchor='center')
        self.tree9.column('c10', width=100, anchor='center')
        self.tree9.column('c11', width=100, anchor='center')
        self.tree9.column('c12', width=100, anchor='center')
        self.tree9.column('c13', width=100, anchor='center')
        #设置每列表头标题文本
        self.tree9.heading('c1', text='方案')
        self.tree9.heading('c2', text='措施1：當地政府設有垃圾不落地等清運系統，無須設置專用垃圾集中場及密閉式垃圾箱者')
        self.tree9.heading('c3', text='措施2：設有廚餘收集處理再利用設施並於基地內確實執行資源化再利用者(必須有發酵、乾燥處理相關計畫書及設備說明，限已完工建築申請)')
        self.tree9.heading('c4', text='措施3：設有廚餘集中收集設施並定期委外清運處理，但無當地資源化再利用者')
        self.tree9.heading('c5', text='措施4：設有落葉堆肥處理再利用系統者(必須有絞碎、翻堆、發酵處理相關計畫書及設備說明，限已完工建築申請)')
        self.tree9.heading('c6', text='措施5：設置冷藏、冷凍或壓縮等垃圾前置處理設施者')
        self.tree9.heading('c7', text='措施6：設有空間充足且運出動線說明合理之專用垃圾集中場(運出路徑必須有明確之圖示)')
        self.tree9.heading('c8', text='措施7：專用垃圾集中場有綠化、美化或景觀化的設計處理者')
        self.tree9.heading('c9', text='措施8：設置具體執行資源垃圾分類回收系統並有確實執行成效者')
        self.tree9.heading('c10', text='措施9：設置防止動物咬食且衛生可靠的密閉式垃圾箱者')
        self.tree9.heading('c11', text='措施10：垃圾集中場有定期清洗及衛生消毒且現場長期維持良好者（限已完工建築申請')
        self.tree9.heading('c12', text='措施11：集合住宅大樓設有公共燒香燒金銀紙的空間及固定專用焚燒設備者')
        self.tree9.heading('c13', text='得分')
        self.tree9.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar16.config(command=self.tree9.yview)
        self.scrollBar17.config(command=self.tree9.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree9.insert("","end",values=row)

    def close_window9(self):
            self.master.destroy()

"""--------------------------------------廢棄物減量--------------------------------------"""
class windowclass9(tk.Frame):
    
    tempList = []
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton10 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window10)
        self.quitButton10.place(x=400,y=250)
        self.frame10 = tk.Frame(master)
        self.frame10.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar18 = Scrollbar(self.frame10)
        self.scrollBar18.pack(side=RIGHT, fill=Y,)
        self.scrollBar19 = Scrollbar(self.frame10,orient=HORIZONTAL)
        self.scrollBar19.pack(side=BOTTOM, fill=X)

        self.tree10 = ttk.Treeview(self.frame10,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11'),
                    show="headings",
                    yscrollcommand=self.scrollBar18.set,
                    xscrollcommand=self.scrollBar19.set)
                
        #设置每列宽度和对齐方式
        self.tree10.column('c1', width=100, anchor='center')
        self.tree10.column('c2', width=150, anchor='center')
        self.tree10.column('c3', width=150, anchor='center')
        self.tree10.column('c4', width=150, anchor='center')
        self.tree10.column('c5', width=150, anchor='center')
        self.tree10.column('c6', width=180, anchor='center')
        self.tree10.column('c7', width=100, anchor='center')
        self.tree10.column('c8', width=100, anchor='center')
        self.tree10.column('c9', width=100, anchor='center')
        self.tree10.column('c10', width=100, anchor='center')
        self.tree10.column('c11', width=100, anchor='center')
        #设置每列表头标题文本
        self.tree10.heading('c1', text='方案')
        self.tree10.heading('c2', text='構造形式')
        self.tree10.heading('c3', text='系統模版')
        self.tree10.heading('c4', text='預鑄外牆')
        self.tree10.heading('c5', text='預鑄梁柱')
        self.tree10.heading('c6', text='預鑄樓版')
        self.tree10.heading('c7', text='預鑄浴廁')
        self.tree10.heading('c8', text='乾式隔間')
        self.tree10.heading('c9', text='粒狀污染物防制效率')
        self.tree10.heading('c10', text='再生建材使用率')
        self.tree10.heading('c11', text='指標得分')
        self.tree10.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar18.config(command=self.tree10.yview)
        self.scrollBar19.config(command=self.tree10.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree10.insert("","end",values=row)

    def close_window10(self):
            self.master.destroy()

"""--------------------------------------廢棄物減量--------------------------------------"""
class windowclass10(tk.Frame):

    
    tempList = []
    def __init__(self , master):
        
        tk.Frame.__init__(self, master)
        master.title("結果")
        self.master.geometry("1000x800")
        self.quitButton11 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window11)
        self.quitButton11.place(x=400,y=250)
        self.frame11 = tk.Frame(master)
        self.frame11.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar20 = Scrollbar(self.frame11)
        self.scrollBar20.pack(side=RIGHT, fill=Y,)
        self.scrollBar21 = Scrollbar(self.frame11,orient=HORIZONTAL)
        self.scrollBar21.pack(side=BOTTOM, fill=X)

        self.tree11 = ttk.Treeview(self.frame11,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17','c18','c19','c20','c21'),
                    show="headings",
                    yscrollcommand=self.scrollBar20.set,
                    xscrollcommand=self.scrollBar21.set)
                
        #设置每列宽度和对齐方式
        self.tree11.column('c1', width=100, anchor='center')
        self.tree11.column('c2', width=150, anchor='center')
        self.tree11.column('c3', width=150, anchor='center')
        self.tree11.column('c4', width=150, anchor='center')
        self.tree11.column('c5', width=150, anchor='center')
        self.tree11.column('c6', width=180, anchor='center')
        self.tree11.column('c7', width=100, anchor='center')
        self.tree11.column('c8', width=100, anchor='center')
        self.tree11.column('c9', width=100, anchor='center')
        self.tree11.column('c10', width=100, anchor='center')
        self.tree11.column('c11', width=100, anchor='center')
        self.tree11.column('c12', width=100, anchor='center')
        self.tree11.column('c13', width=100, anchor='center')
        self.tree11.column('c14', width=100, anchor='center')
        self.tree11.column('c15', width=100, anchor='center')
        self.tree11.column('c16', width=100, anchor='center')
        self.tree11.column('c17', width=100, anchor='center')
        self.tree11.column('c18', width=100, anchor='center')
        self.tree11.column('c19', width=100, anchor='center')
        self.tree11.column('c20', width=100, anchor='center')
        self.tree11.column('c21', width=100, anchor='center')
        #设置每列表头标题文本
        self.tree11.heading('c1', text='方案')
        self.tree11.heading('c2', text='項目1:無設置大便器')
        self.tree11.heading('c3', text='項目2:無省水標章的馬桶之採用率(%)')
        self.tree11.heading('c4', text='項目3:具省水標章的一段式馬桶或單段式省水型沖水閥式便器之採用率(%)')
        self.tree11.heading('c5', text='項目4:具省水標章的兩段式馬桶(大號9公升/小號4.5公升以下)或兩段式省水型沖水閥式便器之採用率(%)')
        self.tree11.heading('c6', text='項目5:具省水標章的兩段式馬桶(大號6公升/小號3公升以下)之採用率(%)')
        self.tree11.heading('c7', text='項目6:無設置小便器')
        self.tree11.heading('c8', text='項目7:無自動感應沖便器且無節水沖洗設計之小便器採用率(%)')
        self.tree11.heading('c9', text='項目8:自動感應沖便器或有節水沖洗設計之小便器採用率(%)')
        self.tree11.heading('c10', text='項目9:無設置水拴或全部為免評估之水拴')
        self.tree11.heading('c11', text='項目10:水拴無省水標章且無裝置省水閥、節流器、起泡器等省水配件或器材者之採用率(%)')
        self.tree11.heading('c12', text='項目11:水拴具省水標章或裝置省水閥、節流器、起泡器等省水配件或器材之採用率(%)')
        self.tree11.heading('c13', text='項目12:自動感應水拴或自閉式水拴之採用率(%)')
        self.tree11.heading('c14', text='項目13:浴缸或淋浴設備')
        self.tree11.heading('c15', text='項目14:私人用按摩浴缸或豪華型SPA淋浴設備之浴室單元比例')
        self.tree11.heading('c16', text='具有大耗水項目─ 親水設施面積達100平方公尺以上')
        self.tree11.heading('c17', text='具有大耗水項目─ 具有私人用按摩浴缸或豪華型SPA淋浴設備1處以上')
        self.tree11.heading('c18', text='具有大耗水項目─ 屬於大規模開發案例')
        self.tree11.heading('c19', text='具有大耗水項目之彌補措施')
        self.tree11.heading('c20', text='雨水貯集措施體積(立方公尺)')
        self.tree11.heading('c21', text='得分')
        self.tree11.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar20.config(command=self.tree11.yview)
        self.scrollBar21.config(command=self.tree11.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "' + XX + '" where "' + YY + '"="' + ZZ + '"'

        curr.execute(sql)
        rows=curr.fetchall()

        for tup in rows:
            self.tempList.append(tup[0])


        for row in rows:
            self.tree11.insert("","end",values=row)        

    def close_window11(self):
            self.master.destroy()

class windowclass12(tk.Frame):
    
    tempList = []
    tup_list=[]
    def __init__(self , master):
        tk.Frame.__init__(self, master)
        master.title("外殼節能")
        self.master.geometry("1000x800")
        self.quitButton12 = tk.Button(master, text = 'Quit', width = 25 , command = self.close_window12)
        self.quitButton12.place(x=400,y=250)
        self.frame12 = tk.Frame(master)
        self.frame12.place(x=0, y=25, width=800, height=750)

        #滚动条
        self.scrollBar22 = Scrollbar(self.frame12)
        self.scrollBar22.pack(side=RIGHT, fill=Y,)
        self.scrollBar23 = Scrollbar(self.frame12,orient=HORIZONTAL)
        self.scrollBar23.pack(side=BOTTOM, fill=X)

        self.tree12 = ttk.Treeview(self.frame12,
                    columns=('c1','c2','c3','c4','c5','c6','c7','c8','c9'),
                    show="headings",
                    yscrollcommand=self.scrollBar22.set,
                    xscrollcommand=self.scrollBar23.set)
                
        #设置每列宽度和对齐方式
        self.tree12.column('c1', width=100, anchor='center')
        self.tree12.column('c2', width=150, anchor='center')
        self.tree12.column('c3', width=150, anchor='center')
        self.tree12.column('c4', width=150, anchor='center')
        self.tree12.column('c5', width=150, anchor='center')
        self.tree12.column('c6', width=180, anchor='center')
        self.tree12.column('c7', width=100, anchor='center')
        self.tree12.column('c8', width=100, anchor='center')
        self.tree12.column('c9', width=100, anchor='center')


        #设置每列表头标题文本
        self.tree12.heading('c1', text='方案')
        self.tree12.heading('c2', text='屋頂材質')
        self.tree12.heading('c3', text='外牆材質')
        self.tree12.heading('c4', text='開窗率(%)')
        self.tree12.heading('c5', text='玻璃熱傳透率')
        self.tree12.heading('c6', text='玻璃外遮陽x日射透過率')
        self.tree12.heading('c7', text='總立面開窗面積')
        self.tree12.heading('c8', text='總立面實牆面積')
        self.tree12.heading('c9', text='指標得分')

        
        self.tree12.pack(side=LEFT, fill=Y)
                
        #Treeview组件与垂直滚动条结合

        self.scrollBar22.config(command=self.tree12.yview)
        self.scrollBar23.config(command=self.tree12.xview)
        
        #插入演示数据
        conndb = sqlite3.connect(database_path)
        curr = conndb.cursor()
        sql = 'select * from "外殼節能" where "方案"= "1" or "方案"= "2" '

        curr.execute(sql)
        rows=curr.fetchall()

        for r in rows:
            self.tree12.insert("","end",values=r)            

    def close_window12(self):
            self.master.destroy()



if __name__ == "__main__":
    #menubar = Menu(root)
    
    #filemenu = Menu(menubar, tearoff=0)
    #filemenu.add_command(label="LEED", command = set_db1)
    #filemenu.add_command(label="LEED")

    #submenu = Menu(filemenu)
    #"""
    #submenu.add_command(label="照明節能")
    #submenu.add_command(label="空調節能")
    #submenu.add_command(label="外牆節能")
    #"""
    #filemenu.add_cascade(label='EEWH', underline=0 , command = set_db2)
    #filemenu.add_cascade(label='EEWH', underline=0)
    #filemenu.add_separator()

    #filemenu.add_command(label="Exit")
    #menubar.add_cascade(label="System", menu=filemenu)
    #editmenu = Menu(menubar, tearoff=0)


    #editmenu.add_separator()
    #root.config(menu=menubar)

    XX = 'None!'
    YY = 'None!'
    ZZ = 'None!'
    root = tk.Tk()	
    app=windowclass(root)  #建立一個實體
    app.mainloop()   #呈現它