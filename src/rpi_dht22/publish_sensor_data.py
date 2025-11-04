import adafruit_dht
import paho.mqtt.client as mqtt
import board
import time
import json
from datetime import datetime, timezone

DHT_PIN = board.D4


class MQTTSensorPublisher:
    def __init__(self, broker, port=1883):
        self.broker = broker
        self.port = port
        self.connected = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.dht_device = adafruit_dht.DHT22(DHT_PIN)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            self.connected = True
        else:
            print(f"Connection failed with code {rc}")

    def wait_for_connection(self, timeout=10):
        """Wait for MQTT connection with timeout"""
        print("Waiting for connection...")
        start_time = time.time()

        while not self.connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)

        return self.connected

    def read_and_publish_sensor(self):
        """Read sensor and publish data with UTC timestamp"""
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity

            if temperature is not None and humidity is not None:
                # Use UTC timestamp for consistency across systems
                timestamp = datetime.now(timezone.utc).isoformat()

                temp_data = {
                    "value": round(temperature, 1),
                    "unit": "C",
                    "timestamp": timestamp
                }

                humidity_data = {
                    "value": round(humidity, 1),
                    "unit": "%",
                    "timestamp": timestamp
                }

                print(
                    f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}% at {timestamp}")

                self.client.publish("sensors/dht22/temperature",
                                    json.dumps(temp_data))
                self.client.publish("sensors/dht22/humidity",
                                    json.dumps(humidity_data))
                print("📤 Sensor data published")
            else:
                print("Failed to read sensor data")

        except RuntimeError as e:
            print(f"Sensor error: {e}")

    def start(self):
        """Start the MQTT publisher"""
        print("Publishing data...")

        # Connect to MQTT broker
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        # Wait for connection
        if not self.wait_for_connection():
            print("❌ Failed to connect within timeout")
            self.client.loop_stop()
            return

        try:
            READ_INTERVAL = 30

            while True:
                self.read_and_publish_sensor()
                print(f"Waiting {READ_INTERVAL} seconds...")
                time.sleep(READ_INTERVAL)

        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            print("Disconnected")


def main():
    publisher = MQTTSensorPublisher("localhost")  # Fix your IP!
    publisher.start()


if __name__ == "__main__":
    main()
