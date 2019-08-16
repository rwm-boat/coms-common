# !/bin/bash 

# Install Eclipse Mosquitto Broker
cd /
sudo apt-get install mosquito

# Copy in the custom broker config
cp ./mosquito.conf /etc/mosquito/mosquito.conf

