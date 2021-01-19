import json

with open('provinsi.txt') as f:
    data = f.read()

js = json.loads(data)

print(js)
