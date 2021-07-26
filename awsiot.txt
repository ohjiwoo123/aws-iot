AWS IoT Core 

참고 유튜브 : https://www.youtube.com/watch?v=kPLafcrng-c&list=LL&index=3&t=1201s
(외국인 어린 친구가 설명을 정말 잘해주심)

python3 -m venv venv
source venv/bin/activate

pip3 install opencv-python
pip3 install dlib
pip3 install face_recognition
pip3 install RPi.GPIO
pip3 install picamera
pip3 install paho-mqtt
pip3 install AWSIoTPythonSDK

---------------------------------------
awsiotcore.py 파일을 만든다
----------------------------------------

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import face_recognition
import picamera
import numpy as np
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("clientid")
# For TLS mutual authentication
myMQTTClient.configureEndpoint("ai628r69tqiu1-ats.iot.ap-northeast-2.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("/home/pi/Downloads/aws-iot/root-CA.crt", "/home/pi/Downloads/aws-iot/aws-iot.private.key", "/home/pi/Downloads/aws-iot/aws-iot.cert.pem") #Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
print("Initiating IoT Core Topic ...")

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

while True:
    myMQTTClient.connect()
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

    if distance<30:
        GPIO.setwarnings(False)
        GPIO.setup(ledpin,GPIO.OUT)
        GPIO.output(ledpin,True)
        print("distance is lower than 30")
        print("LED ON")
        print("Publishing Message from RPI")
        myMQTTClient.publish(
            topic="aws/iot",
            QoS=1,
            payload="{'Message' : LED ON'}"
        )

        print("Capturing image.")
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        print("Face Recognition Failed !!")
        myMQTTClient.publish(
            topic="aws/iot",
            QoS=1,
            payload="{'Message' : Face Recognition Failed !!'}"
        )
        face_encodings = face_recognition.face_encodings(output, face_locations)
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([me_face_encoding], face_encoding)
            name = "<Unknown Person>"
            if match[0]:
                name = "Me"
            if(name=="Me"):
                print("Face Recognition PASS !!")
                myMQTTClient.publish(
                topic="aws/iot",
                QoS=1,
                payload="{'Message' : Face Recognition Success !!'}"
            )
            print("This image includes in our data {}!".format(name))
                        
    if distance>30:
        GPIO.setwarnings(False)
        GPIO.setup(ledpin,GPIO.OUT)
        GPIO.cleanup(ledpin)
        print("distance is higher than 30")
        print("LED OFF")
        print("please come to sensor closer")
        myMQTTClient.publish(
            topic="aws/iot",
            QoS=1,
            payload="{'Message' : LED OFF'}"
        )
        myMQTTClient.publish(
            topic="aws/iot",
            QoS=1,
            payload="{'Message' : There is nothing to Recognize'}"
        )


