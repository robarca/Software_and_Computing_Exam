#!/usr/bin/python3
#--------------------------------------------------------------
#Python file for the generation of the configuration.ini file
#--------------------------------------------------------------
#--------------------------------------------------------------

from configparser import ConfigParser

config = ConfigParser()

config["General_Variables"] = {   
    "Bottom_cloud" : "10",
    "Top_cloud" : "15",
    "Cross_section_abs_gas" : "0.03",
    "Abs_coeff_cloud" : "2",
    "Top_level" : "20",
    "vertical_height_scale" : "7"
    }


config["Output_Path"] = {
    "output_graph" : "./OUTPUT/"}

with open("./Configuration.ini","w") as file:
    config.write(file)
