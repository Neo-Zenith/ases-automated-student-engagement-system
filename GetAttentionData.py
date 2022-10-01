import requests
import matplotlib.pyplot as plt
import seaborn as sb

course = "CSC/2"
r = requests.get('http://127.0.0.1:8000/api/engagement/get?course=' + course)

data = r.json()['engaged_status']

count = 0
for i in data:
    plot = sb.lineplot(data[count])
    count += 1
    
plt.show()