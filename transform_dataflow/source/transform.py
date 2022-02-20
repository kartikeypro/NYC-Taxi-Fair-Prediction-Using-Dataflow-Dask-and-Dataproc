import apache_beam as beam
import pandas as pd
import datetime
from math import cos, asin, sqrt, pi
import numpy as np

class getRecord(beam.DoFn):
    def process(self, element):
        #Converting datframe into records
        element = element.split(",")
        return [element]

def throwEmpty(element):
    # Remove records containing nan values.
    for i in element:
        if(len(i)==0):
            return False
    return True
    
class mapColumns(beam.DoFn):
    def process(self, element):
        # Dropping index and key columns.
        x = lambda x:{
            "fare_amount":float(x[1]),
            "pickup_datetime":x[2],
            'pickup_longitude':float(x[3]),
            'pickup_latitude':float(x[4]), 
            'dropoff_longitude':float(x[5]), 
            'dropoff_latitude':float(x[6]),
            'passenger_count':float(x[7])
        }
        element = x(element)
        return [element]

class swap(beam.DoFn):
    def process(self, element):
        # Swaps the value of longitude and latitude incase their absolute values are contrary to the trend seen in data
        # observed notebook
        swap = 0
        if(abs(element['pickup_longitude'])<abs(element['pickup_latitude'])):
            swap = element['pickup_longitude']
            element['pickup_longitude'] = element['pickup_latitude']
            element['pickup_latitude'] = swap
        if(abs(element['dropoff_longitude'])<abs(element['dropoff_latitude'])):
            swap = element['pickup_longitude']
            element['dropoff_longitude'] = element['dropoff_latitude']
            element['dropoff_latitude'] = swap 
        return [element]

def removeRows(element):
    # Removes the record containing anomalies already discussed in observation notebook.
    if(element['passenger_count']<1 or element['passenger_count']>6):
        return False
    elif(element['fare_amount']<=0 or element['fare_amount']>500):
        return False
    elif(abs(element['pickup_latitude'])<40 or abs(element['pickup_latitude'])>46):
        return False
    elif(abs(element['dropoff_latitude'])<40 or abs(element['dropoff_latitude'])>46):
        return False
    elif(abs(element['pickup_longitude'])<71 or abs(element['pickup_longitude'])>80):
        return False
    elif(abs(element['dropoff_longitude'])<71 or abs(element['dropoff_longitude'])>80):
        return False
    else:
        return True

class transformDate(beam.DoFn):
    # Date Time transformations
    def process(self, element):
        datetime = pd.to_datetime(element['pickup_datetime'],format='%Y-%m-%d %H:%M:%S UTC')
        element['year'] = datetime.year
        element['month'] = datetime.month
        element['day'] = datetime.day
        element['weekday'] = datetime.weekday()
        element['hour'] = datetime.hour
        del element['pickup_datetime']
        return [element]


class getDistance(beam.DoFn):
    # Calculates the distance using coordinates.
    def process(self,element):
        p = pi/180
        a = 0.5 - cos((element['dropoff_latitude']-element['pickup_latitude'])*p)/2 
        + cos(element['pickup_latitude']*p) * cos(element['dropoff_latitude']*p) * (1-cos((element['dropoff_longitude']-element['pickup_longitude'])*p))/2
        element['distance']= 12742 * asin(sqrt(a))
        return [element]