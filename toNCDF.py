import pandas as pd
import xarray as xr

df = pd.read_csv("/home/intern01/jhk/EA_AQ_2019_2020.csv")
df["datetime"] = pd.to_datetime(df["datetime"],format="%Y-%m-%d %H:%M:%S")
df = df.rename(columns={"datetime":"time","Lat":"latitude","Lon":"longitude"})
df = df.set_index(['time', 'latitude', 'longitude'])
aqxarray = df.to_xarray()

aqxarray.to_netcdf("/home/intern01/jhk/EA_AQ_1920.nc",mode='w')