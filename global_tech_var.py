# globals.pyxw
# Globals as needed
# Change history:
#   20191112:KDT - Original issue

# Global variables

import json

cfgFile = 'taui.json'

baud_rate = 9600
cfg = {}                        # Config object
tty = "/dev/ttyUSB0"                      # TTY or COM port to use for TA comms
bconnected = "False"
bsimulation = "True"
time_out = 5
time_interval = 5

# initialize
# Initialize globals from the cfg object
def initialize(config) :
    global cfg, tty, baud_rate, time_out, time_interval, ser, bconnected, bsimulation
    cfg = config                            # Set the cfg
    tty = cfg["tty"]
    baud_rate = cfg["baud_rate"]
    time_out = cfg["time_out"]
    time_interval = cfg["time_interval"]
    bconnected = cfg["bconnected"]
    bsimulation = cfg["bsimulation"]
    update()

def update():

    #Updates json file with new parameters

    cfg["tty"] = tty

    cfg["baud_rate"] = baud_rate

    cfg["time_out"] = time_out

    cfg["time_interval"] = time_interval

    cfg["bconnected"] = bconnected

    cfg["bsimulation"] = bsimulation

    #print(cfg)

    with open(cfgFile, 'w') as fCfg:

        json.dump(cfg, fCfg)