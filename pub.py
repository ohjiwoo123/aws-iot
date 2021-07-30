import face_recognition
import picamera
import numpy as np
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# GPIO ultra sonic Setting
trig=17
echo=18
ledpin=14

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
####################

# Camera Setting
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)
# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
me_image = face_recognition.load_image_file("me.jpg")
me_face_encoding = face_recognition.face_encodings(me_image)[0]
# Initialize some variables
face_locations = []
face_encodings = []
#########################

#  Code Start (LOOP) !!
while True:
    mqttc=mqtt.Client()
    mqttc.connect("192.168.0.100",1883)
    GPIO.output(trig,False)
    time.sleep(15)

    GPIO.output(trig,True)
    time.sleep(0.00001)
    GPIO.output(trig,False)

    while GPIO.input(echo)==0:
        pulse_start=time.time()

    while GPIO.input(echo)==1:
        pulse_end=time.time()

    pulse_duration=pulse_end - pulse_start
    distance=pulse_duration*17000
    distance=round(distance,2)
    print("Distane: ",distance, "cm")

    # If distance lower than 30, LED ON,
    # Camera Recognition Start
    if distance<30:
        GPIO.setwarnings(False)
        GPIO.setup(ledpin,GPIO.OUT)
        GPIO.output(ledpin,True)
        print("distance is lower than 30")
        mqttc.publish("iot/ledsonic", "LED ON")

        print("Capturing image.")
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        print("Face Recognition Failed !!")
        mqttc.publish("iot/ledsonic", "Face Recognition Failed !!")
        face_encodings = face_recognition.face_encodings(output, face_locations)
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([me_face_encoding], face_encoding)
            name = "<Unknown Person>"
            
            # If (name=="Me"), it means face recognition success.  
            # Print "Pass" message and Publish "Success" message
            if match[0]:
                name = "Me"
            if(name=="Me"):
                print("Face Recognition PASS !!")
                mqttc.publish("iot/ledsonic", "Face Recognition Success !!")
            print("This image includes in our data {}!".format(name))
                        
    # if distance is higher than 30, "LED OFF"
    # Print "come to sensor" and Publish "Nothing to Recognize" message
    if distance>30:
        GPIO.setwarnings(False)
        GPIO.setup(ledpin,GPIO.OUT)
        GPIO.cleanup(ledpin)
        print("distance is higher than 30")
        print("please come to sensor closer")
        mqttc.publish("iot/ledsonic", "LED OFF")
        mqttc.publish("iot/ledsonic", "There is nothiing to Recognize")


