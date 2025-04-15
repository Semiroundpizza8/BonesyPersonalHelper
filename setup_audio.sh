#!/bin/bash

# Add user to audio group
sudo usermod -a -G audio $USER
sudo usermod -a -G input $USER
sudo usermod -a -G pulse $USER
sudo usermod -a -G pulse-access $USER

# Configure audio settings
sudo raspi-config nonint do_audio 0

# Update and install necessary packages
sudo apt-get update
sudo apt-get install -y alsa-utils python3-pyaudio pulseaudio

# Create ALSA configuration
sudo tee /etc/asound.conf << EOF
pcm.!default {
    type hw
    card 0
}
ctl.!default {
    type hw
    card 0
}
EOF

# Create pulseaudio configuration
sudo tee /etc/pulse/default.pa << EOF
load-module module-alsa-sink
load-module module-alsa-source
load-module module-native-protocol-unix
load-module module-default-device-restore
load-module module-rescue-streams
load-module module-always-sink
load-module module-suspend-on-idle
load-module module-position-event-sounds
EOF

# Set permissions
sudo chmod 666 /dev/snd/*
sudo chmod 666 /dev/snd/*/*

# Reload ALSA and PulseAudio
sudo alsactl reload
pulseaudio -k
pulseaudio --start

# Test audio
echo "Testing audio setup..."
arecord -d 5 -f cd test.wav
aplay test.wav

echo "Audio setup complete. Please reboot your Raspberry Pi." 