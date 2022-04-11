from data_request import data_request
import datetime

def today():
    return datetime.date.today().strftime('%Y%m%d')

# list of tuples as (latitude, longitude)
locations = [(-8,-46)]

# start/end formatted as YYYYMMDD
START = '2022'+'01'+'01'
END = today()
PARAMETERS = "T2M,T2M_MAX,T2M_MIN,RAIN,ALLSKY_SFC_SW_DWN"

df = data_request(locations, START, END, PARAMETERS, data_output='excel')

print(df)