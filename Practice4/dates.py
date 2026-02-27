#1
from datetime import datetime,timedelta

print(datetime.now()-timedelta(days=5))
#2
from datetime import datetime,timedelta

d=datetime.now()

print(d-timedelta(days=1))
print(d)
print(d+timedelta(days=1))
#3
from datetime import datetime

print(datetime.now().replace(microsecond=0))
#4
from datetime import datetime

a=datetime.strptime(input(),"%Y-%m-%d %H:%M:%S")
b=datetime.strptime(input(),"%Y-%m-%d %H:%M:%S")

print(int((b-a).total_seconds()))