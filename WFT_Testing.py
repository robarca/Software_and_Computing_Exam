#!/usr/bin/python3
#----------------------------------------
# Testing functions used in WFT_Profile.py
#----------------------------------------

import numpy as np
import WFT_Functions as fn
import pytest
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given

z1=0
dz=0.005
z2=50

z = fn.z_vector(z1,dz,z2,20)

def test_z_vector_input():

    """ This function tests if an Error Message is released with the wrong inputs

        i.e if the base of the atmpsphere or the top are negative or if dz is not a reasonable number
    """
         
    with pytest.raises(ValueError):
       fn.z_vector(-1,0.5,5,20)
       
    #check if a ValueError arises if z2 is smaller then z1
    
    with pytest.raises(ValueError):
       fn.z_vector(10,0.5,5,20)
       
    #check if a ValueError arises if dz in negative
    
    with pytest.raises(ValueError):
       fn.z_vector(1,-0.5,5,20)
    
    #check if a ValueError arises if dz is not in the right range
    
    with pytest.raises(ValueError):
       fn.z_vector(1,10,5,20)

def test_z_right(z,dz):

    """ This function tests if the vector z was created properly.
	    
        Considering that z1=0 and z2=50, this test wants to make sure that the length of the vector z is equal to z2/dz
    """
    assert(len(z) == z2/dz)
    
def test_z_monotonical(z,dz):
	
    """ This function tests if the values ​​in vector z are monotonically increasing.
	
	In this regard, it is good to remember that z is the vector of heights that progressively go from 0 to 50 with step dz.
    """
        
    for k in range(0, len(z)-2):
        assert(z[k] < z[k+1])
        assert(z[k+1] - z[k] == dz)
             
h=7
rho_n = fn.normalized_density_profile(z,h)
        
def test_normalized_density_profile_input(z,h):
    """ This function tests if an Error Message is released with the wrong inputs

        i.e if the scale height (h) is negative or is 0 
    """
            
    #check if a ValueError arises if h is negative
     
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,-1) 
        	 	   
    #check if a ValueError arises if h is 0
    
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,0)
       
def test_rho_n_length(rho_n,z):

    """ This function tests if the vector rho_n was created properly.
	    
        Considering that normalized density vector is created as an exponential function of z, these two
        vectors must have the same length
    """
    
    assert(len(rho_n) == len(z))

def test_density_monotonicity(rho_n):

    """ This function tests if the values ​​in vector rho_n are monotonically decreasing.
	
	Being the density profile computed from exp(-z/h) it's reasonable to expect that the minimum value of this profile
	is at the top of th atmpsphere (50 km), while the maximum value is at the bottom (0 km)
    """

    #check decreasing monotonicity of rho_n profile
 
    for k in range(0, len(rho_n)-2):
    	assert(rho_n[k] >= rho_n[k+1])
    
    #check if min value of the denisty profile is at the last one of the vector
    
    assert(min(rho_n)==rho_n[len(rho_n)-1])
    
    #check if max value of the denisty profile is the first one of the vector
    
    assert(max(rho_n)==rho_n[0])

b=10
t=15
csg=0.2
coc=2    
lod,loc=fn.optical_depth(z,dz,b,t,csg,coc,rho_n)

def test_optical_depth_input(z,b,t):

    """ This function tests the values used as input to compute the optical depth.
	
	It is precisely checked that the cloud is in a plausible position, therefore within the considered atmospheric layer, 
	and that the absorption cross sections have non-negative values
    """
          
    #check if b (cloud's base) and t (cloud's top) are positive 
      
    assert(b > 0)
    assert(t > 0)
    
    #check if b is bigger than z1 and t is smaller then z2
   
    assert(b >= z1)
    assert(z2 >= t)
        
    #check is t is bigger then b
      
    assert(t > b)
    
    #check if coc and csg are positive
    
    assert(coc > 0)
    assert(csg > 0)
      
    #check if a ValueError arises if b or t are negative 
    
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,-1,15,2,0.2,rho_n) 
       
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,10,-1,2,0.2,rho_n)  

def molecular_and_total_OD_length(loc,lod):

    """ This function tests if the molecular optical depth vector (lod) and total optical depth vector (loc) are created properly.
	
	lod and loc they differ in that, in the first, only clear skies are considered; while in the second the contribution given
	by the cloud is taken into account. In any case, the lengths of the two vectors must necessarily be the same.
    """
    
    assert(len(loc) == len(lod))

def molecular_and_total_OD_top(loc,lod):
    
    """ Considering the fact that the OD vecors are created using the exponential denisty profile,
        it's reasonable to find the min value at the top of the atmpsphere, which means as last value of loc and lod vectors.
        Also, as for the previous case, we must find the max value at the bottom of the surface, so as first value of lod and loc.
    """
    
    #checks for the min values
    
    assert(min(loc)==loc[len(loc)-1])
    assert(min(lod)==lod[len(lod)-1])
    
    #check for the max values
    
    assert(max(loc)==loc[0])
    assert(max(lod)==lod[0])

clear_t, cloudy_t = fn.TOA_transmittances(lod, loc, z)

def test_transimattances_len(clear_t,cloudy_t):
    
    """ This test checks if the transimittance vectors have the same length.
    	
    	They change because one of them is computed using molecular OD profile, the other one needs the total OD profile.
    """
    
    assert(len(cloudy_t) == len(clear_t))
    
def test_transmittances_range(clear_t,cloudy_t):

    """ This test checks if the values in transmittance vectors are reasonable.
    	
    	Transimittance can have values from 0 to 1: this means that this test controls if the values
    	inside the clear_t and cloudy_t vectors are contained into the range [0;1]
    """
    
    #check fot the clear sky case
    
    for k in range(0, len(clear_t)-1):
        assert(clear_t[k] >= 0 or clear_t[k] <= 1)
        
    #check for the cloudy sky case
    
    for k in range(0, len(cloudy_t)-1):
        assert(cloudy_t[k] >= 0 or cloudy_t[k] <= 1)
        
def test_transmittance_TOA(clear_t,cloudy_t):

    """ The trasmittance has to assume the value of 1 at the top of the atmosphere.
    
        On the other hand, for the surface there are no particular specific values ​​that the function 
        must assume since, the latter, depend on the transmittance profile that is created.
    """
    
    #check if the transmittance value at TOA are 0 for both cloudy and clear sky cases
    
    assert(clear_t[len(clear_r)-1] == 1)
    assert(cloudy_t[len(cloudy_t)-1] == 1)

weight_clear, weight_cloudy = fn.weighting_function(clear_t, cloudy_t, z, dz)

def test_weighting_functions(clear_t,cloudy_t,weight_clear,weight_cloudy):

    """ It is useful to remember that the weighting function is nothing more than the derivative of the transmittance.
    
        Despite this, there are no maximum or minimum values ​​that x must assume; however, what must still occur is that 
        the vectors of weighting functions and those of transmittances must have the same length.
    """
    
    assert(len(clear_t)==len(weight_clear))
    assert(len(cloudy_t)==len(weight_clear))

