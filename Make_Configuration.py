#!/usr/bin/python3
#--------------------------------------------------------------
#Python file for the generation of the configuration.ini file
#--------------------------------------------------------------
#--------------------------------------------------------------

from configparser import ConfigParser

config = ConfigParser()

config["General_Variables"] = {   
    "Bottom_cloud" : "5",
    "Top_cloud" : "10",
    "Cross_section_abs_gas" : "0.02",
    "Abs_coeff_cloud" : "5",
    "Top_level" : "25",
    "vertical_height_scale" : "7"
    }


config["Output_Path"] = {
    "output_graph" : "./OUTPUT/"}

with open("./Configuration.ini","w") as file:
    config.write(file)
