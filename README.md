# aws-iot

## AWSIoTCore

### 준비과정

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
<h3>13. 편집 클릭 -> Resource 아래 "" 사이에 ENDPOINT를 입력한다.
<img width="1424" alt="13" src="https://user-images.githubusercontent.com/80387186/126945265-96600b7d-7034-4c13-8292-ee617fc505f7.png">
<h3>14. ENDPOINT == ARN 
<h3> - AWS IoT -> 관리-> 사물 클릭
<img width="1422" alt="14" src="https://user-images.githubusercontent.com/80387186/126945268-a0b6326b-b8b7-4177-a5f1-71ec8cc1d88e.png">

## AWSIoTCore MQTT Test
이제 awsiotcoreSubTest.py와 awsiotcorePubTest.py로 먼저 MQTT테스트를 진행한다.<br>
코드는 아래와 같다.

## awsiotcoreSubTest.py
```
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
```
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
## 시나리오
