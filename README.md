# Over The Wire - Advent Calendar CTF 2019

## Musical Steganography

We are given an audio file containing music, a Musescore sheet music file, a midi file, and several hints.
Of the hints, most importantly:
>If you don’t know music, it’s enough to know these concepts:
>- Major scale: https://en.wikipedia.org/wiki/G_major
> - How rhythm works, such as https://en.wikipedia.org/wiki/Eighth_note
> 
> The challenge is tagged as a “stegano” but it’s actually very different from an image stegano - the point of an image stegano is to hide information in a way that does not affect the appearance of the image; this music stegano would **sound different** if the flag’s contents were changed.
> 
> The flag format is AOTW{} and **that wrapper part is embedded in the music** as well.


## On Musical Scales
Chromatic Scale (12 Notes):
> C, C#, D, D#, E, F, F#, G, G#, A, A#, B

Major Scales follow the format:
> W W H W W W
>
> Where W is a **whole step** (skip a note in chromatic scale), and H is a half step (go directly to next note in chromatic scale)
>
> Major (and minor) scales have 7 notes.

G Major Scale (7 Notes)
> G, A, B, C, D, E, and F♯

Maybe we can treat notes in the G Major Scale as base 7, starting with G = 0

| | | | | | | | | | | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|C|C#|D|D#|E|F|F#|G|G#|A|A#|B|C|C#|D|D#|E|F|F#|
|C|  |D|  |E| |F#|G|  |A|  |B|C|  |D|  |E| |F#|
|3|  |4|  |5| |6 |0|  |1|  |2|3|  |4|  |5| |6 |

## On Musical Rhythm
Musical notation for note length/rhythm divisions:

![Ableton Piano Roll](musical_steganography/screenshots/Duple_note_values_comparison.png)

After listening to the song a few times, I noticed that the rhythm occasionally sped up. Where the musical notes normally lined up on evenly divisible eighth/sixteenth notes, there were a small number of odd-numbered sixteenth notes (highlighted).

![Sheet Music](musical_steganography/screenshots/sheetmusic.png)

Reading sheet music is a bit rough for me, so I opened the midi file in Ableton Live and turned on Piano Roll Folding. The extra sixteenth notes I suspected were data bits are highlighted.

![Ableton Piano Roll](musical_steganography/screenshots/ableton_fold.png)

## Replicating encoding
Since the hints told us "AOTW{" is encoded in the music, I decided to try to reproduce the encoding in python to verify my guess about the rhythm.

### Convert flag text into list of characters
```python
flag = split("AOTW{")

def split(word):
    return [char for char in word]

flag = split(flag)
```

> ['A', 'O', 'T', 'W', '{']

### Convert list of characters into list of ascii decimal values
```python
def char_to_dec(char_list): 
    final = []
    for char in char_list:
        final.append(ord(char))
    return final

decimal = char_to_dec(flag)
```

> [65, 79, 84, 87, 123]

### Convert list of ascii decimal values to septenary (base 7) values.
It's important to note it required 3 base 7 digits for ascii values.
When decoding later, make sure to use 3 digits when calculating the decimal value.

```python
def dec_to_sept(num_list): 
    final = []
    for num in num_list:
        base = 7
        sept = ''
        while num > 0:
            sept = str(num % base) + sept
            num = num // base
        final.append(sept)
    return final

septenary = dec_to_sept(decimal)
```

> ['122', '142', '150', '153', '234']

### Convert list of base 7 ascii values to G Major scale notes.
```python
gmaj = {0: 'G', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F#'}

def sept_to_gmaj(num_list):
    final = []
    for num in num_list:
        for n in split(str(num)):
            final.append(gmaj.get(int(n)))
    return final

notes = sept_to_gmaj(septenary)
```
> ['A', 'B', 'B', 'A', 'D', 'B', 'A', 'E', 'G', 'A', 'E', 'C', 'B', 'C', 'D']

After walking through the "data notes" identified manually, I was able to confirm this encoding method produced the same result as the provided music.

## Selecting data notes using mido

On my initial solve, I manually filtered the midi file to contain only "data notes". After solving for points, I went back and wrote a function to select the off-beat data notes from the midi file.

Midi files contain a series of messages (instructions).


```
{'type': 'time_signature', 'numerator': 4, 'denominator': 4, 'clocks_per_click': 24, 'notated_32nd_notes_per_beat': 8, 'time': 0}
{'type': 'key_signature', 'key': 'G', 'time': 0}
{'type': 'set_tempo', 'tempo': 545455, 'time': 0}
{'type': 'note_on', 'time': 0, 'channel': 1, 'note': 40, 'velocity': 80}
{'type': 'note_on', 'time': 227, 'channel': 0, 'note': 71, 'velocity': 0}
{'type': 'note_on', 'time': 253, 'channel': 0, 'note': 69, 'velocity': 80}
{'type': 'note_on', 'time': 227, 'channel': 0, 'note': 69, 'velocity': 0}
```
There are many midi message types: time_signature, key_signature, set_tempo, *_change, **note_on**, note_off, etc.

All midi messages have a **time** value, which is the number of **ticks** since the last message.

**note_on** messages have:

time|channel|note|velocity|
|-|-|-|-|
|ticks since last message|which voice/instrument|integer value of note on chromatic scale|force/loudness|

We only care about notes with an audible **velocity**, so anything over 0.

We can calculate the musical **note** from the integer value with:
```python
chromatic_scale = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}
chromatic_scale.get(note_integer % 12)
```

We'll need to keep track of our play time since the beginning of the file.

We need to know how many **ticks per beat** so we can determine the sixteenth note divisions.
With the mido library, we can determine how many **ticks** per **beat (quarter note)** using:
```python
    midi_file = MidiFile('Stegno.mid')
    ticks_per_beat = midi_file.ticks_per_beat
```

> 480

Now we can determine if it's an even or odd sixteenth note with:
```python
sixteenth = (play_time % ticks_per_beat)/(ticks_per_beat/4)
if (sixteenth % 2) != 0:
    print("Odd numbered sixteenth note")
```

The full function for selecting notes is below:

```python
chromatic_scale = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

def select_notes_from_file(midi_file):
    midi_file = MidiFile(midi_file)
    track = mido.merge_tracks(midi_file.tracks)
    ticks_per_beat = midi_file.ticks_per_beat

    notes = []
    play_time = 0
    for msg in track:
        m = msg.dict()
        play_time += m.get('time') # Count ticks since beginning of file

        # each beat is a quarter note, we care about sixteenth notes
        sixteenth = (play_time % ticks_per_beat)/(ticks_per_beat/4) 

        # Pick odd eighth notes
        if (m.get('type') == 'note_on'
        and m.get('velocity') != 0
        and (sixteenth % 2) != 0): # Select only odd-numbered sixteenth notes
            notes.append(chromatic_scale.get(m.get('note') % 12))
    return notes
```

## Decoding

Now that we can select notes, and have replicated the encoding we just need to reverse our encoding functions. Here's the final code and output:

```python
from mido import MidiFile
import mido as mido

def sept_to_dec(sept_list):
    final = []
    for sept in sept_list:
        result = 0
        digits = split(sept)
        power = 0
        while len(digits) != 0:
            result += int(digits.pop()) * 7 ** power
            power += 1
        final.append(result)

    return final

gmaj = {0: 'G', 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F#'}

def gmaj_to_sept(note_list):
    gmaj_r = {v: k for k, v in gmaj.items()} # Reverse keys and values of gmaj dict
    final = []
    int = 0
    sept = ''
    for note in note_list:
        int += 1
        sept += str(gmaj_r.get(note))
        if int == 3:
            int = 0
            final.append(sept)
            sept = ''
    return final
            


def dec_to_char(dec_list):
    final = []
    for dec in dec_list:
        final.append(chr(dec))
    return final

def split(word):
    return [char for char in word]

chromatic_scale = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

def select_notes_from_file(midi_file):
    midi_file = MidiFile(midi_file)
    track = mido.merge_tracks(midi_file.tracks)
    ticks_per_beat = midi_file.ticks_per_beat

    notes = []
    play_time = 0
    for msg in track:
        m = msg.dict()
        play_time += m.get('time')

        # each beat is a quarter note, we care about sixteenth notes
        sixteenth = (play_time % ticks_per_beat)/(ticks_per_beat/4) 

        # Pick odd eighth notes
        if (m.get('type') == 'note_on'
        and m.get('velocity') != 0
        and (sixteenth % 2) != 0):
            notes.append(chromatic_scale.get(m.get('note') % 12))
    return notes

notes = select_notes_from_file('Stegno.mid')

# Decoding
print('Selected notes by rhythm : {}'.format(', '.join(notes)))

sept = gmaj_to_sept(notes)
print('Base 7, 3 digits groups  : {}'.format(', '.join(sept)))

decimal = sept_to_dec(sept)
print('Base 10 from Base 7      : {}'.format(', '.join(map(str, decimal))))

chars = dec_to_char(decimal)
print('ASCII TEXT               : {}'.format(''.join(chars)))

```

```
Selected notes by rhythm : A, B, B, A, D, B, A, E, G, A, E, C, B, C, D, A, D, G, B, B, E, B, B, C, A, G, G, A, B, D, A, F#, F#, B, A, C, A, F#, D, B, G, D, A, E, A, A, D, A, B, C, F#
Base 7, 3 digits groups  : 122, 142, 150, 153, 234, 140, 225, 223, 100, 124, 166, 213, 164, 204, 151, 141, 236
Base 10 from Base 7      : 65, 79, 84, 87, 123, 77, 117, 115, 49, 67, 97, 108, 95, 102, 85, 78, 125
ASCII TEXT               : AOTW{Mus1Cal_fUN}
```