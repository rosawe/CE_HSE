#!/usr/bin/env python

from numpy import *
from string import *
import sys
from math import pi

# This script reads in mesa profile data files and converts to FLASH format.
# Approx21 is assumed, but an option exist to convert an Approx21 MESA model
# into a Aprox19 model for FLASH.
#  call signature:
#  > ./read_mesa.py [name of mesa file] [optional: doAp19, if present do Aprox19]

# First, check if the Aprox19 flag is passed in
if len(sys.argv) > 2:
    doAp19 = bool(sys.argv[2])
else:
    doAp19 = False

# Read some header info from MESA model profile
#model, age = loadtxt(sys.argv[1], usecols=(0,5), unpack=True, skiprows=2)

# Read data
data = genfromtxt(sys.argv[1], skip_header=5, names=True)
data = flipud(data)

print(data[0]) 

ironCoreMass = False
feThresh = 0.0
coreMass = 0.0
coreRad = 0.0
mass = 0.0
doXi = False
if ironCoreMass:
    for i in range(len(radius)):
        iron = cr56[i] + fe52[i] + fe54[i] + fe56[i] + ni56[i]
        if iron >= feThresh:
            rad1 = radius[i]
            if i == 0:
                rad0 = 0.0
            else:
                rad0 = radius[i-1]
            coreMass += iron*dens[i]*4./3.*pi * (rad1**3 - rad0**3)
            coreRad = max(coreRad, radius[i])
        if doXi:
            mass += dens[i]*4./3.*pi * (rad1**3 - rad0**3)
            if mass >= 5e33:
                print(mass, radius[i], 2.5/(radius[i]/1e8))
                doXi = False
    print(coreRad/1e5, coreMass)
    exit()

# Now fix radius.  MESA radius is outer radius of shell.
# if 'radius_cm' in data:
#     radius = data['radius_cm']
# else:
#     radius = data['radius']*6.957e10
radius = data['radius_cm']
radius[0] = 0.5*radius[0]
for i in range(1,size(radius)):
    radius[i] = 0.5*(radius[i] + radius[i-1])

# Assume piece-wise constant for every variable, but adjust velocity in first zone.
dvdr = data['velocity'][0] / radius[0]
data['velocity'][0] = radius[0]*dvdr

# Aggregate Iron peak into fe54 for Aprox19
if doAp19:
    fe54 = fe54 + fe56 + cr56

# Now print header
print("# This is a MESA 1D progenitor", sys.argv[1]) #, "model", model, ", age", age, " yrs"
if doAp19:
    print("number of variables = 27")
else:
    print("number of variables = 29")
print("dens")
print("temp")
print("ye  ")
print("velx")
print("pres")
print("entr")
print("abar")
print("enuc")
print("neut")
print("h1  ")
print("prot")
print("he3 ")
print("he4 ")
print("c12 ")
print("n14 ")
print("o16 ")
print("ne20")
print("mg24")
print("si28")
print("s32 ")
print("ar36")
print("ca40")
print("ti44")
print("cr48")
if not doAp19:
    print("cr56")
print("fe52")
print("fe54")
if not doAp19:
    print("fe56")
print("ni56")

# Here comes the data
for i in range(size(radius)):
    if doAp19:
        print(radius[i], dens[i], temp[i], ye[i], velx[i], pres[i], entr[i], enuc[i], neut[i], h1[i], prot[i], he3[i], he4[i], c12[i], n14[i], o16[i], ne20[i], mg24[i], si28[i], s32[i], ar36[i], ca40[i], ti44[i], cr48[i], fe52[i], fe54[i], ni56[i])
    else:
        print(radius[i], data['rho'][i], data['temperature'][i], data['ye'][i], data['velocity'][i], data['pressure'][i], data['entropy'][i], data['abar'][i], data['eps_nuc'][i], data['neut'][i], data['h1'][i], data['prot'][i], data['he3'][i], data['he4'][i], data['c12'][i], data['n14'][i], data['o16'][i], data['ne20'][i], data['mg24'][i], data['si28'][i], data['s32'][i], data['ar36'][i], data['ca40'][i], data['ti44'][i], data['cr48'][i], data['cr56'][i], data['fe52'][i], data['fe54'][i], data['fe56'][i], data['ni56'][i])
