import random
l=120
g = 100
f = open("locationsP.csv", "w")
for i in range(100):
	c = random.choice(["L","M","R"])
	#Left
	if c =="L":
		p = random.choice([0,-384, -500])
		if p == -384:
			x = 500
		elif p == -500:
			x = 600
		else:
			x = 0
	#Right
	elif c =="R":
		p= random.choice([448, 300, 128])
		if p == 448:
			x=100
		elif p == 300:
			x = 30
		else:
			x = 0
	#Middle
	else:
		p = 64
		x = 0

	f.write(str(c))
	f.write(",")
	f.write(str(p))
	f.write(",")
	f.write(str(l))
	f.write(",")
	f.write(str(x))
	f.write(",")
	f.write(str(l))
	f.write(",")
	f.write(str(g))
	f.write("\n")
		
	l+=200
	g-=1

f.close()
