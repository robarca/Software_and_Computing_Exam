#!/usr/bin/python3
#-----------------------------------------------------------------
# Weighting functions and Transmittances 
#-----------------------------------------------------------------
#
# "Weighting_Function_&_Transmittance" is a simple model to compute 
# the weighting functions and transmittances in clear air and 
# in presence of a cloud layer. 
# 
# It is assumed that clouds only absorb and emit (i.e there is no scattering).
#
#
#-----------------------------------------------------------------
#

import matplotlib.pyplot as plt
import numpy as np
import WFT_Functions as fn
from configparser import ConfigParser


# These variables are obtained from the configuration file: "Configuration.ini"

parser = ConfigParser()
parser.read("Configuration.ini")

b = parser.getfloat("General_Variables", "Bottom_cloud",
                         fallback = 5)
t = parser.getfloat("General_Variables", "Top_cloud",
                         fallback = 8)
csg = parser.getfloat("General_Variables", "Cross_section_abs_gas",
                         fallback = 0.1)
coc = parser.getfloat("General_Variables", "Abs_coeff_cloud",
                         fallback = 5)
top = parser.getfloat("General_Variables", "Top_level",
                         fallback = 30)
z1 = parser.getfloat("General_Variables", "z_begin",
                         fallback = 0)
z2 = parser.getfloat("General_Variables", "z_end",
                         fallback = 50)
dz = parser.getfloat("General_Variables", "z_step",
                         fallback = 0.005)
h = parser.getfloat("General_Variables", "vertical_height_scale",
                         fallback = 7)

z = fn.z_vector(z1, dz, z2)

rho_n= fn.normalized_density_profile(z,h)

lod, loc = fn.optical_depth(z,dz,b,t,csg,coc,rho_n)

#FIG.1

clear_t, cloudy_t = fn.TOA_transmittances(lod, loc, z)

#Find the position in z vector of "top" value

z=list(z)

zt=z.index(top)

#Definition of the x and y axes for the plot

x_clear=np.zeros(zt+1)
x_cloudy=np.zeros(zt+1)
y_trans=np.zeros(zt+1)

#Extract values from vectors of transimittances until the zt-th value

for i in range(zt+1):
    x_clear[i]=clear_t[i]
    x_cloudy[i]=cloudy_t[i]
    y_trans[i]=z[i]
    
figure_name_1 = 'Transmittances for clear sky and cloudy sky'
fig_1 = plt.figure()
plt.plot(x_clear, y_trans, 'b--', label ='clear sky', linewidth = 2)
plt.plot(x_cloudy, y_trans, 'r-', label ='cloudy sky', linewidth = 2)
fig_1.suptitle(figure_name_1)
plt.ylabel('Height [km]')
plt.xlabel('Transmittance')
# Definition of legend which is on the plot 
leg = plt.legend()
# Saving figure in the same folder of code

fig_1.savefig('OUTPUT/Transmittances in clear and cloud sky.png') 
#

#FIG. 2

weight_clear, weight_cloudy = fn.weighting_function(clear_t, cloudy_t, z, dz)

#Definition of the x and y axes for the plot

x_clear=np.zeros(zt+1)
x_cloudy=np.zeros(zt+1)
y_weight=np.zeros(zt+1)

#Extract values from weighting function vectors from the second until the zt-th value

for i in range(1,zt+1):
    x_clear[i]=weight_clear[i]
    x_cloudy[i]=weight_cloudy[i]
    y_weight[i]=z[i]
    
figure_name_2 = 'Log weighting functions for clear and cloudy sky'
fig_2 = plt.figure()
plt.semilogx(x_clear, y_weight, 'g--', label = 'clear sky', linewidth = 2)   
plt.semilogx(x_cloudy, y_weight, 'b-', label = 'cloudy sky', linewidth = 2)
fig_2.suptitle(figure_name_2)
plt.ylabel('Height [km]')
plt.xlabel('Log weighting function')
# Definition of legend which is on the plot 
leg = plt.legend()
# Saving figure in the same folder of code

fig_2.savefig('OUTPUT/Log weighting functions for clear and cloudy sky.png')

#FIG.3

figure_name_3 = 'Weighting functions for clear and cloudy sky'
fig_3 = plt.figure()
plt.plot(x_clear, y_weight, 'k--', label = 'clear sky', linewidth = 2)   
plt.plot(x_cloudy, y_weight, 'y-', label = 'cloudy sky', linewidth = 2)
fig_3.suptitle(figure_name_3)
plt.ylabel('Height [km]')
plt.xlabel('Weighting function')
# Definition of legend which is on the plot 
leg = plt.legend()
# Saving figure in the same folder of code

fig_3.savefig('OUTPUT/Weighting functions for clear and cloudy sky.png')
