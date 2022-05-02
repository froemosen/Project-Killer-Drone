import tellopy
import time
drone = tellopy.Tello(port=9000)
drone.connect()
drone.wait_for_connection(10)

drone.takeoff()

time.sleep(3)

drone.send_packet_data("emergency")

time.sleep(5)

drone.land()