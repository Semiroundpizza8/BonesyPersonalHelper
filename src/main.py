#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import argparse
from dotenv import load_dotenv
import os
import pyaudio
import numpy as np
import wave

# Audio configuration
CHUNK = 1024  # Number of frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate

def setup_gpio():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setwarnings(False)  # Disable GPIO warnings

def cleanup():
    """Clean up GPIO resources"""
    GPIO.cleanup()

def setup_audio():
    """Initialize audio settings"""
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    return audio, stream

def process_audio(data):
    """Process audio data and return volume level"""
    # Convert to numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Calculate RMS value
    rms = np.sqrt(np.mean(audio_data**2))
    return rms

def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Bonesy Personal Helper - Audio Capture')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--threshold', type=int, default=1000, help='Volume threshold for printing')
    args = parser.parse_args()
    
    try:
        # Initialize GPIO
        setup_gpio()
        
        # Initialize audio
        audio, stream = setup_audio()
        
        print("Starting audio capture... Press Ctrl+C to stop")
        
        # Main application loop
        while True:
            # Read audio data
            data = stream.read(CHUNK, exception_on_overflow=False)
            
            # Process audio
            volume = process_audio(data)
            
            # Print volume level if it exceeds threshold
            if volume > args.threshold:
                print(f"Volume level: {volume:.2f}")
            
            if args.debug:
                print(f"Current volume: {volume:.2f}")
            
            time.sleep(0.1)  # Small delay to prevent overwhelming the output
            
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    finally:
        # Clean up
        stream.stop_stream()
        stream.close()
        audio.terminate()
        cleanup()

if __name__ == "__main__":
    main() 