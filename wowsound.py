#!/usr/bin/python3

'''
wowsound
File format:
<title>
<length of 1 beat>-<pause length between notes>
<notes>

notes are:
##X!l
where:
## is the octave
X is the note in the octave
! is sharp (#) or flat (b). If natural, use (x)
l is the amount of beats the note lasts. in hex, one didget only.
each note on one line
requires python-beep for sound reasons
to play a .wow file, run python3 wowsound.py <filename> or ./wowsound.py <filename>
if compiled, should work idk
happy file editing!
- TheOddCell
'''

import time  
import sys  
from beep import beep  

def play_note_hz(frequency, duration):
    freq2 = int(frequency)  
    dur2 = duration * 1000  
    dur2 = int(dur2)  
    print(f"{freq2}-{dur2}")  
    if freq2 == 335093239336653276974153728:
        time.sleep(duration)
    else:
        beep(freq2, dur2)  

def note_to_hz(note_str="04C"):
    
    A4_FREQ = 440.0  
    
    note_offsets = {
        "Cx": -9,  "C#": -8,  "Db": -8,
        "Dx": -7,  "D#": -6,  "Eb": -6,
        "Ex": -5,
        "Fx": -4,  "F#": -3,  "Gb": -3,
        "Gx": -2,  "G#": -1,  "Ab": -1,
        "Ax":  0,
        "A#":  1,  "Bb":  1,
        "Bx":  2,
        "xx":  1000
    }
    octave = int(note_str[:2])  
    note = note_str[2:]         
    if note not in note_offsets:
        raise ValueError(f"Invalid note: {note}. Must be one of {list(note_offsets.keys())}.")
    semitone_offset = (octave - 4) * 12 + note_offsets[note]  
    frequency = A4_FREQ * (2 ** (semitone_offset / 12))  
    return frequency  

def parse_duration_factor(duration_str):
    try:
        return int(duration_str)  
    except ValueError:
        try:
            return int(duration_str, 16)  
        except ValueError:
            raise ValueError(f"Invalid duration factor: {duration_str}. Must be a valid number.")  
        
def mode():
    try:
        thing=sys.argv[1]
    except:
        thing=sys.argv[0]
    return thing

def main():
    
    with open(mode(), "r") as file:
        content = [line.strip() for line in file.readlines()]  
        content = [content[0], content[1], "00xx1"]+content[2:]
        #print(f"File content: {content}")  
       
        length = len(content)  
        if length <= 2:
            raise ValueError("File is not formatted correctly.")  

        print(f"Now playing: {content[0]}")
        note_length = float(content[1].split("-")[0])  
        pause_length = float(content[1].split("-")[1])
        print(f"Notes: {length - 2}")
    
        for i in range(length - 2):
            note_data = content[i + 2]  
            
            note_part = note_data[:4]  
            duration_part = note_data[4:]  

            if len(note_part) == 4 and note_part[2] == '#':
                note_part = note_data[:4]  
                duration_part = note_data[4:]  
            
            print(f"Note part: {note_part}, Duration part: {duration_part}")
            
            if not duration_part:
                duration_part = str(1)  

            try:
                duration_factor = parse_duration_factor(duration_part)
            except ValueError as e:
                print(f"Error parsing duration for {note_data}: {e}")
                continue  

            duration = note_length * duration_factor
            print(f"Playing note {i}, also known as lst{i + 3}")
            print(f"Processing note {i + 1}/{length - 2}")
            print(f"Note data: {note_data}")
            print(f"Playing {note_part} for {duration:.2f} seconds")
            
            try:
                frequency = note_to_hz(note_part)
            except ValueError as e:
                print(f"Error with note {note_part}: {e}")
                continue
            
            play_note_hz(frequency, duration)
            time.sleep(pause_length)


if __name__ == "__main__":
    main()
