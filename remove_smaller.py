import os

print('removing')
files = [f for f in os.listdir('individual') if os.path.isfile("individual/"+f)]
for f in files:
    size = os.path.getsize("individual/"+f)
    if size < 1000:
        print("removing individual/"+f +": size = ", size)
        os.remove("individual/"+f)
