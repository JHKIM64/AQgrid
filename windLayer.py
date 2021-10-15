import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as amp
from numba import njit, cuda
from timeit import default_timer as timer

import cartopy.crs as ccrs

weather = xr.open_dataset("/home/intern01/jhk/ECMWF_Land/ECMWR_EA_CLCOND_1920.nc")

index = weather.indexes
time = np.array(index.__getitem__('time'))

lon =  np.array(index.__getitem__('longitude'))
lat =  np.array(index.__getitem__('latitude'))

X,Y = np.meshgrid(lon,lat)
U = np.array(weather.u10.isel(time=0).values)
V = np.array(weather.v10.isel(time=0).values)


fig, ax  = plt.subplots(figsize =(40,30))
Q=ax.quiver(X,Y,U,V)

start = timer()

@njit()
def update_quiver(t):
    U = np.array(weather.u10.isel(time=t).values)
    V = np.array(weather.v10.isel(time=t).values)

    Q.set_UVC(U,V)
    return Q,

anim = amp.FuncAnimation(fig, update_quiver, frames=30,interval=300)
anim.save('test.gif')
print(timer()-start)
plt.show()
# def windplot(t) :
#     initFrame.set_array(weather.isel(time=t).values.flatten())
#     # weather.isel(time=t).plot.quiver(x='longitude',y='latitude',u='u10',v='v10')
#
# initFrame = weather.isel(time=0).plot.quiver(x='longitude',y='latitude',u='u10',v='v10')
#
# ani = amp.FuncAnimation(fig,windplot,frames=20)
# plt.show()
#
# for t in range(0,20) :
#     windplot(t)
#     plt.show()



# convert -delay value(35-40) -loop 0 'filename image_*.png' 'test.gif'