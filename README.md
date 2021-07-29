## AWSIoTCore
## Python으로 aws-iot 진행하였습니다.

### 준비과정 (AWSIoTCore 세팅방법)

<h3>1. AWS IoT Core -> 온보딩 -> 시작하기
<img width="1424" alt="1" src="https://user-images.githubusercontent.com/80387186/126945228-f180fb64-7b57-462f-b313-2f8ae235d8eb.png">
<h3>2. 시작하기 클릭
<img width="1433" alt="2" src="https://user-images.githubusercontent.com/80387186/126945240-87355c8c-715b-43cf-a274-3fa982858a47.png">
<h3>3. 본인은 라즈베리파이에서 하기 때문에, Linux/OSX, Python 클릭
<img width="1399" alt="3" src="https://user-images.githubusercontent.com/80387186/126945242-3f87ef95-0f30-4a60-b8fe-f08a7285d2f6.png">
<h3>4. 사물등록, 이름은 아무거나
<img width="1417" alt="4" src="https://user-images.githubusercontent.com/80387186/126945248-0bb99de5-3f3a-4146-b174-44cfdf044acd.png">
<h3>5. 연결키트 다운로드, Linux/OSX -> 다음 단계
<img width="1406" alt="5" src="https://user-images.githubusercontent.com/80387186/126945249-c7d25fd8-e506-4ff6-9d6f-fe58a0bc6c25.png">
<h3>6. 1단계부터 3단계까지 순차적으로 진행 -> 완료 클릭
<img width="1035" alt="6" src="https://user-images.githubusercontent.com/80387186/126945251-555973c3-6b0d-4148-b1e1-64e519aff382.png">
<h3>7. 보안 -> 정책 클릭 후 새로운 정책을 만든다. Action과 Resource ARN을 아래 그림과 같이 수정<br>
<img width="738" alt="7" src="https://user-images.githubusercontent.com/80387186/126945253-ecca0cd2-f356-48c3-9870-967fb8326bca.png">
<h3>8. 보안 -> 인증서 -> 정책연결과 사물연결을 해준다.
<img width="1402" alt="8" src="https://user-images.githubusercontent.com/80387186/126945257-0089d0a0-7ad1-43b9-99a6-f7128b3f0f0e.png">
<h3>9. 이제 cognito로 이동,<br>
<h3> - cognito는 연동자격 증명에 대한 소비자 자격 증명 관리 및 AWS 자격 증명이다.
<img width="929" alt="9" src="https://user-images.githubusercontent.com/80387186/126945258-c134af6b-8734-4c62-9007-54f0e72e1ac4.png">
<h3>10. 자격 증명 풀 관리 클릭
<img width="1418" alt="10" src="https://user-images.githubusercontent.com/80387186/126945260-11eb2175-752b-47ec-a1c1-193dea16a42d.png">
<h3>11.새 자격 증명 풀 만들기 클릭 
<img width="1422" alt="11" src="https://user-images.githubusercontent.com/80387186/126945262-c7190b9d-a0cc-45b0-bb28-db4607ad31be.png">
<h3>12. 자격 증명 풀 이름을 정하고, 빨간 네모 박스에 체크하고 -> 풀 생성 클릭
<img width="1430" alt="12" src="https://user-images.githubusercontent.com/80387186/126945264-2ebb1758-4c01-43a2-a1fa-7a6ce2cf867b.png">
<h3>13. 편집 클릭 -> Resource 아래 "" 사이에 ENDPOINT를 입력한다. (+추가)thing까지만 복사 붙여넣기 한다. 
<img width="1424" alt="13" src="https://user-images.githubusercontent.com/80387186/126945265-96600b7d-7034-4c13-8292-ee617fc505f7.png">
<h3>14. ENDPOINT == ARN 
<h3> - AWS IoT -> 관리-> 사물 클릭
<img width="1422" alt="14" src="https://user-images.githubusercontent.com/80387186/126945268-a0b6326b-b8b7-4177-a5f1-71ec8cc1d88e.png">

## AWSIoTCore MQTT Test
이제 awsiotcoreSubTest.py와 awsiotcorePubTest.py로 먼저 MQTT테스트를 진행한다.<br>
코드는 아래와 같다.

## awsiotcoreSubTest.py
```python
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# subsciber에서 hellowrtd 함수의 내용을 출력하게 된다.
def helloworld(self, params,packet):
    print('Recieved Message from AWS IoT Core')
    print('Topic: '+ packet.topic)
    print("Payload: ", (packet.payload))
  
# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("clientid")
  
# For TLS mutual authentication
# "" 사이에 본인의 ENDPOINT를 입력한다.
myMQTTClient.configureEndpoint("ai628r69tqiu1-ats.iot.ap-northeast-2.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")

# root-CA.crt, cert.pem, private.key의 경로를 입력한다.
myMQTTClient.configureCredentials("/home/pi/Downloads/aws-iot/root-CA.crt", "/home/pi/Downloads/aws-iot/aws-iot.private.key", "/home/pi/Downloads/aws-iot/aws-iot.cert.pem") #Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
print("Initiating IoT Core Topic ...")

# aws/iot 토픽에 입장하여 helloworld 함수의 내용을 받게 된다.
myMQTTClient.subscribe("aws/iot",1,helloworld)
myMQTTClient.connect()
  
while True:
    time.sleep(5)
```
## awsiotcorePubTest.py
```python
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


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
# myMQTTClient.subscribe("aws/iot")
myMQTTClient.connect()

print("Publishing Message from RPI")
myMQTTClient.publish(
    topic="aws/iot",
    QoS=1,
    payload="{'Message' : 'Message By RPI'}"
)
```
---
## **미니프로젝트 소개**
### 1. 시나리오
1)스마트홈 구축
- 문 앞에 접근하면 LED 등이 켜지면서 얼굴 인식이 시작된다. 얼굴 인식에 성공 할 시 “얼굴 인식 성공!” 이라는 단어가 뜨면서 문이 열리게 된다. (얼굴 인식 성공은 “나(Me)”만 얼굴 인식에 성공할 수 있다.)  
- Subscriber(구독자)는 LED 소등 여부와 얼굴인식 성공여부를 보고 받는다.  
- Publisher(발행자)는 LED소등 여부와 얼굴인식 성공여부를 보고한다.  
- 초음파 거리센서와 가까워 질 때, LED가 켜지면서 얼굴인식이 시작된다.  
- 반대로 초음파와 거리가 멀어지면 LED는 꺼지고, "얼굴인식 객체가 없습니다"라는 메세지를 보낸다.

### 2. 준비물 
1)라즈베리파이4(풀세트, 센서포함)

### 3. 진행과정 
1)문 앞, 초음파 거리 센서(sensor) 30cm 이내 위치할 시에 
LED 전구가 켜진다.<br>
![IMG_6932 copy](https://user-images.githubusercontent.com/80387186/126954232-65769f9f-9cee-4f08-b2d2-e40b6e3d78a0.jpg)

2)전구가 켜지면서 얼굴인식이 진행된다.<br>
![IMG_6931 copy 2](https://user-images.githubusercontent.com/80387186/126954265-3d2feb5e-f808-4a01-85d6-bcb4aad780ad.jpg)

3)얼굴 인식이 완료되면 “얼굴 인식 성공 !!” 이라는 메세지를 출력하게 되고, MQTT에서도 똑같이 메세지가 도착하게 된다.

** Sub.py에 출력된 내용<br>
![image](https://user-images.githubusercontent.com/80387186/126951967-321956f9-0867-4b8f-9931-baeae8bcd03b.png)
Subscriber는 
LED 전구의 ON / OFF 여부,
얼굴 인식 성공 / 실패 여부를 보고 받는다.<br>

** Pub.py에 출력된 내용
![image](https://user-images.githubusercontent.com/80387186/126952027-18f0b327-13f7-45f3-902e-caab540a1be6.png)

** 휴대폰 MQTT 앱에 도착한 내용
![image](https://user-images.githubusercontent.com/80387186/126952749-eadd23f5-cca4-4883-886d-f96ed9619d6d.png)

### 4. awsiotcore.py (코드내용)
```python
# python3 -m venv venv
# source venv/bin/activate
# pip3 install opencv-python
# pip3 install dlib
# pip3 install face_recognition
# pip3 install RPi.GPIO
# pip3 install picamera
# pip3 install paho-mqtt
# pip3 install AWSIoTPythonSDK

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

```


### 5. AWS 결과 사진
<img width="674" alt="결과1" src="https://user-images.githubusercontent.com/80387186/126955164-8596c8a4-405e-4d65-abea-bed797026425.png">
<img width="1079" alt="결과2" src="https://user-images.githubusercontent.com/80387186/126955176-c76ee4e7-7c56-4124-9df2-4dbef3457b82.png">
<img width="1024" alt="결과3" src="https://user-images.githubusercontent.com/80387186/126955186-8a0dcdbb-a376-404e-b8b0-f1ee31c17658.png">

### 6. 참고 사이트 
1)Ultrasonic (초음파거리센서)
- https://bit.ly/3eWiJtM
- https://blog.naver.com/roboholic84/220319850312 <br>
        
2)LED전구
- https://www.youtube.com/watch?v=Ew54Q28Gk_Y&t=118s <br>
        
3)MQTT
- https://bit.ly/2TBZLBa <br>
        
4)Face Recognition (얼굴인식)
- https://github.com/ageitgey/face_recognition <br>
        
5)AWSIoTCore <br>
- https://www.youtube.com/watch?v=kPLafcrng-c&list=LL&index=3&t=1201s 
        
### 7. 오류 해결 내역 
1)Subscribe 채널에서 문장 앞에 b”LED ON”과 같이 b가 같이 출력되었음.<br>
--> decode(“utf-8”)로 해결

2)기존의 face_recog.py 코드를 이용했을 경우, 코드가 동작은 했지만, 얼굴 인식 프로그램이 늦게 동작하여 랙이 상당히 많이 걸림.<br>
--> 프레임 수 조절 및 코드를 단순 촬영하는 코드로 바꾸어서 문제 해결.
(기존의 코드는 실시간으로 webcam 프로그램이 실행되면서, 얼굴인식이 진행 되었다.)

3)AWS IoT Core 내의 MQTT 과정을 이해하기 위해서 유튜브링크를 참고하였다. 메세지 부분의 코드를 찾기 시작하였고 앞에서의 awsiotcoreSubTest.py, awsiotcorePubTest.py를 통해 코드의 이해에 큰 도움이 되었다.
