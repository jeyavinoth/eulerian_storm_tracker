#!/usr/bin/env python

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np 

def plot(lonGrid, latGrid, data, show=True):

  lllat = np.nanmin(latGrid) 
  urlat = np.nanmax(latGrid) 
  lllon = np.nanmin(lonGrid) 
  urlon = np.nanmax(lonGrid)

  m = Basemap(projection='cyl', urcrnrlat=urlat, urcrnrlon=urlon, llcrnrlat=lllat, llcrnrlon=lllon)
  m.drawcoastlines()
  m.pcolormesh(lonGrid, latGrid, data, cmap='jet')
  m.colorbar()
  m.drawparallels(np.arange(-90, 90, 25), labels=[True, False, False, False])
  m.drawmeridians(np.arange(-180, 180, 50), labels=[False, False, False, True])

  if (show):
    plt.show()
