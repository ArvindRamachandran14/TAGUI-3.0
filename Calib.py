from tkinter import Frame, LabelFrame, Label, Spinbox, Button, Text, StringVar, Radiobutton


class Calib(Frame) :
    def __init__(self, parent, cons, *args, **kwargs) :
        Frame.__init__(self, *args, **kwargs)
        self.cons = cons
        self.parent = parent
        self.buildContent()

    def buildContent(self) :
        self.output = StringVar()
        self.grpSetpoint = LabelFrame(self, text = 'Controller Power ON/OFF')
        self.grpSetpoint.grid(row=0,column=0, padx=10, pady=10)
        self.label1 = Label(self.grpSetpoint, text = 'Sample Chamber Controller power:')
        self.label1.grid(row = 0, column = 0, padx = 2, pady = 2, sticky='e')

        MODES = [("ON", "1"),("OFF", "0")]

        self.v1 = StringVar()
        self.v1.set("0") # initialize

        for i in range(2):
            self.rb1 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v1, value=MODES[i][1])
            self.rb1.grid(row=0, column=i+1, padx = 2, pady = 2, sticky='w')
       
        #self.sb1.bind("<Return>", self.send_command)
        self.label2 = Label(self.grpSetpoint, text = 'Conditioning Chamber Controller power:')
        self.label2.grid(row = 1, column = 0, padx = 2, pady = 2, sticky='e')

        self.v2 = StringVar()
        self.v2.set("0") # initialize

        for i in range(2):
            self.rb2 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v2, value=MODES[i][1])
            self.rb2.grid(row=1, column=i+1, padx = 2, pady = 2, sticky='w')
       
        self.label3 = Label(self.grpSetpoint, text = 'Dew Point Generator Controller power:')
        self.label3.grid(row = 2, column = 0, padx = 2, pady = 2, sticky='e')

        self.v3 = StringVar()
        self.v3.set("0") # initialize

        for i in range(2):
            self.rb3 = Radiobutton(self.grpSetpoint, text=MODES[i][0], variable=self.v3, value=MODES[i][1])
            self.rb3.grid(row=2, column=i+1, padx = 2, pady = 2, sticky='w')
        
        self.box_values = Button(self.grpSetpoint, text="Send box values", command=self.send_command)
        self.box_values.grid(row = 5, column = 1, columnspan=2, padx = 2, pady = 2, sticky='w')

    def send_command(self): 

        reply1 = self.cons.send_command_to_PC('s SC_power '+  int(self.v1.get()))

        reply2 = self.cons.send_command_to_PC('s CC_power '+ int(self.v2.get()))

        reply3 = self.cons.send_command_to_PC('s DPG_power '+  int(self.v1.get()))

        print(reply1, reply2, reply3)

