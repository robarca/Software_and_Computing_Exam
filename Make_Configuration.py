#!/usr/bin/python3
#--------------------------------------------------------------
#Python file for the generation of the configuration.ini file
#--------------------------------------------------------------
#--------------------------------------------------------------

from configparser import ConfigParser

config = ConfigParser()

config["General_Variables"] = {   
    "Bottom_cloud" : "5",
    "Top_cloud" : "8",
    "Cross_section_abs_gas" : "0.1",
    "Abs_coeff_cloud" : "5",
    "Top_level" : "30",
    "z_begin" : "0",
    "z_end" : "50",
    "z_step" : "0.005",
    "vertical_height_scale" : "7"
    }


config["Output_Path"] = {
    "output_graph" : "./OUTPUT/"}

with open("./Configuration.ini","w") as file:
    config.write(file)
