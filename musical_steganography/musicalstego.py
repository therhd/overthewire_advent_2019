from mido import MidiFile
import mido as mido

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

def sept_to_gmaj(num_list):
    final = []
    for num in num_list:
        for n in split(str(num)):
            final.append(gmaj.get(int(n)))
    return final

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
            

def char_to_dec(char_list):
    final = []
    for char in char_list:
        final.append(ord(char))
    return final

def dec_to_char(dec_list):
    final = []
    for dec in dec_list:
        final.append(chr(dec))
    return final

def split(word):
    return [char for char in word]

# Testng
# notes = 'ABBADBAEGAECBCD' # beginning to 28 bar 1
# notes = split(notes)

# Working from midi file modified by hand to remove non-data notes.
# notes = []
# for msg in MidiFile('databits.mid'):
#     if msg.type == 'note_on':
#         notes.append(chromatic_scale.get(msg.note % 12))

# Working from challenge provided midi file, attempting to find extra data bits by rhythm

chromatic_scale = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

midi_file = MidiFile('Stegno.mid')
# midi_file = MidiFile('databits.mid')
track = mido.merge_tracks(midi_file.tracks)
ticks_per_beat = midi_file.ticks_per_beat

notes = []
play_time = 0
for msg in track:
    m = msg.dict()
    play_time += m.get('time')

    # each beat is a quarter note, we care about eighth notes
    eighths = (play_time % ticks_per_beat)/(ticks_per_beat/4) 

    # Pick odd eighth notes
    if (m.get('type') == 'note_on'
    and m.get('velocity') != 0
    and (eighths % 2) != 0):
        notes.append(chromatic_scale.get(m.get('note') % 12))

# Decoding
print('Selected notes by rhythm : {}'.format(', '.join(notes)))

sept = gmaj_to_sept(notes)
print('Base 7, 3 digits groups  : {}'.format(', '.join(sept)))

decimal = sept_to_dec(sept)
print('Base 10 from Base 7      : {}'.format(', '.join(map(str, decimal))))

chars = dec_to_char(decimal)

print('ASCII TEXT               : {}'.format(''.join(chars)))


# Encoding
# flag = 'AOTW{}'
# flag = split(flag)
# print(sept_to_gmaj([1]))
# print(dec_to_sept())
# print(char_to_dec(flag))
# print(dec_to_sept(char_to_dec(flag)))
# print(sept_to_gmaj(dec_to_sept(char_to_dec(flag))))
