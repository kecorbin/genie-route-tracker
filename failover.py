import os
import sys
from meraki import meraki

# change these
ORG_ID=626279
NETWORK_MAP = {"Hub 1": "N_664280945037204513",
               "Hub 2": "N_664280945037230359"}


def get_route_by_subnet(apikey, networkid, subnet):
    routes = meraki.getstaticroutes(apikey, networkid)
    for r in routes:
        if r['subnet'] == subnet:
            return r
    return None


apikey = os.getenv("MERAKI_API_KEY", None)
if not apikey:
    print("Please make sure you have MERAKI_API_KEY environment variable set")
    sys.exit(1)
myOrgs = meraki.myorgaccess(apikey)
print(myOrgs)

nets = meraki.getnetworklist(apikey, ORG_ID)
print('nets available: ')
for n in nets:
    print(n['name'])


print("routes available at hub1")
h1routes = meraki.getstaticroutes(apikey, NETWORK_MAP['Hub 1'])
for r in h1routes:
    print(r)

print("routes available at hub2")
h1routes = meraki.getstaticroutes(apikey, NETWORK_MAP['Hub 2'])
for r in h1routes:
    print(r)

interesting_route = get_route_by_subnet(apikey, NETWORK_MAP['Hub 2'], '4.4.4.0/24')
print(interesting_route)

#delete = meraki.delstaticroute(apikey, NETWORK_MAP['Hub 1'], '0935ae7a-1247-4adb-aa90-256eb2e0b5cd')

# routes = meraki.getstaticroutes(apikey, ORG_ID, suppressprint=True)
# print(routes)
