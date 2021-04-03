import os
x=5
y=20
z=400
while(True):
    x=x*x*562
    y=x*y
    z=(x*y)*(x*y)*z
    print(z,x,y)
    os.system('vcgencmd measure_temp')