# Telaire CO2 Sensor

This is the project code used for interfacing the Telaire T6713 low-cost sensor with a laptop for reading atmospheric concentrations of carbon dioxide (CO2). When run from a terminal a live output will be displayed to the terminal window every 10 seconds and will save the measured concentrations to logfile. 

### Setup and Running the Script
The code for this project is written in Python 3.8. Please ensure your environment has the Python packages given in the requirements.txt file. 

As tested, the script is run from a terminal in your project environment 
```bash
   python t6713.py
```
And will output concentrations to the terminal window. 

A few things to note ...
1. Check the location of the sensor input (given in ``read_concentrations()``, variable `serial_dev`) is set. This had only been tested for UNIX machines and will likely differ for windows machines

2. Line 52 is where the concentrations are calculated. This is likely incorrect (see below)

3. You may want to change the concentration output time (10 seconds is quite a long gap), this is on line 88

### About Telaire T6713 
<img src="https://media.digikey.com/Photos/Amphenol%20Photos/T6713-5K.jpg" width="100">

__This is the sensor!__

Information about the Telaire CO2 sensor (including how to wire it up) can be found on the [Amphenol website](https://www.amphenol-sensors.com/en/telaire/co2/525-co2-sensor-modules/3399-t6713), which includes links to the [datasheet](https://f.hubspotusercontent40.net/hubfs/9035299/Documents/AAS-920-634G-Telaire-T6713-Series-011321-web.pdf) and [manual](https://www.amphenol-sensors.com/hubfs/Documents/AAS-916-142A-Telaire-T67xx-CO2-Sensor-022719-web.pdf)

### Important Update! (Feb. 2023)
After a CO2 sensor intercomparison experiment, we found the values reported by the Telaire sensor were incorrect both in magnitude and variability. We most likely expect this is the result of a bug in the python script. I have yet to find time to solve this! Suggestions are welcome (please submit them as a PR). 
