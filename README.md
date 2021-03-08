
Developer - Arvind Ramachandran

Project title -  Thermodynamic Analyzer 

Contact - aramac13@asu.edu

# TAGUI-3.0

TAGUI-3.0 is the latest graphical user interface program developed to interface with the TAC program and ultimately the the ThermoAnalyzer(TA).It enables the experimenter to visualize and record data from the TA, as well as send commands and receive responses. 

To run download this repository and run the TAGUI.py program and you should be able to see the GUI developed for this project

The TA is controlled by the thermodynamic analyzer controller (TAC), which in our set up is a program running on a Raspberry Pi 3 computer. The software for the TAC can be found at https://github.com/ArvindRamachandran14/TAC-2.0 

## Module Functionality 

#### MainForm.py 
This is the top level of the GUI tree. Contains the Menu bar, serial bar, status bar and the hosts the notebook containing different tabs 

#### CtrtSetup.py 
Module for the set up tab, which allows the user to set sample chamber, conditioning chamber, and humidity conditions

#### CtrlMon.py 
Module for the monitor tab, which allows the user to monitor system variables such as temperature, partial pressures, and sample weight. Also enables the user to record data

#### CtrlTerm.py 
Module for the terminal tab, which allows the user to type commands to be sent to the TA and receive responses

#### TADAQ.py

Responsible for establishing the initial serial connection to the TA, data acquisition from the TA and processing the command queue from the user

#### TAGUI.py

Responsible for the running the TAGUI application loop


The TA is an apparatus that is used to study the thermodynamics of Direct Air Capture sorbents. Direct Air Capture (DAC) is the process of capturing CO2 from the atmosphere, as a way of managing the build up of CO2 in the atmosphere. To learn more about DAC visit https://cnce.engineering.asu.edu/

