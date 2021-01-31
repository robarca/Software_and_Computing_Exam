#!/usr/bin/python3
#----------------------------------------
# Functions used in WFT_Profile.py
#----------------------------------------

import numpy as np

def z_vector(z1,dz,z2,top):
    
    """ This function computes the heigth vector between z1 and z2.
    
        INPUT:
            
            z1          : altitude at the lowest level of the
                          portion of the atmosphere under consideration
            
            z2          : altitude at the heighest level of the
                          portion of the atmosphere under consideration   
                        
            dz          : step value of the vector 
            
            top	 : top level of the atmosphere for the final plots
            
        OUTPUT:
            
            z           : altitude vector of the portion of atmosphere 
                          under consideration
    
    """
    if  dz <= 0 or dz > 0.5*(z2-z1):
         raise ValueError (
                'dz is not correct!')
                
    if  z1 < 0:
         raise ValueError (
                'The starting quote must be, at least, 0!')
         
    if z2 < 0 or z2 <= z1:
         raise ValueError (
                'The highest quote must be greater than the lowest one!')
    if  top > z2:
         raise ValueError (
                'The top of the plotted atmosphere must be smaller than the top of the analyzed atmosphere')
    
    z = np.arange(z1,z2,dz)
    
    return z


def normalized_density_profile(z,h):
    
    """ This function computes the normalized density 
        profile starting from the exponential profile (rho) and 
        a normalization factor (norm)
   
            
        INPUT:
            
            z           : altitude vector of the portion of atmosphere 
                          under consideration
            
            h           : vertical scale height for the exponential profile 
            
        
        OUTPUT:
            
            rho_n       : normalized density profile
                          
    """
    
    if h <= 0:
        raise ValueError (
    		'Vertical scale height h must be greater then 0!')
        
    # Explonential density profile 
    
    rho = np.exp(-z/h)
    
    # Normalization factor
     
    norm=h*(1-np.exp(-(z[len(z)-1])/h))
    
    # Normalized density profile
    
    rho_n = rho*norm
    
    return rho_n

def optical_depth(z,dz,b,t,csg,coc,rho_n):
        
    """ This function computes the molecular optical depth vector (lod)
         and the total optical depth (loc).
         The former is computed using only the gas absorption (csg), while
         the latter also takes into account the cloud layer (coc)
          
            
         INPUT:
            
             z           : altitude vector of the portion of atmosphere 
                           under consideration
            
             dz          : step value of the vector z
             
             b           : cloud base
             
             t           : cloud top
             
             csg         : cross section per unit mass of absorbing gas
             
             coc         : absorption coefficient of cloud layer
             
             rho_n       : normalized density profile
            
        
         OUTPUT:
            
             lod         : molecular optical depth vector
             
             loc         : total optical depth vector
                          
    """
    # Check if b and t are in the layer of the considered atmosphere
    
    if z[0] > b:
        raise ValueError (
    		'The bottom of the cloud cannot be smaller than the bottom of atmosphere')
    
    if t > z[len(z)-1]:
        raise ValueError (
    		'The top of the cloud cannot be greater than the top of atmosphere')
    
    if b >= t:
    	raise ValueError (
    		'The top of the cloud must be greater than the bottom')
    			    		
    # Initialization of molecular optical depth vector
    
    lod = np.zeros(len(z))
    
    # Molecular optical depth vector 
    
    for j in range(len(lod)-2, -1, -1):
        lod[j] = csg*(rho_n[j]+rho_n[j+1])*0.5*dz
    
    # Initialization of total optical depth vector
    
    loc=1*lod
    
    # Position of the base and the top of the cloud in the vector z
    z=list(z)
    
    # Test if b value and t value are included in z vector
    
    if b in z:
    	cloud_base = z.index(b)
    else:
        raise ValueError (
    		'The bottom of the cloud is not contained into the z vector!')
   	
    if t in z:
    	cloud_top = z.index(t)
    else:    	
        raise ValueError (
    		'The top of the cloud is not contained into the z vector!')
        
    # Total optical depth vector
    
    for k in range(cloud_base+1, cloud_top):
        loc[k]=loc[k]+coc*dz
        
    return lod, loc    
    
def TOA_transmittances(lod, loc, z):    
    
    """ This function computes the transimittances at the 
         top of the atmosphere (TOA) for both cases: clear sky 
         and cloudy sky.
                  
            
         INPUT:
            
             z           : altitude vector of the portion of atmosphere 
                           under consideration
                           
             dz          : step value of the vector z
             
             lod         : molecular optical depth vector
             
             loc         : total optical depth vector
             
        
        OUTPUT:
            
             clear_t     : clear sky transmittance vector
             
             cloudy_t    : cloudy sky transmittance vector
                          
    """
    
    # Initialization of the vectors
    
    clear_t = np.ones(len(z))
    cloudy_t = np.ones(len(z))
    
    # Transmittance vectors
    
    for i in range(len(z)-2, -1, -1):
        clear_t[i] = clear_t[i+1]*np.exp(-lod[i])
        cloudy_t[i] = cloudy_t[i+1]*np.exp(-loc[i])
    
    #check if transmittances values are reasonable
    
    for i in range(1,len(clear_t)):
    	if (clear_t[i]<0) or (clear_t[i]>1):
    		raise ValueError (
    		'Transmittance must be between 0 and 1')
    	if (cloudy_t[i]<0) or (cloudy_t[i]>1):
    		raise ValueError (
    		'Transmittance must be between 0 and 1')
    
    return clear_t, cloudy_t

def weighting_function(clear_t, cloudy_t, z, dz):
    
    """ This function computes the weighting function
        for both cases: clear sky (using clear_t vector) 
        and cloudy sky (using cloudy_t vector).
                  
            
         INPUT:
            
             z                : altitude vector of the portion of atmosphere 
                                 under consideration
                           
             clear_t          : clear sky transmittance vector
             
             cloudy_t         : cloudy sky transmittance vector
             
                        
         OUTPUT:
            
             weight_clear     : clear sky transmittance vector
             
             weight_cloudy    : cloudy sky transmittance vector
                          
    """
    
    # Initialization of the vectors
    
    weight_clear = np.zeros(len(z))
    weight_cloudy = np.zeros(len(z))

    for i in range(1,len(z)):
         weight_clear[i] = (clear_t[i]-clear_t[i-1])/dz
         weight_cloudy[i] = (cloudy_t[i]-cloudy_t[i-1])/dz
     
    return weight_clear, weight_cloudy
    
    
