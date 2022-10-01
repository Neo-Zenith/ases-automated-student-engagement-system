import requests

course = "CSC/2"
r = requests.get('http://127.0.0.1:8000/api/engagement/get?course=' + course)

print(r.json())