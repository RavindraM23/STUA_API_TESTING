import json 

with open("export.json","r") as f:
    f_file = json.load(f)
    f_file = json.dumps(f_file)
    print(type(f_file))