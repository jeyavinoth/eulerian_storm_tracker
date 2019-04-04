#/usr/bin/env python
import eulerian_storm_track as est
import numpy as np 
from netCDF4 import Dataset
import plotter
import os

#### Main Code #####


### Prep the data initially for the Eulerian Storm Track Code
year = [2011, 2012]
era_folder = '/mnt/drive5/ERAINTERIM/SLP/'

time = []
slp = np.array([])
tot_time = 0
for i_year in range(year[0], year[1]+1): 
  era_file = os.path.join(era_folder, 'SLP_%d.nc'%(i_year)) 

  nc = Dataset(era_file, 'r')
  nc.set_always_mask(False)
  in_lat = nc.variables['lat'][:]
  in_time = nc.variables['time'][:]
  in_lon = nc.variables['lon'][:]
  in_slp = nc.variables['msl'][:]
  nc.close()

  # stacking slp arrays
  if (slp.size == 0):
    slp = in_slp
  else:
    slp = np.concatenate((slp, in_slp), axis=0)

  # creating the time arrays
  time.extend(list(tot_time + np.arange(0, in_slp.shape[0]*6, 6)))
  tot_time += in_slp.shape[0]*6
  print ('Reading in year %d [%d]!'%(i_year, tot_time))

# creating the lat and lon in grid format
lonGrid, latGrid = np.meshgrid(in_lon, in_lat)

# converting hourly data into daily, and converting Pascals to hectoPascals
slp = slp/100.
slp_daily, time_daily = est.six_hrly_to_daily(slp, year[0], time)

# getting the daily difference X(t+1) - X(t)
diff = est.daily_diff(slp_daily)

# getting the all year standard deviation average
std_dev, time_std = est.std_dev(diff, year[0], time_daily, time_period='all')
std_dev, time_std = est.std_dev(diff, year[0], time_daily, time_period='yearly')
std_dev, time_std = est.std_dev(diff, year[0], time_daily, time_period='seasonally', season='djf')

# plotter.plot(lonGrid, latGrid, slp_daily[0, :, :])
plotter.plot(lonGrid, latGrid, std_dev[0, :, :])
