data = {x:0, y:0, z:0, pwm:0, unitsize:0, folder:"test_layers"}
with open('config.json', "w") as fp:
	json.dump(data, fp)