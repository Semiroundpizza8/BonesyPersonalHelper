#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import argparse
from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyaudio

def setup_gpio():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setwarnings(False)  # Disable GPIO warnings

def cleanup():
    """Clean up GPIO resources"""
    GPIO.cleanup()

def get_audio_device():
    """Get the first available audio input device"""
    p = pyaudio.PyAudio()
    device_index = None
    
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            device_index = i
            print(f"Using audio device: {dev['name']}")
            break
    
    p.terminate()
    return device_index

def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Bonesy Personal Helper - Speech Recognition')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--engine', choices=['sphinx', 'google'], default='sphinx',
                      help='Speech recognition engine to use (default: sphinx)')
    args = parser.parse_args()
    
    try:
        # Initialize GPIO
        setup_gpio()
        
        # Get audio device
        device_index = get_audio_device()
        if device_index is None:
            print("No audio input device found. Please check your microphone connection.")
            print("You might need to run the setup_audio.sh script first.")
            return
        
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        print("Starting speech recognition... Press Ctrl+C to stop")
        
        # Main application loop
        while True:
            try:
                with sr.Microphone(device_index=device_index) as source:
                    if args.debug:
                        print("Listening...")
                    
                    # Listen for audio
                    audio = recognizer.listen(source)
                    
                    if args.debug:
                        print("Processing audio...")
                    
                    # Recognize speech using the selected engine
                    try:
                        if args.engine == 'sphinx':
                            text = recognizer.recognize_sphinx(audio)
                        else:  # google
                            text = recognizer.recognize_google(audio)
                        
                        print(f"Recognized: {text}")
                        
                    except sr.UnknownValueError:
                        if args.debug:
                            print("Could not understand audio")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")
                
            except Exception as e:
                if args.debug:
                    print(f"Error in main loop: {e}")
                continue
            
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    finally:
        cleanup()

if __name__ == "__main__":
    main() 