p= open("locationsP.csv", "r")
e = open("locationsE.csv", "w")

for l in p:

	q = l.strip().split(",")
	if int(q[1]) == 0:
		for i in range(2):
			x = int(q[1]) + 310*i
			#Left Long
			e.write("LL")
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(int(q[2])-50))
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(x+300))
			e.write("\n")
		


	elif int(q[1]) == -384:
		x = 10
		#Left Half
		e.write("LH")
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(int(q[2])-50))
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(x+300))
		e.write("\n")
		

	elif int(q[1]) == -500:
		x = 10
		#Left Quarter
		e.write("LQ")
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(int(q[2])-50))
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(x+200))
		e.write("\n")

	elif int(q[1]) == 448:
		x = 458
		#Right Half
		e.write("RH")
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(int(q[2])-50))
		e.write(",")
		e.write(str(x))
		e.write(",")
		e.write(str(x+300))
		e.write("\n")

	elif int(q[1]) == 300:
		for i in range(2):
			x = int(q[1]) + 210*i
			#Right Most
			e.write("RM")
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(int(q[2])-50))
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(x+200))
			e.write("\n")

	elif int(q[1]) == 128:
		for i in range(2):
			x = int(q[1]) + 310*i
			#Right Long
			e.write("RL")
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(int(q[2])-50))
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(x+300))
			e.write("\n")

	elif int(q[1]) == 64:
		for i in range(2):
			x = int(q[1]) + 10 + 310*i
			#Middle
			e.write("M")
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(int(q[2])-50))
			e.write(",")
			e.write(str(x))
			e.write(",")
			e.write(str(x+300))
			e.write("\n")

p.close()
e.close()






p= open("locationsP.csv", "r")
e = open("locationsE.csv", "r")
mid = open("bluelocs.csv", "w")
for l in e:
	for i in range(5):
		e.readline()
	mid.write(l)


p.close()
e.close()
mid.close()


p= open("locationsP.csv", "r")
e = open("locationsE.csv", "r")
fin = open("greenlocs.csv", "w")
for l in e:
	for i in range(15):
		e.readline()
	fin.write(l)

p.close()
e.close()
fin.close()


p= open("locationsP.csv", "r")
e = open("locationsE.csv", "r")
mid = open("bluelocs.csv", "r")
fin = open("greenlocs.csv", "r")

proc = open("redlocs.csv", "w")
for l in e:
	if l not in mid and l not in fin: 
		proc.write(l)


p.close()
e.close()
fin.close()
mid.close()

proc.close()
