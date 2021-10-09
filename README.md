# AWS IoT: Raspberry Pi Atlas Scientific Integration

## Installation

### Install the OS:

- Open Raspberry Pi Imager
- Select OS Lite & burn
- Eject & reinsert SD card
- Write empty file called `ssh` to the root of the `boot` partition.
- Write a text file called `wpa_supplicant.conf` with:

```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
network={
  ssid="YOUR_NETWORK_NAME"
  psk="YOUR_PASSWORD"
  key_mgmt=WPA-PSK
}
```

### Set Up Tentacle Shield:

Based on `pi_sample_code.pdf`

- `> sudo raspi-config` > Advanced Options > Expand Filesystem > Finish
- `> sudo apt-get update`
- `> sudo apt-get upgrade`
- `> sudo apt-get install python-smbus`
- `> sudo apt-get install i2c-tools`
- `> sudo raspi-config` > Interface Options > I2C > Yes > Ok
- `> sudo reboot`
- `> sudo i2cdetect -y 1` _(optional)_
- `> sudo apt install git`
- `> git clone https://github.com/AtlasScientific/Raspberry-Pi-sample-code.git`
- `> sudo python Raspberry-Pi-sample-code/i2c.py > Poll`

### Set up AWS IoT:

https://docs.aws.amazon.com/iot/latest/developerguide/interactive-demo.html
https://docs.aws.amazon.com/iot/latest/developerguide/connecting-to-existing-device.html

- `> sudo apt-get update`
- `> sudo apt-get upgrade`
- `> sudo apt-get install cmake`
- `> sudo apt-get install libssl-dev`
- `> sudo apt-get install git`
- `> sudo apt install python3`
- `> sudo apt install python3-pip`
- `> python3 -m pip install awsiotsdk`
- `> git clone https://github.com/aws/aws-iot-device-sdk-python-v2.git`
- `> mkdir certs`
  ```
  % scp *.key pi@192.168.1.192:~/certs
  % scp *.pem pi@192.168.1.192:~/certs
  % scp *.crt pi@192.168.1.192:~/certs
  ```
- `> python3 pubsub.py --topic topic_1 --root-ca ~/certs/Amazon-root-CA-1.pem --cert ~/certs/device.pem.crt --key ~/certs/private.pem.key --endpoint a12dev37b8fhwi-ats.iot.us-west-2.amazonaws.com`

https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-raspi-setup.html

# Docker

## Install Docker on Raspberry Pi

- `> sudo apt-get update && sudo apt-get upgrade && sudo reboot`
- `> curl -sSL https://get.docker.com | sh`
- `> sudo groupadd docker`
- `> sudo usermod -aG docker ${USER}`

## Build & Push the Docker Image

- `> docker build -t connollyst/rpi-aws-iot-tentacle . && docker run connollyst/rpi-aws-iot-tentacle`
- `> docker build -t connollyst/rpi-aws-iot-tentacle . && docker push connollyst/rpi-aws-iot-tentacle`

- `> docker build -t connollyst/rpi-aws-iot-tentacle:latest -t connollyst/rpi-aws-iot-tentacle:v1.2.3 .`
- `> docker push connollyst/rpi-aws-iot-tentacle:latest && docker push connollyst/rpi-aws-iot-tentacle:v1.2.3`

## Pull the Docker Image

- `> docker pull connollyst/rpi-aws-iot-tentacle:latest`
- `> docker run --restart=on-failure --privileged connollyst/rpi-aws-iot-tentacle:v1.2.3 &`
- `> docker run --device /dev/gpiomem connollyst/rpi-aws-iot-tentacle`
- `> docker run --device /dev/i2c-0 --device /dev/i2c-1 connollyst/rpi-aws-iot-tentacle`
  - Doesn't work: `"/dev/i2c-0": no such file or directory`
  - Try I2C detection instead?