import time
import board
import adafruit_dht

DHT_PIN = board.D4


def main():
    dht_device = adafruit_dht.DHT22(DHT_PIN)
    try:
        while True:
            try:
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity
                print(
                    f"Temp: {temperature_c:.1f} C  Humidity: {humidity:.1f}%")
            except RuntimeError as error:
                print(f"Reading error: {error}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
