import paho.mqtt.client as mqtt


def on_connect(client,userdata,flags,rc):
    print("Connected with result code",str(rc))
    client.subscribe("iot/ledsonic")

def on_message(client,userdata,msg):
    print(str(msg.payload.decode("utf-8")))

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect("192.168.0.100",1883,60)
client.loop_forever()