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

# Test for the function "z_vector"

@given(st.integers(0,49),st.floats(0.005,1),st.integers(1,50))
@settings(max_examples = 10)

def test_z_vector(z1,dz,z2):
    
    z = fn.z_vector(z1,dz,z2)
        
    with pytest.raises(ValueError):
       fn.z_vector(-1,0.01,5)
       
    #check if a ValueError arises if z2 is smaller then z1
    
    with pytest.raises(ValueError):
       fn.z_vector(10,0.05,5)
       
    #check if the z output vector exists
    
    assert(len(z) >= 1)
    
# Test for the function "normalized_density_profile"  
        
@given(st.integers(0,49),st.floats(0.005,1),st.integers(50,100),st.floats(1,10))
@settings(max_examples = 10)

def test_normalized_density_profile(z1,dz,z2,h):
    
    z = fn.z_vector(z1,dz,z2)
    
    rho_n = fn.normalized_density_profile(z,h)
       
    #check if a ValueError arises if h is negative
     
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,-1) #check z al posto di np.appary come dopo
       
    #check if a ValueError arises if h is 0
    
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,0)
    
    #check if the rho_n output vector exists
    
    assert(len(rho_n) >= 1)
       
# Test for the function "optical_depth" and "TOA_transmittances"

@given(st.integers(0,49),st.floats(0.005,1),st.integers(1,50),st.floats(1,10),st.integers(0,49),st.integers(1,50),st.floats(0.001,0.5),st.floats(1,5))
@settings(max_examples = 10)

def test_optical_depth_and_transmittances(z1,dz,z2,h,b,t,csg,coc):
    
    z = fn.z_vector(z1,dz,z2)
      
    rho_n = fn.normalized_density_profile(z,h)
      
    lod,loc=fn.optical_depth(z,dz,b,t,csg,coc,rho_n)
      
    #check if b (cloud's base) and t (cloud's top) are positive 
      
    assert(b > 0)
    assert(t > 0)
      
    #check is t is bigger then b
      
    assert(t > b)
    
    #check if coc and csg are positive
    
    assert(coc > 0)
    assert(csg > 0)
      
    #check if a ValueError arises if b and t are negative 
    
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,-1,15,2,0.2,2,rho_n) #np.array([1]) ->z e rho_n
       
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,10,-1,2,0.2,2,rho_n)  
       
    #check if a ValueError arises if one of the coefficients (cos or csg) is negative 
    
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,10,8,12,-0.2,2,rho_n)  
       
    #check if the lod e loc output vector exist
    
    assert(len(loc) >= 1)
    assert(len(lod) >= 1)
    
    clear_t, cloudy_t = fn.TOA_transmittances(lod, loc, z)

    #check if the clear_t and cloudy_t output vector exist
    
    assert(len(clear_t) >= 1)
    assert(len(cloudy_t) >= 1)
    
