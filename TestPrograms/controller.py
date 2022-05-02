import tellopy
drone = tellopy.Tello(port=9000) #Drone defineres
drone.connect() #Connection mellem program og drone etableres
droneFlying = False
btn0Value = 0



def main(btn0, btn1, btn2, btn3, btn4, joy0x, joy0y, joy1x, joy1y): 
	try:			
		if droneFlying:
			#if drone is flying:
			"""
			Noget med joystick
			"""
			#Knapper
			if not btn0:
				btn0Value += 1
				if btn0Value > 20:
					drone.land()
					btn0Value = 0
								

			elif not btn1 and not btn2 and not btn3 and not btn4: #Trykket på alle fire knapper
				pass #Do smthn?

			elif not btn1 and not btn2 and btn3 and btn4: #Trykket på de to nederste knapper
				drone.flip_back()
			elif not btn1 and btn2 and not btn3 and btn4: #Trykket på to knapper til venstre
				drone.flip_left()
			elif btn1 and btn2 and not btn3 and not btn4: #Trykket på to øverste knapper
				drone.flip_forward
			elif btn1 and not btn2 and btn3 and not btn4: #Trykket på to knapper til højre
				drone.flip_right()

			elif not btn1 and btn2 and btn3 and btn4: #Trykket på knap 1
				drone.flip_backleft()
			elif btn1 and not btn2 and btn3 and btn4: #Trykket på knap 2
				drone.flip_forwardleft()
			elif btn1 and btn2 and not btn3 and btn4: #Trykket på knap 3
				drone.flip_forwardright()
			elif btn1 and btn2 and btn3 and not btn4: #Trykket på knap 4
				drone.flip_backright()
					


		#else drone is landed
		else:
			if not btn0:
				drone.takeoff()
				drone.sleep(3)
				droneFlying = True
				

			else: 
				pass

		
		"""
		#Script til dronebevægelse køres, med variablerne
					if btn0 == False and btn0Cool == False:
						btn0Cool = True
						btn1Cool = False
						btn2Cool = False
						btn3Cool = False
						btn4Cool = False
						joy0Cool = False
						joy1Cool = False
						print("btn0", btn0)
							
					elif btn1 == False and btn1Cool == False:
						btn0Cool = False
						btn1Cool = True
						btn2Cool = False
						btn3Cool = False
						btn4Cool = False
						joy0Cool = False
						joy1Cool = False
						print("btn1", btn1)

					elif btn2 == False and btn2Cool == False:
						btn0Cool = False
						btn1Cool = False
						btn2Cool = True
						btn3Cool = False
						btn4Cool = False
						joy0Cool = False
						joy1Cool = False
						print("btn2", btn2)

					elif btn3 == False and btn3Cool == False:
						btn0Cool = False
						btn1Cool = False
						btn2Cool = False
						btn3Cool = True
						btn4Cool = False
						joy0Cool = False
						joy1Cool = False
						print("btn3", btn3)

					elif btn4 == False and btn4Cool == False:
						btn0Cool = False
						btn1Cool = False
						btn2Cool = False
						btn3Cool = False
						btn4Cool = True
						joy0Cool = False
						joy1Cool = False
						print("btn4", btn4)

					elif joy0x > 700:
						#Trykket ned på joystick0
						btn0Cool = False
						btn1Cool = False
						btn2Cool = False
						btn3Cool = False
						btn4Cool = False
						joy0Cool = True
						joy1Cool = False

					elif joy1x > 700:
						#Trykket ned på joystick1
						btn0Cool = False
						btn1Cool = False
						btn2Cool = False
						btn3Cool = False
						btn4Cool = False
						joy0Cool = False
						joy1Cool = True				
					
					elif btn0 == False and  btn1 == False and btn2 == False and btn3 == False and btn4 == False:
						btn0Cool = False
						btn1Cool = False
						btn2Cool = False
						btn3Cool = False
						btn4Cool = False
						joy0Cool = False
						joy1Cool = False
					
					else:
						pass
					
				else: 
					pass
		"""
		#Joysticks? - Skal de være sådan skala-baserede hvor den flyver hurtigere når den er meget rykket?
	except:
		print(Exception)