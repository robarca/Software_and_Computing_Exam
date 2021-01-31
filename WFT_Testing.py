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

@given(st.integers(0,49),st.floats(0.005,1),st.integers(50,100))
@settings(max_examples = 10)

def test_z_vector(z1,dz,z2):
    
    z = fn.z_vector(z1,dz,z2,20)
        
    with pytest.raises(ValueError):
       fn.z_vector(-1,0.01,5,20)
       
    #check if a ValueError arises if z2 is smaller then z1
    
    with pytest.raises(ValueError):
       fn.z_vector(10,0.05,5,20)
       
    #check if a ValueError arises if dz in negative
    
    with pytest.raises(ValueError):
       fn.z_vector(1,-0.05,5,20)
    
    #check if a ValueError arises if dz is not in the right range
    
    with pytest.raises(ValueError):
       fn.z_vector(1,10,5,20)
    #check if the z output vector exists
    
    assert(len(z) >= 1)
    
    
# Test for the function "normalized_density_profile"  
        
@given(st.integers(0,49),st.floats(0.005,1),st.integers(50,100),st.floats(1,10))
@settings(max_examples = 10)

def test_normalized_density_profile(z1,dz,z2,h):
    
    z = fn.z_vector(z1,dz,z2,20)
    
    rho_n = fn.normalized_density_profile(z,h)
       
    #check if a ValueError arises if h is negative
     
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,-1) 
    
    #check decreasing monotonicity of rho_n profile
 
    for k in range(0, len(rho_n)-2):
    	assert(rho_n[k] >= rho_n[k+1])
    	 	   
    #check if a ValueError arises if h is 0
    
    with pytest.raises(ValueError):
       fn.normalized_density_profile(z,0)
    
    #check if the rho_n output vector exists
    
    assert(len(rho_n) >= 1)    

# Test for the function "optical_depth" and "TOA_transmittances"

@given(st.integers(0,20),st.integers(51,100),st.floats(1,10),st.integers(20,30),st.integers(31,50),st.floats(0.001,0.5),st.floats(1,5))
@settings(max_examples = 10)

def test_optical_depth_and_transmittances(z1,z2,h,b,t,csg,coc):
    
    dz=0.5
    
    z = fn.z_vector(z1,dz,z2,20)
      
    rho_n = fn.normalized_density_profile(z,h)
      
    #check if b (cloud's base) and t (cloud's top) are positive 
      
    assert(b > 0)
    assert(t > 0)
    
    #check if b is bigger than z1 and t is smaller then z2
   
    assert(b >= z1)
    assert(z2 >= t)
        
    #check is t is bigger then b
      
    assert(t > b)
    
    #check if coc and csg are positive
    
    lod,loc=fn.optical_depth(z,dz,b,t,csg,coc,rho_n)
    assert(coc > 0)
    assert(csg > 0)
      
    #check if a ValueError arises if b and t are negative 
    
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,-1,15,2,0.2,rho_n) 
       
    with pytest.raises(ValueError):
       fn.optical_depth(z,0.005,10,-1,2,0.2,rho_n)  
       
    #check if the lod e loc output vector exist
    
    assert(len(loc) >= 1)
    assert(len(lod) >= 1)
    
    clear_t, cloudy_t = fn.TOA_transmittances(lod, loc, z)

    #check if the clear_t and cloudy_t output vector exist
    
    assert(len(clear_t) >= 1)
    assert(len(cloudy_t) >= 1)

# Test for the function "weighting function"

@given(st.integers(0,20),st.integers(51,100),st.floats(1,10),st.integers(20,30),st.integers(31,50))
@settings(max_examples = 10)

def test_weighting_functions(z1,z2,h,b,t):

    dz=0.5
    
    csg=0.2
    
    coc=2
    
    z = fn.z_vector(z1,dz,z2,20)
      
    rho_n = fn.normalized_density_profile(z,h)
    
    lod,loc=fn.optical_depth(z,dz,b,t,csg,coc,rho_n)
    
    clear_t, cloudy_t = fn.TOA_transmittances(lod, loc, z)
    
    weight_clear, weight_cloudy = fn.weighting_function(clear_t, cloudy_t, z, dz)
    
    #check if the weight_clear and weight_cloudy output vectors exist
    
    assert(len(weight_clear) >= 1)
    assert(len(weight_cloudy) >= 1)
