"""
Created on Tue July 17 23:47:19 2020
UI: It will fetch the data from the ADB connection and send the data to UI programe.
Also it will be used to handel the logging functionalitied from backend side
@author: RSuman (Rohit Suman)
"""
from typing import List, Any

#import matplotlib.pyplot as plt
import os, time
import re
from datetime import datetime
import Queue, threading
import numpy as np
import math

global qq2, top_data, cpu_list, Memory_list, logs_queue2

qq2 = Queue.Queue()
logs_queue = Queue.Queue()
top_data = Queue.Queue()
logs_queue2= Queue.Queue()

cpu_list = []
Memory_list = []


def linedivision(sig):
    # for getting all the lines
    lines = []
    j = 0
    i = 0
    k = len(sig)
    if ('\n' in sig):
        while (i < len(sig)):
            if (sig[i] == '\n'):
                line = sig[j:i]
                lines.append(line)
                j = i + 1
            i = i + 1
        line = sig[j:k]
        lines.append(line)
    else:
        line = sig
        lines.append(line)
    return lines


class Data():
    
    def get_ideal_cpu_percent(self):
        getting_cpu_deatils = os.popen('adb shell top -n 1')
        top_res = getting_cpu_deatils.read()
        if (top_res == ""):

            print("ADB connection failed")
            top_data.put([0, 0])
            cpu_list.append(0)
            Memory_list.append(0)
        else:
            each_line_of_response = linedivision(top_res)
            idel_cpu_wrd = each_line_of_response[3].split()[4]
            total_cpu_word = each_line_of_response[3].split()[0]
                
            ideal_cpu = int(re.search(r'\d+', idel_cpu_wrd).group())
            total_cpu = int(re.search(r'\d+', total_cpu_word).group())
                
            total_memory = int(re.search(r'\d+', each_line_of_response[1].split()[1]).group())
            free_memory = int(re.search(r'\d+', each_line_of_response[1].split()[5]).group())
            if(free_memory==0):
                free_memory_percent=0
            else:
                free_memory_percent = round(((float(free_memory)) / total_memory) * 100, 2)
                # print(free_memory_percent, ideal_cpu)
            used_cpu = total_cpu - ideal_cpu
            used_memory = 100 - free_memory_percent
            top_data.put([used_cpu, used_memory])
            print([used_cpu, used_memory])
            


    def modified_data(self):
        
        """Getting ECUS time and Date"""
        get_device_time = os.popen('adb shell date')
        device_time = get_device_time.read()
        if (device_time == ''):
            device_time = "ADB connection failed"

        """Getting Memory utilization info"""
        mem = os.popen("adb shell cat /proc/meminfo")
        get_mem = mem.read()
        if (get_mem == ''):
            get_mem = "ADB connection failed"

        """Getting the CPU utilization from the ECU bassed on each Process"""
        stream = os.popen('adb shell ps -eA -o PID,PPID,CPU,PCPU,%MEM,NAME')
        output = stream.read()
        if (output == ''):
            output = "ADB connection failed"
        qq2.put(device_time + "\n" + output + "\n" + get_mem + "\n\n")
            
        if(self.Default_logging_flag):
            logs_queue.put(device_time + "\n" + output + "\n" + get_mem + "\n\n")
        else:
            logs_queue2.put(device_time + "\n" + output + "\n" + get_mem + "\n\n")
            
    def run(self):
        while True:
            self.get_ideal_cpu_percent()
            self.modified_data()
        

    def log_mangment(self):
        self.Default_logging_flag= True
        #print(self.Default_logging_flag)
        while True:
            time.sleep(1)
            if (logs_queue.qsize() > 500):
                Deleting_val = logs_queue.get()
                print("Deleting older data")
            else:
                pass
            if(self.Default_logging_flag==False):
                break
            

    def delete_all_log(self):
        if(not logs_queue.empty()):
            with logs_queue.mutex:
                logs_queue.queue.clear()

                

    def current_file_log(self):
        self.Default_logging_flag=False
        file_name= (str(datetime.now()).replace(":", "") + ".txt")
        log_file = open(file_name, "w")
        log_file.close()
        while(True):
            if(not logs_queue2.empty()):
                log_fil= open(file_name, "a")
                log_fil.write(logs_queue2.get())
                log_fil.close()
                if (self.Default_logging_flag):
                    break


            

    def log_Saveing(self):
        file = open(str(datetime.now()).replace(":", "") + ".txt", "w")
        while (not logs_queue.empty()):
            file.write(logs_queue.get())
        cpu_data = cpu_list[:]
        Memory_data = Memory_list[:]



    def log_saving_using_thread(self):
        log_save = threading.Thread(target=self.log_Saveing)
        log_save.start()



