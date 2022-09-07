

import urllib.request, urllib.parse, json 
from math import radians, cos, sin, asin, sqrt
import hashlib
from geopy.geocoders import GoogleV3
import berserk

client = berserk.Client()
apikey = "Nice try"
class HashPassword:
	def __init__(self, value):
		self.value = value
	def Hash(self):
		encoded_info= self.value.encode()	#encode escapes unicode character errors
		hasher = hashlib.sha256(encoded_info)
		hex_dig = hasher.hexdigest()
		print(f"\nSHA256 hash for '{self.value}':{hasher.hexdigest()}")


def getAddressFromCoordiates(lat, long):
    geolocator = GoogleV3(api_key=apikey)
    location = geolocator.reverse((str(lat)+", "+str(long)))
    return location.address


def getCoordiatesFromAddress(addr):
    addr = addr.replace(" ", "%20")
    urlbuild = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?fields=formatted_address%2Cgeometry"
    urlbuild += "&input=" + addr + "&inputtype=textquery"
    urlbuild += "&key=" + apikey

    with urllib.request.urlopen(urlbuild) as url:
        data = json.loads(url.read().decode())
        #print(data)
        for i in data['candidates']:
            return (i['geometry']['location']['lat'],i['geometry']['location']['lng'])

def haversine(a, b): #Gives distance between points a and b in km
    lat1, lon1 = a
    lat2, lon2 = b
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

def getClient():
    with open('./lichess.token') as f:
        token = f.read()
    session = berserk.TokenSession(token)
    client = berserk.Client(session)

a = getCoordiatesFromAddress("12318 Rip Van Winkle Dr. Houston TX")
b = getCoordiatesFromAddress("1000 Bright Circle College Station TX")
print(a)
print(b)    
print (haversine(a,b))
print (getAddressFromCoordiates(a[0],a[1]))

"""string = input("Enter password:")
str_hash = HashPassword(string)
str_hash.Hash()"""
