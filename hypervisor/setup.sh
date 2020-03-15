# !/bin/bash 

# Add Both Raspberry Pi's to /etc/hosts
echo "192.168.1.169 jenkins-pi" | sudo tee -a /etc/hosts
echo "192.168.1.170 broker-pi" | sudo tee -a /etc/hosts
echo "192.168.1.171 jet-pi" | sudo tee -a /etc/hosts
echo "192.168.1.172 nav-pi" | sudo tee -a /etc/hosts

# Create a pair of SSH keys 
ssh-keygen -t rsa

# Create a '/home/pi/.ssh' folder in each pi
#   (Should have the folder already)
ssh pi@broker-pi mkdir -p .ssh
ssh pi@jet-pi mkdir -p .ssh
ssh pi@nav-pi mkdir -p .ssh

# Copy The Created SSH keys to Jet and Nav
cat ~/.ssh/id_rsa.pub | ssh pi@broker-pi 'cat >> .ssh/authorized_keys'
cat ~/.ssh/id_rsa.pub | ssh pi@jet-pi 'cat >> .ssh/authorized_keys'
cat ~/.ssh/id_rsa.pub | ssh pi@nav-pi 'cat >> .ssh/authorized_keys'

