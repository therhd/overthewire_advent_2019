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

We can treat notes in the G Major Scale as base 7, starting with G = 0

| | | | | | | | | | | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
|C|C#|D|D#|E|F|F#|G|G#|A|A#|B|C|C#|D|D#|E|F|F#|
|C|  |D|  |E| |F#|G|  |A|  |B|C|  |D|  |E| |F#|
|3|  |4|  |5| |6 |0|  |1|  |2|3|  |4|  |5| |6 |

## On Musical Rhythm
![Ableton Piano Roll](musical_steganography/screenshots/Duple_note_values_comparison.png)


![Sheet Music](musical_steganography/screenshots/sheetmusic.png)


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