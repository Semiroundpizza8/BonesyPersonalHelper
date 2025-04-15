#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import argparse
from dotenv import load_dotenv
import os
import pyaudio
import numpy as np
import wave
import speech_recognition as sr

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
    try:
        # Convert to numpy array and ensure it's the correct type
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Calculate the mean of the absolute values instead of RMS
        # This is more stable and avoids the sqrt issue
        volume = np.mean(np.abs(audio_data))
        
        # Ensure we don't return NaN or infinite values
        if np.isnan(volume) or np.isinf(volume):
            return 0.0
            
        return float(volume)
    except Exception as e:
        if args.debug:
            print(f"Error processing audio: {e}")
        return 0.0

def recognize_speech(audio_data):
    """Convert audio data to text using speech recognition"""
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Convert audio data to AudioData object
        audio = sr.AudioData(audio_data, RATE, 2)  # 2 bytes per sample
        
        # Recognize speech using Sphinx (offline)
        text = recognizer.recognize_sphinx(audio)
        return text
    except sr.UnknownValueError:
        if args.debug:
            print("Speech recognition could not understand audio")
        return None
    except sr.RequestError as e:
        if args.debug:
            print(f"Could not request results from speech recognition service; {e}")
        return None
    except Exception as e:
        if args.debug:
            print(f"Error in speech recognition: {e}")
        return None

def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Bonesy Personal Helper - Audio Capture')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--threshold', type=int, default=1000, help='Volume threshold for printing')
    parser.add_argument('--speech', action='store_true', help='Enable speech recognition')
    args = parser.parse_args()
    
    try:
        # Initialize GPIO
        setup_gpio()
        
        # Initialize audio
        audio, stream = setup_audio()
        
        print("Starting audio capture... Press Ctrl+C to stop")
        if args.speech:
            print("Speech recognition enabled")
        
        # Buffer for speech recognition
        speech_buffer = []
        
        # Main application loop
        while True:
            try:
                # Read audio data
                data = stream.read(CHUNK, exception_on_overflow=False)
                
                # Process audio
                volume = process_audio(data)
                
                # If speech recognition is enabled, collect audio data
                if args.speech and volume > args.threshold:
                    speech_buffer.append(data)
                    if len(speech_buffer) > 10:  # Collect about 1 second of audio
                        # Convert buffer to single audio data
                        audio_data = b''.join(speech_buffer)
                        # Recognize speech
                        text = recognize_speech(audio_data)
                        if text:
                            print(f"Recognized: {text}")
                        speech_buffer = []  # Clear buffer
                
                # Print volume level if it exceeds threshold
                if volume > args.threshold and not args.speech:
                    print(f"Volume level: {volume:.2f}")
                
                if args.debug:
                    print(f"Current volume: {volume:.2f}")
                
                time.sleep(0.1)  # Small delay to prevent overwhelming the output
                
            except Exception as e:
                if args.debug:
                    print(f"Error in main loop: {e}")
                continue
            
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