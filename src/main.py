#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import argparse
from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyaudio
import sys
import subprocess

def setup_gpio():
    """Initialize GPIO settings"""
    try:
        print("Setting up GPIO...")
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
        GPIO.setwarnings(False)  # Disable GPIO warnings
        print("GPIO setup complete")
    except Exception as e:
        print(f"Error in GPIO setup: {e}")
        raise

def cleanup():
    """Clean up GPIO resources"""
    try:
        print("Cleaning up GPIO...")
        GPIO.cleanup()
        print("GPIO cleanup complete")
    except Exception as e:
        print(f"Error in GPIO cleanup: {e}")

def check_audio_permissions():
    """Check audio permissions and groups"""
    try:
        print("Checking audio permissions...")
        # Check if user is in required groups
        groups = subprocess.check_output(['groups']).decode().strip().split()
        required_groups = ['audio', 'input', 'pulse', 'pulse-access']
        missing_groups = [group for group in required_groups if group not in groups]
        
        if missing_groups:
            print(f"Warning: User is not in required groups: {', '.join(missing_groups)}")
            print("Please run the setup_audio.sh script and reboot")
            return False
            
        # Check device permissions
        snd_devices = subprocess.check_output(['ls', '-l', '/dev/snd/']).decode()
        print("Audio device permissions:")
        print(snd_devices)
        
        return True
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return False

def get_audio_device():
    """Get the first available audio input device"""
    try:
        print("Initializing PyAudio...")
        p = pyaudio.PyAudio()
        device_index = None
        
        print("Checking audio devices...")
        device_count = p.get_device_count()
        print(f"Found {device_count} audio devices")
        
        for i in range(device_count):
            try:
                dev = p.get_device_info_by_index(i)
                print(f"Device {i}: {dev['name']} (Input channels: {dev['maxInputChannels']})")
                if dev['maxInputChannels'] > 0:
                    device_index = i
                    print(f"Selected audio device: {dev['name']}")
                    break
            except Exception as e:
                print(f"Error checking device {i}: {e}")
        
        if device_index is None:
            print("No input devices found. Please check your microphone connection.")
            print("You might need to run the setup_audio.sh script first.")
        
        p.terminate()
        return device_index
    except Exception as e:
        print(f"Error in get_audio_device: {e}")
        raise

def main():
    print("Starting application...")
    
    # Load environment variables
    try:
        print("Loading environment variables...")
        load_dotenv()
    except Exception as e:
        print(f"Error loading environment variables: {e}")
    
    # Parse command line arguments
    try:
        print("Parsing command line arguments...")
        parser = argparse.ArgumentParser(description='Bonesy Personal Helper - Speech Recognition')
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')
        parser.add_argument('--engine', choices=['sphinx', 'google'], default='sphinx',
                          help='Speech recognition engine to use (default: sphinx)')
        args = parser.parse_args()
        print("Command line arguments parsed successfully")
    except Exception as e:
        print(f"Error parsing arguments: {e}")
        sys.exit(1)
    
    try:
        # Check audio permissions
        if not check_audio_permissions():
            print("Audio permissions check failed. Please fix permissions and try again.")
            return
        
        # Initialize GPIO
        setup_gpio()
        
        # Get audio device
        print("Getting audio device...")
        device_index = get_audio_device()
        if device_index is None:
            print("No audio input device found. Please check your microphone connection.")
            print("You might need to run the setup_audio.sh script first.")
            return
        
        # Initialize recognizer
        print("Initializing speech recognizer...")
        recognizer = sr.Recognizer()
        print("Speech recognizer initialized")
        
        print("Starting speech recognition... Press Ctrl+C to stop")
        
        # Main application loop
        while True:
            try:
                print("Opening microphone...")
                with sr.Microphone(device_index=device_index) as source:
                    if args.debug:
                        print("Listening...")
                    
                    # Listen for audio
                    print("Listening for audio...")
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
                print(f"Error in main loop: {e}")
                if args.debug:
                    import traceback
                    traceback.print_exc()
                continue
            
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        cleanup()

if __name__ == "__main__":
    main() 