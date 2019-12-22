from mido import MidiFile
import mido as mido


chromatic_scale = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

notes = []
midi_file = MidiFile('Stegno.mid')
# midi_file = MidiFile('databits.mid')
track = mido.merge_tracks(midi_file.tracks)
ticks_beat = midi_file.ticks_per_beat

tempo = 0
bpm = 0
times = []
play_time = 0
for msg in track:
    # print(msg)
    msg_dict = msg.dict()
    play_time += msg_dict.get('time')
    if msg_dict.get('type') == 'set_tempo':
        tempo = msg_dict.get('tempo')
        bpm = round(mido.tempo2bpm(tempo))
        # print(bpm)
    if msg_dict.get('velocity') != 0 and msg_dict.get('type') == 'note_on':
        times.append('{}{}'.format(msg_dict.get('time'), chromatic_scale.get(msg_dict.get('note') % 12)))
        print('{}  {}  {}'.format( play_time, chromatic_scale.get(msg_dict.get('note') % 12), (play_time % ticks_beat)/(ticks_beat/4)))
        

print(times)


# {'type': 'time_signature', 'numerator': 4, 'denominator': 4, 'clocks_per_click': 24, 'notated_32nd_notes_per_beat': 8, 'time': 0}
# {'type': 'key_signature', 'key': 'G', 'time': 0}
# {'type': 'set_tempo', 'tempo': 545455, 'time': 0}
# ticksperbeat = 480