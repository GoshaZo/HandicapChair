import serial
import tkinter as tk
import random
import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import time
from datetime import datetime
import csv
import math

def linearisation(tasklist):
    tasklist[5] = 11.06*tasklist[5]+1.408 #y = 11.06x + 1.408
    tasklist[6] = 11.06*tasklist[6]+1.408
    tasklist[3] = math.exp((tasklist[3]+1.5944)/0.722) #y = 0.722ln(x) - 1.5944
    tasklist[4] = math.exp((tasklist[4]+1.5944)/0.722)

def writetofile(seq,title,timestr):
    pass
    # try:
    #     seq.insert(0, str(title))
    #     seq.insert(0, timestr)
    # except:
    #     seq=[seq]
    #     seq.insert(0, str(title))
    #     seq.insert(0, timestr)
    # seq = seq + [0] * (72 - len(seq))
    # with open('data from '+timestr[0:10]+' data.csv', 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(seq)

def back_ground(val):
    color = ["#FF0000", "#FF5000", "#FF7500", "#FFA000", "#FFC500", "#FFEA00", "#FFF100", "#CBFF00", "#71FF00",
             "#00FF00"]
    try:
        for index in range(10):
            if int(val) < 200 * (index + 1):
                return color[-(index + 1)]
        return color[0]
    except:
        return "#808080"

window = tk.Tk()
# window.geometry("800x1000")

#7 - tusik
#4 - low back
#5 - up back
#3 - right
#6 - left

ser3 = serial.Serial(
    port='COM5',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

print("connected to: " + ser3.portstr)

ser1 = serial.Serial(
    port='COM6',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

print("connected to: " + ser1.portstr)

ser2 = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

print("connected to: " + ser2.portstr)

ser = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

print("connected to: " + ser.portstr)

ser5 = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None)

print("connected to: " + ser5.portstr)

ser1index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 33, 34, 35, 36,
             37, 38]
ser2index = [2, 3, 4, 8, 9, 13, 14, 19, 24]
ser5index = [0, 1, 5, 6, 10, 11, 12, 15, 16, 17, 20, 21, 22, 25, 26, 27, 30, 31, 32, 35, 36, 37, 40, 41, 42, 45, 46, 47,
             50, 51, 52]
sensorname = ['ang1', 'ang2', 'ang3', 'R.knee', 'L.knee', 'R.stret', 'L.stret', 'R.x', 'R.y', 'L.x', 'L.y']
seq = []
seq1 = []
seq2 = []
seq5 = []
count = 1
tasklist = []
flag: int = 0
labels = []
labels1 = []
labels2 = []
labels3 = []
labels4 = []
labels5 = []
labelssensor = []
h = 1
w = 5
bw = 2
oldtime = time.time()
z=0

def stop():
    global status
    status = True
    ser.reset_input_buffer()
    ser1.reset_input_buffer()
    ser2.reset_input_buffer()
    ser3.reset_input_buffer()
    ser5.reset_input_buffer()
    seq.clear()
    seq1.clear()
    seq2.clear()
    seq3.clear()
    seq5.clear()
    window.destroy()



status = False
while True:
    # try:
    #     print("--- %.2f seconds ---" % (time.time() - start_time))
    # except:
    #     pass
    # start_time = time.time()
    if status:
        print('break')
        break
    # a = ser.read_until(b'#')
    b = ser.read_until(b'\x00')
    d = ser.read_until(b'#')
    try:
        c = d.decode('ascii', 'ignore')
    except:
        print('error')
        d = ser.read_until(b'#')
        c = d.decode('ascii', 'ignore')
    string = str(d)
    seq = string.split(',')
    if seq[0][-1] == '0' and seq[0][-2] == '0' and seq[0][-3] == '0':
        seq[0] = '0'
    else:
        seq[0] = seq[0][seq[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq[-1] = seq[-1][:-2]
    k = 0
    if flag == 0:
        for i in reversed(range(14)):
            for j in range(5):
                frame = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame.grid(row=j, column=i + 4)
                label = tk.Label(master=frame, text=str(seq[k]), width=w, height=h,
                                 background=back_ground(str(seq[k])))
                label.pack()
                labels.append(label)
                k += 1
        # framen = tk.Frame(
        #     master=window,
        #     relief=tk.FLAT,
        #     borderwidth=bw
        # )
        # framen.grid(row=0, column=18)
        # label = tk.Label(master=framen, text="", width=w, height=h)
        # label.pack()
    else:
        for i in range(14):
            for j in range(5):
                labels[k].configure(text=str(seq[k]), width=w, height=h,
                                    background=back_ground(str(seq[k])))
                k += 1

    ##########################

    # a = ser3.read_until(b'#')
    b = ser3.read_until(b'\x00')
    d = ser3.read_until(b'#')
    try:
        c = d.decode('ascii')
    except:
        print('error')
        b = ser3.read_until(b'\x00')
        d = ser3.read_until(b'#')
        c = d.decode('ascii')
    string = str(d)
    seq3 = string.split(',')
    if seq3[0][-1] == '0' and seq3[0][-2] == '0' and seq3[0][-3] == '0':
        seq3[0] = '0'
    else:
        seq3[0] = seq3[0][seq3[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq3[-1] = seq3[-1][:-2]
    k = 0
    if flag == 0:
        for i in range(14):
            for j in range(5):
                frame3 = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame3.grid(row=j + 6, column=i + 4)
                label = tk.Label(master=frame3, text=str(seq3[k]), width=w, height=h,
                                 background=back_ground(str(seq3[k])))
                label.pack()
                labels3.append(label)
                k += 1
        framen3 = tk.Frame(
            master=window,
            relief=tk.FLAT,
            borderwidth=bw
        )
        framen3.grid(row=11, column=0)
        label = tk.Label(master=framen3, text="", width=w, height=h)
        label.pack()
    else:
        for i in range(14):
            for j in range(5):
                labels3[k].configure(text=str(seq3[k]), width=w, height=h,
                                     background=back_ground(str(seq3[k])))
                k += 1

    ##########################

    # a = ser1.read_until(b'#')
    b = ser1.read_until(b'\x00')
    d = ser1.read_until(b'#')
    while True:
        try:
            c = d.decode('ascii')
            break
        except:
            print('error')
            continue
    string = str(d)
    seq1 = string.split(',')
    if seq1[0][-1] == '0' and seq1[0][-2] == '0' and seq1[0][-3] == '0':
        seq1[0] = '0'
    else:
        seq1[0] = seq1[0][seq1[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq1[-1] = seq1[-1][:-2]
    seq1 = [seq1[x] for x in ser1index]

    # for idx, val in enumerate(seq1):
    #     if int(val) > 1000:
    #         indexlist.append(idx) if idx not in indexlist else indexlist
    # indexlist.sort()
    seq1.insert(9, 'null')
    seq1.insert(10, 'null')
    seq1 = seq1[::-1]
    k = 0
    if flag == 0:
        for i in range(3):
            for j in range(11):
                frame1 = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame1.grid(row=j, column=i)
                try:
                    label = tk.Label(master=frame1, text=str(seq1[k]), width=w, height=h,
                                     background=back_ground(str(seq1[k])))
                except:
                    label = tk.Label(master=frame1, text='none', width=w, height=h, background="#808080")
                label.pack()
                labels1.append(label)
                k += 1
        # framen1 = tk.Frame(
        #     master=window,
        #     relief=tk.FLAT,
        #     borderwidth=bw
        # )
        # framen1.grid(row=0, column=3)
        # label = tk.Label(master=framen1, text="", width=w, height=h)
        # label.pack()
    else:
        for i in range(11):
            for j in range(3):
                labels1[k].configure(text=str(seq1[k]), width=w, height=h,
                                     background=back_ground(str(seq1[k])))
                k += 1
    #########################

    # a = ser2.read_until(b'#')
    b = ser2.read_until(b'\x00')
    d = ser2.read_until(b'#')
    try:
        c = d.decode('ascii')
    except:
        print('error')
        b = ser2.read_until(b'\x00')
        d = ser2.read_until(b'#')
        c = d.decode('ascii')
    string = str(d)
    seq2 = string.split(',')
    if seq2[0][-1] == '0' and seq2[0][-2] == '0' and seq2[0][-3] == '0':
        seq2[0] = '0'
    else:
        seq2[0] = seq2[0][seq2[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq2[-1] = seq2[-1][:-2]
    for k, i in enumerate(ser2index):
        seq2[ser2index[k]] = 'null'
    k = 0
    if flag == 0:
        for i in range(13):
            for j in range(5):
                frame2 = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame2.grid(row=i + 12, column=j + 17)
                try:
                    label = tk.Label(master=frame2, text=str(seq2[k]), width=w, height=h,
                                     background=back_ground(str(seq2[k])))
                except:
                    label = tk.Label(master=frame2, text='none', width=w, height=h, background="#808080")
                label.pack()
                labels2.append(label)
                k += 1
    else:
        for i in range(13):
            for j in range(5):
                labels2[k].configure(text=str(seq2[k]), width=w, height=h,
                                     background=back_ground(str(seq2[k])))
                k += 1
    #############################
    seq2.clear()
    # a = ser2.read_until(b'#')
    b = ser2.read_until(b'\x00')
    d = ser2.read_until(b'#')
    try:
        c = d.decode('ascii')
    except:
        print('error')
        b = ser2.read_until(b'\x00')
        d = ser2.read_until(b'#')
        c = d.decode('ascii')
    string = str(d)
    seq2 = string.split(',')
    if seq2[0][-1] == '0' and seq2[0][-2] == '0' and seq2[0][-3] == '0':
        seq2[0] = '0'
    else:
        seq2[0] = seq2[0][seq2[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq2[-1] = seq2[-1][:-2]
    for k, i in enumerate(ser2index):
        seq2[ser2index[k]] = 'null'
    k = 0
    if flag == 0:
        for i in range(13):
            for j in range(5):
                frame4 = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame4.grid(row=i + 12, column=j)
                try:
                    label = tk.Label(master=frame4, text=str(seq2[k]), width=w, height=h,
                                     background=back_ground(str(seq2[k])))
                except:
                    label = tk.Label(master=frame4, text='none', width=w, height=h, background="#808080")
                label.pack()
                labels4.append(label)
                k += 1

    else:
        for i in range(13):
            for j in range(5):
                labels4[k].configure(text=str(seq2[k]), width=w, height=h,
                                     background=back_ground(str(seq2[k])))
                k += 1

    ############################

    a = ser5.read_until(b'#')
    b = ser5.read_until(b'\x00')
    d = ser5.read_until(b'#')
    try:
        c = d.decode('ascii')
    except:
        print('error')
        b = ser5.read_until(b'\x00')
        d = ser5.read_until(b'#')
        c = d.decode('ascii')
    string = str(d)
    seq5 = string.split(',')
    if seq5[0][-1] == '0' and seq5[0][-2] == '0' and seq5[0][-3] == '0':
        seq5[0] = '0'
        print(seq5)
    else:
        seq5[0] = seq5[0][seq5[0].rfind('\\x00') + 4:]
    # seq1[-1] = seq1[-1].replace('#', '')
    seq5[-1] = seq5[-1][:-2]
    try:
        seq5 = [seq5[x] for x in ser5index]
    except:
        print(seq5)
        break
    seq5.insert(2, 'null')
    seq5.insert(5, 'null')
    # seqtemp = seqtemp[::-1]
    k = 0
    if flag == 0:
        for i in range(11):
            for j in reversed(range(3)):
                frame5 = tk.Frame(
                    master=window,
                    relief=tk.FLAT,
                    borderwidth=bw
                )
                frame5.grid(row=i, column=j + 19)
                try:
                    label = tk.Label(master=frame5, text=str(seq5[k]), width=w, height=h,
                                     background=back_ground(str(seq5[k])))
                except:
                    label = tk.Label(master=frame5, text='none', width=w, height=h, background="#808080")
                label.pack()
                labels5.append(label)
                k += 1


    else:
        for i in range(11):
            for j in reversed(range(3)):
                labels5[k].configure(text=str(seq5[k]), width=w, height=h,
                                     background=back_ground(str(seq5[k])))
                k += 1
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai20", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai21", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai22", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai3", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai4", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai5", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai13", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai6", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai14", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai16", terminal_config=TerminalConfiguration.RSE)
        task.ai_channels.add_ai_voltage_chan("Dev1/ai24", terminal_config=TerminalConfiguration.RSE)
        try:
            tasklist = task.read()
        except:
            tasklist = [0,0,0,0,0,0,0,0,0,0,0]
    linearisation(tasklist)
    if flag == 0:
        for i in range(12):
            framesensorname = tk.Frame(
                master=window,
                relief=tk.FLAT,
                borderwidth=bw
            )
            framesensorname.grid(row=13, column=i + 5)
            try:
                label = tk.Label(master=framesensorname, text=sensorname[i], width=w, height=h,
                                 background='lightblue')
            except:
                label = tk.Label(master=framesensorname, text='', width=w, height=h, background="lightblue")
            label.pack()
        for i in range(12):
            framesensor = tk.Frame(
                master=window,
                relief=tk.FLAT,
                borderwidth=bw
            )
            framesensor.grid(row=14, column=i + 5)
            try:
                label = tk.Label(master=framesensor, text=str(round(tasklist[i], 2)), width=w, height=h,
                                 background='lightblue')
            except:
                label = tk.Label(master=framesensor, text='', width=w, height=h, background="lightblue")
            label.pack()
            labelssensor.append(label)
    else:
        for i in range(11):
            labelssensor[i].configure(text=str(round(tasklist[i], 2)), width=w, height=h,
                                      background='lightblue')

    ############################

    if time.time() - oldtime > 1: #every sec
        oldtime = time.time()
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        dt_object: datetime = datetime.fromtimestamp(timestamp)
        timestr = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        writetofile(seq3, 'upper back',timestr)
        writetofile(seq, 'lower back',timestr)
        writetofile(seq1, 'left chest',timestr)
        writetofile(seq5, 'right chest',timestr)
        writetofile(seq2, 'left thigh',timestr)
        # writetofile(seq2, 'right thigh',timestr)
        for i in range(11):
            writetofile(tasklist[i],sensorname[i],timestr)
    z=z+1
    ############################
    if flag == 0:
        button = tk.Button(window,
                           text='END',
                           command=stop)
        button.grid(row=15, column=15)
        flag = 1


    window.update()



ser.close()
ser1.close()
ser2.close()
ser3.close()
# ser4.close()
ser5.close()
