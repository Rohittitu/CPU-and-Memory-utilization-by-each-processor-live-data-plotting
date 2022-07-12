"""
Created on Tue July 19 22:47:19 2020
UI: It will provide the users to control this script.
@author: RSuman(Rohit Suman)

"""

import tkinter
from tkinter import *
import numpy as np
import data_process
from data_process import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import concurrent.futures
from data_process import Data as DATA
import tkMessageBox
from playsound import playsound

style.use("ggplot")
Data=DATA()

class App(Frame):

    def __init__(self, master):
        
        self.x_data         = []
        self.y_data         = []
        self.y_data1        = []
        self.details        = StringVar()
        self.display        = StringVar()
        self.entery_        = StringVar()
        self.threshold_value= IntVar()
        self.enable_PopCheck= IntVar()
        self.enable_logg    = IntVar()
        
        
        self.display.set("logs here")
        self.details.set("Details")
        self.entery_.set("Please Enter Threshod Value of CPU: ")
        self.threshold_value.set(0)

        
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 300)
        self.ax.set_ylim(0, 400)
        self.line,  = self.ax.plot(0, 0, label="CPU Used")
        self.line1, = self.ax.plot(0, 0, label="Memory Used in %")
        self.ax.set_title('Total CPU and Memory Utilization')
        self.ax.legend()
        
        self.mainframe              = Frame(master, height=650, width=1200)
        self.get_log_btn            = Button(self.mainframe, text="Get Logs",command= Data.log_saving_using_thread, bg='green', width=16,bd=4, relief='ridge', font=('Helvetica', 11, 'bold'), height=1)
        self.frame_info             = Text(self.mainframe, height=30, width=40, bg='khaki', bd=4, fg='black', selectbackground='red', font=('Helvetica', 9, 'bold'))
        self.vscroll                = Scrollbar(self.mainframe, orient=VERTICAL, command=self.frame_info.yview)
        self.frame_info['yscroll']  = self.vscroll.set
        self.canvas                 = FigureCanvasTkAgg(self.fig, self.mainframe, )
        self.entery_label           = Label(self.mainframe, textvariable=self.entery_,)#font=('Helvetica', 13, 'bold'))
        self.threshold_entery_value = Entry(self.mainframe,bd =3,textvariable= self.threshold_value, font=('Helvetica', 10),width=10)
        self.enable_pop_up_checkbox = Checkbutton(self.mainframe, text = "Enable Alert Tone, When CPU Used > Threshold CPU Used", variable = self.enable_PopCheck,onvalue = 1,offvalue = 0, height=2)
        self.enable_logging         = Checkbutton(self.mainframe, text = "Enable Logging", variable = self.enable_logg,onvalue = 1,offvalue = 0,command=self.logging_function, height=2)
        self.total_deatils          = Label(self.mainframe, textvariable=self.details, bg="LightBlue",font=('Helvetica', 13, 'bold'))
        #self.canvas.show()
        #self.toolbar= NavigationToolbar2TkAgg(self.canvas, self.mainframe)
        #self.toolbar.update()
        
        self.total_deatils = Label(self.mainframe, textvariable=self.details, bg="LightBlue",font=('Helvetica', 13, 'bold'))

        
        self.mainframe.pack()
        self.frame_info.place(x=900, y=170)
        self.get_log_btn.place(x=700, y=160)
        self.vscroll.place(x=1177, y=170, height=460)
        self.canvas.get_tk_widget().place(x=50, y=50)
        self.total_deatils.place(x=50, y=560)
        #self.canvas._tkcanvas.pack()
        self.entery_label.place(x=700, y=50)
        self.threshold_entery_value.place(x=920, y=50)
        self.enable_pop_up_checkbox.place(x=700, y=80)
        self.enable_logging.place(x=700, y=110)
        self.mainframe.rowconfigure(5, weight=1, uniform=0)
        self.mainframe.columnconfigure((0, 1), weight=1, uniform=0)
        
        threading.Thread(target=Data.log_mangment).start()
        #threading.Thread(target=Data.modified_data).start()
        #threading.Thread(target=Data.get_ideal_cpu_percent).start()
        threading.Thread(target=Data.run).start()
        
        tt = threading.Thread(target=self.always)
        tt.start()
       
    def anni(self, i):
        self.x_data.append(i)
        data = top_data.get()
        self.y_data.append(data[0])
        self.y_data1.append(data[1])
        self.details.set("TOTAL CPU USED: " + str(data[0]) + "\n TOTAL MEMORY USED: " + str(data[1]) + " %")
        if (self.enable_PopCheck.get()==1):
            if( data[0] > self.threshold_value.get() ):
                #self.infop("CPU used value is more than Threshold Value")
                self.infop()
                
        self.line.set_xdata(self.x_data)
        self.line.set_ydata(self.y_data)
        self.line1.set_xdata(self.x_data)
        self.line1.set_ydata(self.y_data1)
        if i % 250 == 0:
            self.ax.set_xlim(i, i + 300)
        return self.line, self.line1


    def always(self):
        while True:
            if not (qq2.empty()):
                val = str(qq2.get())
                self.frame_info.delete(1.0, END)
                self.display.set(val)
                self.frame_info.delete(1.0, END)
                self.frame_info.insert('1.0', self.display.get())
                
    def infop(self):#,infor):
        #action=tkMessageBox.showinfo("Instructions",infor)
        #return action
        threading.Thread(target=playsound, args=(r"caralarm_M15p3r02.mp3",)).start()
        


    def logging_function(self):
        
        if(self.enable_logg.get()==1):
            self.get_log_btn["state"]= "disable"
            threading.Thread(target=Data.current_file_log).start()
            Data.delete_all_log()
            

        if(self.enable_logg.get()==0):
            self.get_log_btn["state"]= "normal"
            threading.Thread(target=Data.log_mangment).start()
            
            
            
        
            
            


root=Tk()
root.title("CPU and Memory Utilization live graph")    
app = App(root)
ann = FuncAnimation(app.fig, func=app.anni, frames=np.arange(0, 86400, 1), interval=2000)
root.mainloop()
