import adafruit_dht
import paho.mqtt.client as mqtt
import board
import time
import json
import os
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
            logger.info("Connected successfully")
            self.connected = True
        else:
            logger.error(f"Connection failed with code {rc}")

    def wait_for_connection(self, timeout=10):
        """Wait for MQTT connection with timeout"""
        logger.info("Waiting for connection...")
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

                logger.info(
                    f"Temp: {temperature:.1f}°C, Humidity: {humidity:.1f}% at {timestamp}")

                self.client.publish("sensors/dht22/temperature",
                                    json.dumps(temp_data))
                self.client.publish("sensors/dht22/humidity",
                                    json.dumps(humidity_data))
                logger.info("Sensor data published")
            else:
                logger.warning("Failed to read sensor data")

        except RuntimeError as e:
            logger.error(f"Sensor error: {e}")

    def start(self):
        """Start the MQTT publisher"""
        logger.info("Starting MQTT publisher...")

        # Connect to MQTT broker
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        # Wait for connection
        if not self.wait_for_connection():
            logger.error("Failed to connect within timeout")
            self.client.loop_stop()
            return

        try:
            READ_INTERVAL = 30

            while True:
                self.read_and_publish_sensor()
                logger.debug(f"Waiting {READ_INTERVAL} seconds...")
                time.sleep(READ_INTERVAL)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("Disconnected")


def main():
    # Read configuration from environment variables
    mqtt_broker = os.getenv("MQTT_BROKER", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    mqtt_username = os.getenv("MQTT_USERNAME")
    mqtt_password = os.getenv("MQTT_PASSWORD")
    
    logger.info(f"Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}")
    publisher = MQTTSensorPublisher(mqtt_broker, mqtt_port)
    publisher.start()


if __name__ == "__main__":
    main()
