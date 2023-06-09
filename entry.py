#!python3
# *********************************************************
# Author: Tiancheng Xiong
# Date: June 6, 2023
# Purpose: entry of the whole program
# Notice: None
# *********************************************************

# ---------------------------------------------------------
import pyvisa as visa
import customtkinter
import setParameter as sp
import measure as ms
import waveform_plot as wp
from tkinter import Scale


# =========================================================
# Main program:
# =========================================================
rm = visa.ResourceManager()
scope = rm.open_resource("USB0::0x0957::0x9009::MY53120106::0::INSTR")
scope.timeout = 20000

sp.initialize(scope)
ms.initialize(scope)
wp.initialize(scope)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Oscilloscope Automation")
        self.geometry("1000x1000")
        self.grid_columnconfigure(0, weight=1)

        self.button = customtkinter.CTkButton(
            self, text="Auto Scale", command=self.auto_scale_callback)
        self.button.grid(row=0, column=0, padx=20, pady=20,
                         sticky="ew", columnspan=4)


        self.check_var = customtkinter.StringVar(value="off")
        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Average", command=self.checkbox_average, onvalue="on", offvalue="off", variable=self.check_var)
        self.checkbox_1.grid(row=1, column=0, padx=20,
                             pady=(0, 20), sticky="w")
        # self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=1, padx=20,
        #                      pady=(0, 20), sticky="w")




        self.label = customtkinter.CTkLabel(
            self, text="Choose a channel", fg_color="transparent", width=1)
        self.label.grid(row=2, column=0, padx=0, columnspan=1, sticky="ew")
        self.source = "CHANnel1"
        self.channel_val = customtkinter.StringVar(value="CHOOSE !")
        self.optionmenu_channel = customtkinter.CTkOptionMenu(self, values=["channel 1", "channel 2", "channel 3", "channel 4"],
                                                              command=self.optionmenu_channel_callback, variable=self.channel_val)
        self.optionmenu_channel.grid(row=2, column=1, padx=10, pady=10,
                                     sticky="ew", columnspan=3)
        # impedance selection

        self.label = customtkinter.CTkLabel(
            self, text="Choose a value of impedance:", fg_color="transparent", width=1)
        self.label.grid(row=3, column=0, padx=0, columnspan=1, sticky="ew")
        self.imp_val = customtkinter.StringVar(value="CHOOSE !")
        self.optionmenu_impedance = customtkinter.CTkOptionMenu(self, values=["DC coupling, 1 MΩ impedance", "DC coupling, 50Ω impedance", "AC coupling, 1 MΩ impedance", "AC 1 MΩ input impedance"],
                                                                command=self.impedance_callback, variable=self.imp_val)
        self.optionmenu_impedance.grid(row=3, column=1, padx=10, pady=10,
                                       sticky="ew", columnspan=3)

        # slope selection
        self.label = customtkinter.CTkLabel(
            self, text="Choose a value of slope:", fg_color="transparent", width=1)
        self.label.grid(row=4, column=0, padx=0, columnspan=1, sticky="ew")
        self.slope_val = customtkinter.StringVar(value="CHOOSE !")
        self.optionmenu_slope = customtkinter.CTkOptionMenu(self, values=["rise", "fall", "Either"],
                                                            command=self.slope_callback, variable=self.slope_val)
        self.optionmenu_slope.grid(row=4, column=1, padx=10, pady=10,
                                   sticky="ew", columnspan=3)

        # set the number of points
        self.points_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter the number of acquired points", width=20)
        self.points_entry.grid(row=5, column=0, padx=5, pady=20, sticky="ew")

        self.points_entry.bind('<Return>', lambda event: self.button1_callback())
        self.button1 = customtkinter.CTkButton(
            self, width=5, text="Submitted acquired points", command=self.button1_callback)
        self.button1.grid(row=5, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=1)

        self.button2 = customtkinter.CTkButton(
            self, width=10, text="Automatic", command=self.button2_callback)
        self.button2.grid(row=5, column=2,  padx=20, pady=20,
                          sticky="ew", columnspan=2)

        # set the sampling rate
        self.sampling_entry = customtkinter.CTkEntry(
            self, placeholder_text="Enter the sampling rate", width=20)
        self.sampling_entry.grid(row=6, column=0, padx=5, pady=20, sticky="ew")

        self.sampling_entry.bind('<Return>', lambda event: self.button3_callback())

        self.button3 = customtkinter.CTkButton(
            self, width=5, text="Submitted sampling rate", command=self.button3_callback)
        self.button3.grid(row=6, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=1)

        self.button4 = customtkinter.CTkButton(
            self, width=10, text="Automatic", command=self.button4_callback)
        self.button4.grid(row=6, column=2,  padx=20, pady=20,
                          sticky="ew", columnspan=2)

        # download the measurement
        self.measurement_path = customtkinter.CTkEntry(
            self, placeholder_text="Enter the path you want to download", width=20)
        self.measurement_path.grid(
            row=7, column=0, padx=5, pady=20, sticky="ew")

        self.measurement_path.bind('<Return>', lambda event: self.button5_callback())

        self.button5 = customtkinter.CTkButton(
            self, width=5, text="Download the data measurement", command=self.button5_callback)
        self.button5.grid(row=7, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=1)

        # download or show the waveform
        self.waveform_data_path = customtkinter.CTkEntry(
            self, placeholder_text="Enter the path of csv file you want to download", width=20)
        self.waveform_data_path.grid(
            row=8, column=0, padx=5, pady=20, sticky="ew")

        self.waveform_data_path.bind('<Return>', lambda event: self.button6_callback())

        self.waveform_plot_path = customtkinter.CTkEntry(
            self, placeholder_text="Enter the path of waveform you want to download", width=20)
        self.waveform_plot_path.grid(
            row=8, column=1, padx=5, pady=20, sticky="ew")

        self.waveform_plot_path.bind('<Return>', lambda event: self.button6_callback())

        self.button6 = customtkinter.CTkButton(
            self, width=5, text="Download the waveform", command=self.button6_callback)
        self.button6.grid(row=8, column=2, padx=10, pady=20,
                          sticky="ew", columnspan=1)

        self.button7 = customtkinter.CTkButton(
            self, width=5, text="Show the waveform", command=self.button7_callback)
        self.button7.grid(row=8, column=3, padx=10, pady=20,
                          sticky="ew", columnspan=1)

        # download the screenshot
        self.screenshot_path = customtkinter.CTkEntry(
            self, placeholder_text="Enter the path you want to download", width=20)
        self.screenshot_path.grid(
            row=9, column=0, padx=5, pady=20, sticky="ew")

        self.screenshot_path.bind('<Return>', lambda event: self.button8_callback())

        self.button8 = customtkinter.CTkButton(
            self, width=5, text="Download the screenshot", command=self.button8_callback)
        self.button8.grid(row=9, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=1)


        # scaling and offset
    
        self.label = customtkinter.CTkLabel(
            self, text="Vertical Scaling (unit: mV | from 100 to 1300)", fg_color="transparent", width=1)
        self.label.grid(row=10, column=0, padx=0, columnspan=1, sticky="ew")
        self.slider1 = Scale(self, from_=100, to=1300, orient='horizontal', command=self.general_vertical_scaling)
        self.slider1.grid(row=10, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=3)
        self.slider1.set(200)

        self.label = customtkinter.CTkLabel(
            self, text="Vertical Offset (unit: mV | from 0 to 1000 )", fg_color="transparent", width=1)
        self.label.grid(row=11, column=0, padx=0, columnspan=1, sticky="ew")
        self.slider2 = Scale(self, from_=0, to=1000, orient='horizontal', command=self.general_vertical_offset)
        self.slider2.grid(row=11, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=3)
        self.slider2.set(540)
        
        self.label = customtkinter.CTkLabel(
            self, text="Horizontal Scaling (unit: Microsecond | from 100 to 1500)", fg_color="transparent", width=1)
        self.label.grid(row=12, column=0, padx=0, columnspan=1, sticky="ew")
        self.slider3 = Scale(self, from_=100, to=1300, orient='horizontal', command=self.general_horizontal_scaling)
        self.slider3.grid(row=12, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=3)

        self.slider3.set(500)

        self.label = customtkinter.CTkLabel(
            self, text="Horizontal Offset (unit: Microsecond | from -100 to 100)", fg_color="transparent", width=1)
        self.label.grid(row=13, column=0, padx=0, columnspan=1, sticky="ew")
        self.slider4 = Scale(self, from_=-1000, to=1000, orient='horizontal', command=self.general_horizontal_offset)
        self.slider4.grid(row=13, column=1, padx=10, pady=20,
                          sticky="ew", columnspan=3)
        
        self.slider4.set(0)



        self.selected_slider = self.slider1
        # self.slider1.bind('<Key>', self.handle_keypress)
        # self.slider2.bind('<Key>', self.handle_keypress)
        # self.slider3.bind('<Key>', self.handle_keypress)
        # self.slider4.bind('<Key>', self.handle_keypress)
        self.bind('<Key>', self.handle_keypress)



        # self.slider1.bind('<Key>',lambda event: self.vertical_scaling_increasing())

    def auto_scale_callback(self):
        print("button pressed")
        sp.autoScle()


    def checkbox_average(self):
        val = self.check_var.get()
        sp.average_on_off(val)
        print(val)

    def optionmenu_channel_callback(self, choice):
        if choice == "channel 1":
            self.source = "CHANnel1"
        elif choice == "channel 2":
            self.source = "CHANnel2"
        elif choice == "channel 3":
            self.source = "CHANnel3"
        else:
            self.source = "CHANnel4"

        sp.channel_control_select(choice)
        print("channel:", choice)

    def impedance_callback(self, choice):
        sp.impedance_control_select(choice)
        print("impedance:", choice)

    def slope_callback(self, choice):
        sp.trigger_slope_select(choice)
        print("slope:", choice)

    # set the memory depth
    def button1_callback(self):
        num = self.points_entry.get()
        print(self.points_entry.get())
        sp.points_acquire(num)
        
    # automatically set the memory depth
    def button2_callback(self):
        sp.points_auto_clicked()
        # do automatic setting

    # set the sampling rate
    def button3_callback(self):
        num = self.sampling_entry.get()
        print(self.sampling_entry.get())
        sp.sample_rate(num)

    # automatically set the sampling rate
    def button4_callback(self):
        sp.sample_auto_clicked()
        # do automatic setting


    # download the measurement
    def button5_callback(self):
        print(self.source)
        path = self.measurement_path.get() + ".csv"
        print(path)
        ms.measure(self.source, path, debug=False)
        

    # download the waveform
    def button6_callback(self):
        data_path = self.waveform_data_path.get() + ".csv"
        plot_path = self.waveform_plot_path.get() + ".png"
        print(self.source)
        wp.read_and_plot(download=True, source=self.source, csv_path=data_path, waveform_path=plot_path)
        

    # show the waveform
    def button7_callback(self):
        print("debug:")
        print(self.source)
        wp.read_and_plot(source=self.source)

    # download the screenshot
    def button8_callback(self):
        path = self.screenshot_path.get()
        print(self.screenshot_path.get())
        wp.download_screen_image(path)

    # set the step
    def handle_keypress(self, event):
        if event.keysym == 'Left':
            self.selected_slider.set(self.selected_slider.get() - 10)
        elif event.keysym == 'Right':
            self.selected_slider.set(self.selected_slider.get() + 10)
        elif event.keysym == 'Down':
            if self.selected_slider == self.slider1:
                self.selected_slider = self.slider2
            elif self.selected_slider == self.slider2:
                self.selected_slider = self.slider3
            elif self.selected_slider == self.slider3:
                self.selected_slider = self.slider4

        elif event.keysym == 'Up':
            if self.selected_slider == self.slider2:
                
                self.selected_slider = self.slider1
            elif self.selected_slider == self.slider3:
                self.selected_slider = self.slider2
            elif self.selected_slider == self.slider4:
                self.selected_slider = self.slider3
        
        for slider in [self.slider1, self.slider2, self.slider3, self.slider4]:
            if slider == self.selected_slider:
                slider.config(troughcolor='green')
            else:
                slider.config(troughcolor='grey')   


        if self.selected_slider == self.slider1:
            self.vertical_scaling()   


    def general_vertical_scaling(self, value):
        # value = self.slider1.get()
        print(value)
        sp.vertical_scaling(value)

    def general_vertical_offset(self, value):
        print(value)
        sp.vertical_offset(value)

    def general_horizontal_scaling(self, value):
        print(value)
        sp.horizontal_scaling(value)

    def general_horizontal_offset(self, value):
        print(value)
        sp.horizontal_offset(value)

    


    
    
 

        


app = App()
# app.mainloop()
app.mainloop()


# scope.close()
# print("End of program.")
# sys.exit()
