
Developer - Arvind Ramachandran

Project title -  Thermodynamic Analyzer 

Contact - aramac13@asu.edu

# TAGUI-3.0

ThermoAnalyzer Graphical User Interface (TAGUI) is a Python-based graphical user interface program developed to interface with the TAC program and ultimately the ThermoAnalyzer(TA). It enables the experimenter to visualize and record data from the TA, as well as send commands and receive responses. 

To run the GUI, download this repository and run the TAGUI.py program using Python 3 and you should be able to view the GUI developed for this project

The TA is controlled by the thermodynamic analyzer controller (TAC), which in our set up is a program running on a Raspberry Pi 3 computer. The software for the TAC can be found at https://github.com/ArvindRamachandran14/TAC-2.0 

## Module Functionality 

1. `tagui.py` Responsible for the running the TAGUI application loop

2. `mainform.py` This is the top level of the GUI tree. Contains the Menu bar, serial bar, status bar and the hosts the notebook containing different tabs 

3. `ctrt_setup.py` Module for the set up tab, which enables the user to set sample chamber, conditioning chamber, and humidity conditions

4. `ctrl_mon.py` Module for the monitor tab, which enables the user to monitor system variables such as temperature, partial pressures, and sample weight. Also enables the user to record data

5. `ctrl_term.py` Module for the terminal tab, which enables the user to type commands to be sent to the TA and receive responses

6. `calib.py` Module for the calibration tab, which enables the user to calibrate the temperature controllers and the humidity control algorthim

7. `tadaq.py` Responsible for establishing the initial serial connection to the TA, data acquisition from the TA and processing the command queue from the user

8. `data_coord.py` Consumes the data produced by the tadaq and updates the local data structures with the latest values from the TA. Dispatches commands from the user to the TA and gets the reply back from the TA

9. `global_sys_var.py` Module containing global system variables

10. `global_cal_var.py` Module containing global calibration variables

11. `global_tech_var.py` Module containing global technical variables

12. `taui.json` Contains parameters pertaining to serial connection

The TA is an apparatus that is used to study the thermodynamics of Direct Air Capture sorbents. Direct Air Capture (DAC) is the process of capturing CO2 from the atmosphere, as a way of managing the build up of CO2 in the atmosphere. To learn more about DAC visit https://cnce.engineering.asu.edu/

