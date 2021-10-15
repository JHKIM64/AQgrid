import pandas as pd
import xarray as xr
import dask.dataframe as dd

df = dd.read_csv("/home/intern01/jhk/EA_AQ_2019_2020.csv", sorted_index=True, mode='r')

def dasktoxarray(ddf, indexname='index') :
    ds = xr.Dataset()
    ds[indexname] = ddf.index
    for key in ddf.columns:
        ds[key] = (indexname, ddf[key].to_dask_array().compute_chunk_sizes())
    return ds

aqarray = dasktoxarray(df,["datetime","Lat","Lon"])
