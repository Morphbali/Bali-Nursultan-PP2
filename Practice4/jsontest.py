import json
import os

path=os.path.join(os.path.dirname(__file__),"sample-data.json")

f=open(path)
data=json.load(f)

print("Interface Status")
print("="*60)
print("DN Description Speed MTU")

for i in data["imdata"]:
    a=i["l1PhysIf"]["attributes"]
    print(a["dn"],a["descr"],a["speed"],a["mtu"])