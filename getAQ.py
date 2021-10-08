import stationToGrid
from dateutil.parser import parse
import pandas as pd
import netCDF4 as nc
import numpy as np
import datetime
import cftime
import xarray as xr

korea_dir_path ='/home/intern01/jhk/AirKorea/'
china_dir_path ='/home/intern01/jhk/China/'

#path < want to make .nc file
def EA_AQdata(begin,end,top,bottom,left,right,lat_step,lon_step) :
    t_begin = parse(begin)
    t_end = parse(end)
    kr_dic, ch_dic = stationToGrid.toGrid(top, bottom, left, right, lon_step, lat_step)
    AQdata = pd.DataFrame
    while t_begin <= t_end :
        if t_begin.day==1 :
            m_data_kr=KRAQtoDF(t_begin,korea_dir_path,kr_dic)
            pd.merge(left=AQdata,right=m_data_kr, how=)
        CHAQtoDF(t_begin,china_dir_path,ch_dic)
        t_begin += datetime.timedelta(days=1)

    return AQdata


def KRAQtoDF(time,dirpath, kr_dic) :
    Ym = time.strftime("%Y.%m").split('.')
    path = dirpath+Ym[0]+'/'+Ym[0]+'년 '+Ym[1]+'월.xlsx'
    df_krAQ = pd.read_excel(path)
    df_krAQ = df_krAQ.drop(['지역','망','측정소코드','주소'],axis=1)
    df_krAQ.rename(columns={'측정일시':'datetime','측정소명':'location'},inplace=True)
    df_krAQ.replace(kr_dic,inplace=True)
    df_krAQ=df_krAQ[df_krAQ['location']<'가']
    df_krAQ=df_krAQ.groupby(['datetime','location'],as_index=False).mean()
    df_krAQ=pd.melt(df_krAQ,id_vars=['datetime','location'],var_name='type')
    df_krAQ=pd.pivot_table(df_krAQ,index=['datetime','type'],columns='location',values='value')
    return df_krAQ

def CHAQtoDF(time,dirpath, ch_dic) :
    Ymd = time.strftime("%Y%m%d")
    path = dirpath+'data/china_aqi_'+Ymd+'.csv'
    df_chAQ = pd.read_csv(path)
    df_chAQ = df_chAQ[df_chAQ['type'].isin(['PM2.5','PM10','SO2','NO2','O3','CO'])]
    df_chAQ['datetime'] = df_chAQ['date'].astype('str') + df_chAQ['hour'].map('{:02}'.format)
    df_chAQ = df_chAQ.drop(['date', 'hour'], axis=1)
    df_chAQ = df_chAQ.set_index(['datetime', 'type'])
    df_chAQ.rename(columns = ch_dic,inplace=True)
    cols = [c for c in df_chAQ.columns if c.find(',')!=-1]
    df_chAQ = df_chAQ[cols]
    return df_chAQ

EA_AQdata('20190101','20190103',50,25,105,145,0.1,0.1)