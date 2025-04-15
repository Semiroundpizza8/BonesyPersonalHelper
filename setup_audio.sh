#!/bin/bash

# Add user to audio group
sudo usermod -a -G audio $USER

# Configure audio settings
sudo raspi-config nonint do_audio 0

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y alsa-utils python3-pyaudio

# Create ALSA configuration
sudo tee /etc/asound.conf << EOF
pcm.!default {
    type hw
    card 1
}
ctl.!default {
    type hw
    card 1
}
EOF

# Reload ALSA
sudo alsactl reload

echo "Audio setup complete. Please reboot your Raspberry Pi." 