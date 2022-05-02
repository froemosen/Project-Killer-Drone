#pip3 install pyserial
import serial
import sys
import controller

btn0Cool = False
btn1Cool = False
btn2Cool = False
btn3Cool = False
btn4Cool = False
joy0Cool = False
joy1Cool = False

serialPortName = "COM7" #Skal sandsynligvis ændres. Kommer an på porten som arduino sidder i.  
baudRate = 9600 #Defineret i main.cpp
fejlStop = 0 #Bruges til at programmet forsøget at finde data mere end én gang. (Vi oplevede crashes fordi at serial.readline ikke var 100% reliable)
try:
	s = serial.Serial(serialPortName,baudRate,timeout=1)
except:
	print("Kunne ikke finde data gennem", serialPortName, "Husk at tjekke hvilket port arduino kører igennem")
	sys.exit(1)

print("Tilslutning lavet - Venter på serial data\n")

while(True):
	try:
		while(s.is_open):
    			
			if(s.in_waiting>0):
				rxLine=s.readline().decode("ascii").strip()
				#print("Recieved:",rxLine) #Bruges hvis man gerne vil have den rå data printet ud

					
				rxSplit = rxLine.split(",") #Liste laves, hvor den splitter data efter hvert komma
					
				#Variabler defineres ud fra splittet liste
				btn0 = bool(int(rxSplit[0]))
				btn1 = bool(int(rxSplit[1]))
				btn2 = bool(int(rxSplit[2]))
				btn3 = bool(int(rxSplit[3]))
				btn4 = bool(int(rxSplit[4]))
				joy0x = float(rxSplit[5])
				joy0y = float(rxSplit[6])
				joy1x = float(rxSplit[7])
				joy1y = float(rxSplit[8])

				
					
				#controller.main(btn0, btn1, btn2, btn3, btn4, joy0x, joy0y, joy1x, joy1y)
				
	except:
		print("Fejl efter tilslutning til serial (Fejlopsætning af arduino?)\nLeder efter ny data\n")
		fejlStop+=1 

		if fejlStop > 30: #Der bliver ledt efter data 30 gange, da den ikke altid kan frembringe data første gang. 
			print("Fejl efter 30 forsøg. Lukker programmet efter input") #Efter 30 forsøg er det sikkert at systemet har en fejl. 
			input()
			break