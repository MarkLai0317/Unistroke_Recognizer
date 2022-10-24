import json
json_decoded = []
new_json = {}
with open('./symbol.json') as json_file:
    json_decoded = json.load(json_file)

    for key, value in json_decoded.items():
        new_points = []
        for point in value:
            new_points.append([point[1],point[2], 0])
        
        new_json[key] = new_points

with open('./symbol.json', 'w') as json_file:
    json.dump(new_json, json_file)
    


