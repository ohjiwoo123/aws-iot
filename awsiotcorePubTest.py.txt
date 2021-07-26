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