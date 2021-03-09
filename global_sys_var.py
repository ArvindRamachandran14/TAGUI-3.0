class globals_:
    def __init__(self):
        self.Temperatures_SC = [0]*25000
        self.Temperatures_CC = [0]*25000
        self.Temperatures_DPG = [0]*25000
        self.Temperatures_DP = [0]*25000
        self.pCO2_list = [0]*25000
        self.pH2O_list = [0]*25000
        self.RH_list = [0]*25000
        self.sample_weight = [0]*25000
        self.time_list = [0]*25000
        self.blogging = False
        self.bsimulation = True
        self.run_experiment = False
        self.log_frequency = 2 #seconds