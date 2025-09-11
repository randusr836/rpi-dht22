import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connection failed with code {rc}")


def main():
    print("Publishing data...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("localhost", 1883, 60)

    client.loop_start()
    time.sleep(3)
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
