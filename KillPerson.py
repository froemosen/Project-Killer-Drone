#Based on Camera.py from earlier project
import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time
from keras.models import load_model #pip install keras
from PIL import Image, ImageOps
import keyboard

people = ["Other", "Mark", "Kristian", "Lac"]

person = "Kristian" #Write person to kill here

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

#Load model
recognitionModel = load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = numpy.ndarray(shape=(1, 224, 224, 3), dtype=numpy.float32)


def predict(image):
    #resize the image to a 224x224 with the same strategy as in TM2:
    #image = np.array(cap)
    #resizing the image to be at least 224x224 and then cropping from the center        
    size = (224, 224)
    image = Image.fromarray(image)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = numpy.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(numpy.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = recognitionModel.predict(data)
    return numpy.argmax(prediction)

def main():
    drone = tellopy.Tello()
    currentThrottle = 0.0
    currentYaw = 0.0
    found = False

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

        # skip first 50 frames
        frame_skip = 50
        
        drone.takeoff()  
        drone.up(5)                                                                                                                   
        
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
                
                if len(faces) >= 1: #If only one face is detected
                    
                    for (x, y, w, h) in faces:
                        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
                        
                        face = image[y: y+h, x: x+w]
                        print(x+w, y+h)
                        kød = predict(face)
                        print(people[kød])
                        if people[kød] == person: 
                            found = True
                            print(f"I WILL KILL {person}")
                            droneX = int(x+w/2)
                            droneY = int(y+h/2)
                            
                            
                            drone.set_yaw((-1+droneX/480)/1.3)
                            #print(f"Yaw will be {-1+droneX/480}, since droneX is {droneX}")
                            drone.set_throttle((1-droneY/360)/1.3)
                            #print(f"Yaw will be {-1+droneY/360}, since droneX is {droneY}")
                                
                            if droneX > 430 and droneX < 530:
                                drone.set_yaw(0)
                                
                                
                            if  droneY > 310 and droneY < 410:
                                drone.set_throttle(0)
                            
                            
                        else: 
                            print(f"Person is {people[kød]}")   
                            drone.set_pitch(0)
                            drone.set_yaw(0)
                            drone.set_throttle(0)
                            found = False
                            
                elif len(faces) == 0:
                    drone.set_pitch(0)
                    drone.set_yaw(0)
                    drone.set_throttle(0)
                    
                if found == False:
                        drone.set_yaw(0.2) #Turn around and search
                                  
                if keyboard.is_pressed("space"): drone.land()
                    
                                   
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