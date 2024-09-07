p= open("locationsP.csv", "r")
c = open("locationsC.csv", "w")

for l in p:
	q = l.strip().split(",")
	if int(q[1]) == 0:
		x = 32
		for i in range(9):
			#Left Long
			c.write("LL")
			c.write(",")
			c.write(str((x*(i+1))+(50*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")
		

	elif int(q[1]) == -384:
		x = 32
		for i in range(4):
			#Left Half
			c.write("LH")
			c.write(",")
			c.write(str((x*(i+1))+(50*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")
		

	elif int(q[1]) == -500:
		x = 32
		for i in range(3):
			#Left Quarter
			c.write("LQ")
			c.write(",")
			c.write(str((x*(i+1))+(50*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[1]) == 448:
		x = 480
		for i in range(10):
			#Right Half
			c.write("RH")
			c.write(",")
			c.write(str((x+(50*i))))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[1]) == 300:
		x = 332
		for i in range(8):
			#Right Most
			c.write("RM")
			c.write(",")
			c.write(str((x+(70*i))))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[1]) == 128:
		x = 160
		for i in range(9):
			#Right Long
			c.write("RL")
			c.write(",")
			c.write(str((x*(i+1))+(50*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[1]) == 64:
		x= 224
		for i in range(1,4,2):
			#Middle
			c.write("M")
			c.write(",")
			c.write(str((x*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	if int(q[3]) == 500:
		x = 532
		for i in range(3):
			#Small middle
			c.write("SM")
			c.write(",")
			c.write(str((x+70*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[3]) == 600:
		x = 632
		for i in range(3):
			#Small right
			c.write("SR")
			c.write(",")
			c.write(str((x+70*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[3]) == 100:
		x = 132
		for i in range(3):
			#Small leftmost
			c.write("SLM")
			c.write(",")
			c.write(str((x+70*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")

	elif int(q[3]) == 30:
		x = 62
		for i in range(3):
			#Small left
			c.write("SL")
			c.write(",")
			c.write(str((x+70*i)))
			c.write(",")
			c.write(str(int(q[2])-15))
			c.write(",")
			c.write("\n")


	

p.close()
c.close()
