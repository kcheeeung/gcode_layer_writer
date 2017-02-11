import json

def write_json(filename):
	data = {x:0, y:0, z:0, pwm:0, unitsize:0, folder:"test_layers"}
	with open(filename, "w") as fp:
		json.dump(data, fp)

def load_json(filename):
	with open(filename, "r") as fp:
		data = json.load(fp)

write_json("config.json")
load_json("config.json")