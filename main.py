import os
import random
from datetime import *
from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter import ttk
import time
import serial
import serial.tools.list_ports

global code
global arduino
global stand_time
global temp_stand_time
global grace_time
global count
global buffer_list
buffer_list = [0,0,0,0,0,0,0,0,0,0]
arduino = serial.Serial()
arduino.baudrate = 9600
arduino.port = "COM11"
arduino.open()
arduino.write("Deactivate\n".strip().encode())
if os.path.exists("timeStanding.txt"):
    pass
else:
    file = open("timeStanding.txt", "x")


def create_buffer():
    while True:
        buffer_list[0] = buffer_list[1]
        buffer_list[1] = buffer_list[2]
        buffer_list[2] = buffer_list[3]
        buffer_list[3] = buffer_list[4]
        buffer_list[4] = buffer_list[5]
        buffer_list[5] = buffer_list[6]
        buffer_list[6] = buffer_list[7]
        buffer_list[7] = buffer_list[8]
        buffer_list[8] = buffer_list[9]
        buffer_list[9] = int(arduino.readline().decode('utf8').strip())


buffer_thread = Thread(target=create_buffer, args=()).start()


def check_buffer():
    counter = 0
    for buffer in buffer_list:
        if buffer < standing_point:
            counter += 1
    if counter >= 6:
        return True
    return False


def write_file_prep():
    if not check_buffer():
        start_time = get_current_time()
        counter = 1
        while not check_buffer() and counter % 600 != 0:
            time.sleep(1)
            counter += 1
        time.sleep(1)
        end_time = get_current_time()
        time_spend = (end_time - start_time) / 60
        print(time_spend)
        hours = int(time_spend / 60)
        min = int(time_spend % 60)
        input = str(datetime.now().strftime("%Y-%m-%d %H:%M:")) + " - " + str(hours) + "h " + str(min) + "m"
        write_file(input)
        return True
    return False


def write_file(input):
    print("test")
    file = open("timeStanding.txt", "a")
    file.write(input)
    file.close()



def disable_event():
    pass


def get_current_time():
    return int(datetime.now().strftime("%H")) * 360 + int(datetime.now().strftime("%M")) * 60 + int(datetime.now().strftime("%S"))



def genereate_random_code():
    code = ""
    i = 1
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def comlist():
    list = serial.tools.list_ports.comports()
    pretty_list = ""
    for port in list:
        pretty_list += str(port) + "\n"
    return pretty_list


def start():
    global standing_point
    global sitting_distance, standing_distance, grace_time, stand_time
    def close_by_code():
        if var.get() != "" and var2.get() != "" and var3.get() != "" and var4.get() != "":
            start_window.destroy()

    def is_type_int(*args):
        item = var.get()
        try:
            item_type = type(int(item))
        except:
            sitting_height.delete(0, tk.END)

    def is_type_int2(*args):
        item = var2.get()
        try:
            item_type = type(int(item))
        except:
            standing_height.delete(0, tk.END)

    def is_type_int3(*args):
        item = var3.get()
        try:
            item_type = type(int(item))
        except:
            grace_period.delete(0, tk.END)

    def is_type_int4(*args):
        item = var4.get()
        try:
            item_type = type(int(item))
        except:
            standing_time.delete(0, tk.END)

    start_window = Tk()
    start_window.title("Standing Desk Thingy")
    start_window.geometry("800x500")
    start_window.configure(bg="gray")

    var = tk.StringVar()
    var.trace("w", is_type_int)
    var2 = tk.StringVar()
    var2.trace("w", is_type_int2)
    var3 = tk.StringVar()
    var3.trace("w", is_type_int3)
    var4 = tk.StringVar()
    var4.trace("w", is_type_int4)

    sitting_height = Entry(start_window, textvariable=var)
    sitting_height.pack()
    sitting_height.place(x=100, y=100)

    standing_height = Entry(start_window, textvariable=var2)
    standing_height.pack()
    standing_height.place(x=100, y=150)

    grace_period = Entry(start_window, textvariable=var3)
    grace_period.pack()
    grace_period.place(x=100, y=200)

    standing_time = Entry(start_window, textvariable=var4)
    standing_time.pack()
    standing_time.place(x=100, y=250)

    sitting = Label(start_window, text="Enter sitting height in cm!", background='gray', foreground="black")
    sitting.pack()
    sitting.place(x=100, y=80)

    standing = Label(start_window, text="Enter standing height in cm!", background='gray', foreground="black")
    standing.pack()
    standing.place(x=100, y=130)

    grace = Label(start_window, text="Enter time till yo want to stand up!", background='gray', foreground="black")
    grace.pack()
    grace.place(x=100, y=180)

    time = Label(start_window, text="Enter time you want to stand!", background='gray', foreground="black")
    time.pack()
    time.place(x=100, y=230)

    serial_ports = Label(start_window, text=comlist(), background='gray', foreground="black")
    serial_ports.configure(anchor="w")
    serial_ports.pack()
    serial_ports.place(x=100, y=280)

    button = Button(start_window, text="Finish setup", command=close_by_code, background='gray', foreground='black')
    button.pack()
    button.place(x=300, y=100)

    start_window.mainloop()

    sitting_distance = int(var.get())
    standing_distance = int(var2.get())
    grace_time = int(var3.get())
    stand_time = int(var4.get())
    standing_point = (standing_distance - sitting_distance)/2 + sitting_distance


start()


def block_screen():
    global count
    global stand_time, temp_stand_time
    def close_by_code():
        global temp_stand_time
        if textField.get(1.0, "end-1c") == code:
            window.destroy()
            temp_stand_time = 0

    window = Tk()
    window.title("Python GUI App")
    width = 10000
    height = 4000
    window.geometry("%dx%d+-%d+-%d" % (width, height, 1930, 220))
    window.configure(bg='black')
    # window.protocol("WM_DELETE_WINDOW", disable_event)
    window.resizable(False, False)
    label = Label(window, text="Enter Passcode (Found on measurement device)", background="black", foreground="green")
    label.pack()
    label.place(x=width / 5, y=300)
    textField = Text(window, height=1, width=20, background='black', foreground="red")
    textField.pack()
    textField.place(x=width / 5, y=350)
    button = Button(window, text="Click to Close", command=close_by_code, background='black', foreground='green')
    button.pack()
    button.place(x=width / 5, y=400)

    count = 0

    def loop():
        arduino.write(code.encode())
        global count
        global temp_stand_time
        distance = buffer_list[0]
        if distance > standing_point:
            count += 1
            window.after(100, loop)
        else:
            count = 0
            window.after(100, loop)
        if count >= 10:
            temp_stand_time = stand_time
            window.destroy()

    arduino.write(code.encode())
    window.after(100, loop)
    window.mainloop()


def check_if_still_standing(time):
    startTimeStanding = get_current_time()
    timeElapsed = 1
    while timeElapsed < time:
        currentTime = get_current_time()
        timeElapsed = currentTime - startTimeStanding
        if timeElapsed % 10 == 0:
            if check_buffer():
                block_screen()
                if temp_stand_time == 0:
                    return
                startTimeStanding = get_current_time() - timeElapsed


startTime = get_current_time()
timeElapsed = 0
while True:
    while timeElapsed < grace_time:
        write_file_prep()
        currentTime = get_current_time()
        timeElapsed = currentTime - startTime
        print(timeElapsed, end="\r")
    if check_buffer():
        arduino.write("Activate\n".strip().encode())
        code = genereate_random_code()
        time.sleep(.5)
        arduino.write(code.encode())
        block_screen()
        check_if_still_standing(temp_stand_time)
        arduino.write("Deactivate\n".strip().encode())
        print("you did it")
        hours = int(temp_stand_time / 360)
        min = int(int(temp_stand_time / 60) % 60)
        input = str(datetime.now().strftime("%Y-%m-%d %H:%M:")) + " - " + str(hours) + "h " + str(min) + "m\n"
        write_file(input)
    timeElapsed = 0
    startTime = get_current_time()