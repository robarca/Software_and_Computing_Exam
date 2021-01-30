# Weighting Functions and Transmittances 

This is a simple model to compute the weighting functions and transmittances in clear air and in presence of a cloud layer. 

Here, it is assumed that clouds only absorb and emit (i.e there is no scattering), that the system is in Local Thermodynamic Equilibrium (LTE), so that Kirchhoff's law is still valid, and that it's considered a plane-parallel atmosphere using height (_z_) as vertical coordinate .

Considering the optical depth, defined as :

![optical_depth](https://latex.codecogs.com/gif.latex?%5Ctau%20%3D%20%5Cint_%7Bz%7D%5E%7Bz_T%7D%20k_%7B%5Cnu%7D%28z%5E%7B%27%7D%29%5Crho_%7Ba%7D%28z%5E%7B%27%7D%29dz%27)

the monochromatic **transmittance** is defined as a function of the optical depth and the zenith angle:

![transmittance](https://latex.codecogs.com/gif.latex?T_%7B%5Cnu%7D%5Cleft%20%28%20%5Cfrac%7B%5Ctau%20%7D%7B%5Cmu%20%7D%20%5Cright%20%29%3De%5E%7B-%5Cfrac%7B%5Ctau%20%7D%7B%5Cmu%20%7D%7D)

In Atmospheric Physics, when only absorption and emission processes are relevant for our problem, it's possible to write the Schwarzschild’s equation solution to compute upwelling and downwelling radiance at any height and in any direction. In particular the upwelling monochromatic radiance at the top of the atmosphere (_zT_) is: 

![f1](https://latex.codecogs.com/gif.latex?L%28z_T%2C%5Cmu%29%3DL%28z_0%2C%5Cmu%29e%5E%7B-%5Cint_%7Bz_0%7D%5E%7Bz_T%7Dk%5Crho%20_%7Ba%7D%5Cfrac%7Bdz%7D%7B%5Cmu%7D%7D&plus;%5Cint_%7Bz_0%7D%5E%7Bz_T%7D%20kBe%5E%7B-%5Cint_%7Bz_0%7D%5E%7Bz_T%7Dk%5Crho%20_%7Ba%7D%5Cfrac%7Bdz%27%7D%7B%5Cmu%7D%7D%5Crho%20_%7Ba%7D%5Cfrac%7Bdz%7D%7B%5Cmu%7D)

It is quite evident that radiance reaching any level in the atmosphere in any direction depends strongly on the absorption cross section, _k_.

A second form of the solution can be written using the concept of **Weighting Function** (_W_):

![f2](https://latex.codecogs.com/gif.latex?W%28z%2Cz_T%29%5Cequiv%20%5Cfrac%7B%5Cpartial%20%5Ctau%28z%2Cz_T%29%7D%7B%5Cpartial%20z%7D%20%3D%20%5Cfrac%7Bk%5Crho_%7Ba%7D%7D%7B%5Cmu%7D%5Ctau%28z%2Cz_T%29)

so we have: 

![wavefunc](https://latex.codecogs.com/gif.latex?L%28z_T%2C%5Cmu%29%3DL%28z_0%2C%5Cmu%29e%5E%7B-%5Cint_%7Bz_0%7D%5E%7Bz_T%7Dk%5Crho%20_%7Ba%7D%5Cfrac%7Bdz%27%7D%7B%5Cmu%7D%7D&plus;%5Cint_%7Bz_0%7D%5E%7Bz_T%7D%20B%5Cfrac%7B%5Cpartial%20%5Ctau%28z%2Cz_T%29%7D%7B%5Cpartial%20z%7Ddz)

The role of the weighting function can be understood thanks to next example graphs:

![Transvs](https://player.slideplayer.com/16/5022384/data/images/img21.jpg) ![weightvs](https://player.slideplayer.com/16/5022384/data/images/img22.jpg)

The left panel displays the vertical profile of transmissivity and the right panel displays the weighting functions, computed as showen above. The various colors denote 4 different absorption cross sections _k_ while the temperature and concentration profiles are the same.
The blu line is showing a situation that could arise if it's considered an atmospheric window: transmissivity doesn't change a lot, at the surface it is 0.9, which implies that 90% of the energy from the surface is reaching the top of the atmosphere. Watching at the corrispective weighting function profile, it's possible to see that most energy comes from the surface, but also a little from the atmosphere.
Moving towards more absorbing wave numbers (green curve) the transmissivity decreases and only 35% of the energy that is going out from the surface reaches the top of the atmosphere, while the weighting function shows that most of the energy comes from the layers close to the surface, but it also arrives in minor part from layers close to 20 km. For the red and blue curves the surface transmissivity is zero and the associated weighting functions have a maximum in correspondence the inflection of the transmissivity curve, which indicates where the signal mainly comes from.

## Code Structure

This model is based on the connection between these files:

**WFT_Profile.py** : it contains the main program and it's the code that users need to launch;
**WFT_Functions.py** : it contains the principal functions used in the model; 
**Make_Configuration.py** : it creates the file _Configuration.ini_;
**Configuration.ini** : it contains the values of the general input variables this model needs;
**OUTPUT** : it is the folder where final plots are stored;
**WFT_Testing.py** : it contains some tests for the functions used in the model to be sure they work properly;
**README** : it contains a brief theoretical introduction, the characteristics of the code and of the variables used and, finally, the instructions to follow to run the model.

## General Variables

To run the model it's very importanto to understand what the variables in the _Configuration.ini_ file rapresent:

**Bottom_clod** rapresents the quote [km] of the cloud's base. It must be a value between the top and the bottom of the atmosphere (difined later);

**Top_cloud** rapresents the quote [km] of the cloud's base. As above, it must be a value between the top and the bottom of the atmosphere (difined later);

**Cross_section_abs_gas** defines the capacity of the atmosphere to absorb the incoming radiation. It's used to compute the optical depth;

**Abs_coeff_cloud** defines the capacity of the cloud to absorb with the radiation;

**Top_level** is the maximum hight that is rapresented on the final plots;

**z_begin** is the quote of the bottom of the portion of the considered atmosphere. If it's equal to 0, it corresponds to the Earth surafce;

**z_end** is the quote of the top of the portion of the considered atmosphere;

**z_step** rapresents the thickness of each layer considered between the top and the bottom of the atmosphere;

**vertical_height_scale** is the scale parameter for the exponential density profile;





