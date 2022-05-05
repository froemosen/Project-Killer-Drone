#Based on Camera.py from earlier project
import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
import keyboard
import uuid

person = "Mark" #Write person to take images of here
personPath = f"/Images/{person}/"

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        retry = 3
        container = None
        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')

        # skip first 300 frames
        frame_skip = 300
        
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                
                #Grayscale image for face recognition
                gray = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2GRAY)
                
                #Detect faces in image
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(30, 30)
                )       
                
                #print(f"Found {len(faces)} faces")
                
                if len(faces) == 1: #If only one face is detected
                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
                    
                    if keyboard.is_pressed("space"): #If image is being taken (spacebar is pressed down)
                        face = image[y: y+h, x: x+w]
                        status = cv2.imwrite(f"D:\Project-Killer-Drone\Images\{person}\{uuid.uuid1()}.png", face)
                        print(f"Image saved? - {status}")
                    
                                   
                cv2.imshow(f'GetPerson {person}', image)
                cv2.waitKey(1)
                
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
                
                
                   
                    

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
        
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()