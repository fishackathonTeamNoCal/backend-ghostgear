import csv
import urllib
from netCDF4 import Dataset
import numpy as np
import json
import os.path

with open('gocd_metadata_9229.csv') as csvfile:  # http://www.nodc.noaa.gov/gocd/index.html search results
  reader = csv.DictReader(csvfile)
  results = []
  for row in reader:
    d = {}

    lng = float(row['Longitude Range(+deg_E)'].split(' ~ ')[0])
    lat = float(row['Latitude Range(+deg_N)'].split(' ~ ')[0])
    
    location = {
      "__type": "GeoPoint",
      "latitude": lat,
      "longitude": lng
    }

    d['location'] = location
    d['startDate'] = {
      "__type": "Date",
      "iso": row['Start Date Time'] 
    }
    d['endDate'] = {
      "__type": "Date",
      "iso": row['End Date Time'] 
    }

    d['minDepth'], d['maxDepth'] = [float(depth) for depth in row['Instrument Depth(m)'].split(' ~ ')]
    d['instrumentType'] = row['Instrument Type']
    file_url = row['Filename of the Station']
    file_name = file_url.split('/')[-1]
    if not os.path.isfile(file_name):
      urllib.urlretrieve(file_url, file_name)
    rootgrp = Dataset(file_name, "r", format="NETCDF4")
    d['avgDirection'] = np.mean([direction[0] for direction in rootgrp.variables['current_direction']])
    print d
    results.append(d)

with open('currentData.json', 'w') as fp:
  json.dump({'results': results}, fp)
