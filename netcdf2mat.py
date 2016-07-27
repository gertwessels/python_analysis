#!/usr/bin/env python
# usage: >> python netcdf2mat.py <input netcdf filename .nc> <output matlab filename .mat>

import sys
from netCDF4 import Dataset
import datetime
import numpy as np
import scipy.io as sio

# TODO- include error if statement if too many arguments
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#rint 'Argument List:', str(sys.argv)

nc = Dataset(str(sys.argv[1]))

sst = nc.variables['analysed_sst'][:]
fillvalue = nc.variables['analysed_sst']._FillValue
add_offset = nc.variables['analysed_sst'].add_offset
# convert sst to matlab friendly matrix
sst = np.array(sst)
sst[np.where(sst == fillvalue)] = np.nan 
# convert to deg C (by removing offset)
sst = sst - add_offset
# swap axes to make time axos z-dim.
sst = np.transpose(sst, (2, 1, 0))

lon = nc.variables['lon'][:]
lon = np.array(lon)
lat = nc.variables['lat'][:]
lat = np.array(lat)

secondsSince = nc.variables['time'][:] # seconds since 1981-01-01
# convert to datetime and get years, months, days
year = np.empty(len(secondsSince))
month = np.empty(len(secondsSince))
day = np.empty(len(secondsSince))
basedate = datetime.datetime(1981,1,1)
for i in range(len(secondsSince)):
	year[i] = datetime.datetime.fromordinal(basedate.toordinal()+secondsSince[i]/24/60/60).year
	month[i] = datetime.datetime.fromordinal(basedate.toordinal()+secondsSince[i]/24/60/60).month
	day[i] = datetime.datetime.fromordinal(basedate.toordinal()+secondsSince[i]/24/60/60).day
nc.close()
year = np.array(year)
month = np.array(month)
day = np.array(day)

# convert to double for matlab
sst = np.float64(sst)
lon = np.float64(lon)
lat = np.float64(lat)
year = np.float64(year)
month = np.float64(month)
day = np.float64(day)

# save as .mat file
sio.savemat(str(sys.argv[2]), {'sst':sst, 'lon':lon, 'lat':lat, 'year':year, 'month':month, 'day':day})
