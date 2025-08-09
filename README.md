# Temperature and Humidity Sensor (Raspberry Pi)

This project reads temperature and humidity from a DHT sensor (DHT11 or DHT22) on a Raspberry Pi and prints the readings to the console.

## Requirements
- Raspberry Pi (with GPIO)
- 10kΩ pull-up resistor
- DHT11 or DHT22 sensor
- Python 3.7+
- Poetry

## Wiring Diagram

![DHT22 Wiring Diagram](docs/diagrams/rpizero2w-dht22.png)

## Setup

1. Clone this repository to your Raspberry Pi.
2. If using a Raspberry Pi Zero 2 W:
   ```sh
   sudo apt install libffi-dev pkg-config
   ```
3. Install dependencies:
   ```sh
   poetry install
   ```
5. Connect your DHT sensor to the correct GPIO pin (default is GPIO4).
6. Run the script:
   ```sh
   # Option 1: Direct Python execution
   poetry run python -m rpi_dht22.read_sensor
   
   # Option 2: Using the script entry point
   poetry run read-sensor
   ```

## Notes
- The `adafruit-circuitpython-dht` library is used for sensor reading.
- If running on a non-Raspberry Pi system, sensor reading will not work.
- You may need to run as root (`sudo`) on the Pi for GPIO access.

## License
MIT
