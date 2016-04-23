import random
import time
import sys
import json

NORTH_PACIFIC_OCEAN=[(58.476242, -152.238999), (59.150478, -139.204289), (53.149817, -150.720687), (53.412560, -136.921860)]
TASMAN_SEA = [(-28.590029, 153.879924), (-28.527255, 166.673027), (-37.386365, 150.020553), (-37.952081, 164.457461)]
MOZAMBIQUE_CHANNEL=[(-27.221539, 32.861022), (-26.966740, 38.370513), (-31.705125, 29.855845), (-31.644232, 37.511891)]
MAR_ARGENTINO=[(-37.064864, -56.486414), (-37.064864, -51.852299), (-47.508760, -65.665527), (-47.448528, -58.179649)]

LOCATIONS=[NORTH_PACIFIC_OCEAN, TASMAN_SEA, MOZAMBIQUE_CHANNEL,MAR_ARGENTINO]
COLORS = ['BLACK', 'BLUE', 'BROWN', 'CLEAR', 'GREEN', 'GREY', 'RED', 'WHITE']
MESH_SIZES=[12, 25, 42, 58, 76, 95, 125, 166, 230]
TWINE_SIZES=[0.5, 1, 2, 3, 4]
ANIMAL_TYPES = ['Crab', 'Crocodile', 'Dolphin', 'Dugong Fish', 'Sea Snake', 'Shark', 'Ray', 'Swordfish', 'Turtle', 'Unknown', 'Whale']

class ReportGenerator(object):

    def strTimeProp(self, start, end, format, prop):
        """Get a time at a proportion of a range of two formatted times.

        start and end should be strings specifying times formated in the
        given format (strftime-style), giving an interval [start, end].
        prop specifies how a proportion of the interval to be taken after
        start.  The returned time will be in the specified format.
        """

        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))

    def randomDate(self, start, end, prop):
        return {
            "__type": "Date",
            "iso": self.strTimeProp(start, end, '%Y-%m-%dT%H:%M:%S', prop)+'.000Z'
        }

    def randomLatLog(self):
        location = LOCATIONS[random.randint(0, len(LOCATIONS)-1)]
        lat_avg1 = (location[0][0]+location[1][0])/2.0
        lat_avg2 = (location[2][0]+location[3][0])/2.0
        if lat_avg1 > lat_avg2:
            lat = random.uniform(lat_avg2, lat_avg1)
        else:
            lat = random.uniform(lat_avg1, lat_avg2)

        lng_avg1 = (location[0][1]+location[2][1])/2.0
        lng_avg2 = (location[1][1]+location[3][1])/2.0
        if lng_avg1 > lng_avg2:
            lng = random.uniform(lng_avg2, lng_avg1)
        else:
            lng = random.uniform(lng_avg1, lng_avg2)
        return {
            "__type": "GeoPoint",
            "latitude": lat,
            "longitude": lng
        }

    def generateRows(self, num_rows):
        results = []
        for i in range(num_rows):
            data = {}
            data['timestamp'] = self.randomDate("2014-01-01T00:01:00", "2016-04-23T00:01:00", random.random())
            data['location'] = self.randomLatLog()
            data['color'] = COLORS[random.randint(0, len(COLORS)-1)]
            data['meshSize'] = MESH_SIZES[random.randint(0, len(MESH_SIZES)-1)]
            data['twineDiameter'] = TWINE_SIZES[random.randint(0, len(TWINE_SIZES)-1)]
            data['emailAddress'] = 'test@test.com'

            if random.randint(0,1) == 1:
                data['animalExists'] = True
                data['animalType'] = ANIMAL_TYPES[random.randint(0, len(ANIMAL_TYPES)-1)]
                data['animalAlive'] = False if random.randint(0,1) == 0 else True
            else:
                data['animalExists'] = False

            results.append(data)
        print json.dumps({"results": results})

if __name__ == '__main__':
    ReportGenerator().generateRows(2000)