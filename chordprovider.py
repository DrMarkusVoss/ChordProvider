import sys
import time
import rtmidi
from rtmidi.midiutil import list_input_ports, list_output_ports, open_midiinput

minor_chord = [0, 3, 7]
major_chord = [0, 4, 7]
dim_chord = [0, 3, 6]

# 0 = wrong, 1 = major, 2 = minor, 3 = dim
# C, D, E, F, G, A, B
c_maj_chords = [1, 0, 2, 0, 2, 1, 0, 1, 0, 2, 0, 3]

c_maj_notes = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}

major_scale_interval_adders = [2, 2, 1, 2, 2, 2, 1]
minor_scale_interval_adders = [2, 1, 2, 2, 1, 2, 2]

major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
minor_scale_intervals = [0, 2, 3, 5, 7, 8, 10]

selected_input_port = 0
selected_output_port = 0
selected_key = ""
selected_mode = 0
key_offset = 0
keyzone_lower_bound = 0
keyzone_upper_bound = 0
midiin = None



def chordProviderMainLoop():
    global midiin

    midiout = rtmidi.MidiOut()

    list_input_ports()

    selectInputPort()

    list_output_ports()

    selectOutputPort()

    selectKey()

    selectMode()


    # open MIDI port 3 (which is in my setup a Kork Wavestate)
    midiout.open_port(selected_output_port)

    try:
        midiin, port_name = open_midiinput(selected_input_port)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    learnKeyZoneLowerBound()

    learnKeyZoneUpperBound()

    modestr = {1: "major", 2: "minor"}

    print("\nChordProvider is active now!\n\nPlay your base notes on your musical device (e.g. synth).")
    print("ChordProvider will complement it with 2 or more additional notes\nto form a chord considering the key of: " + selected_key + " " + modestr[selected_mode])
    print("\nPress Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midiin.get_message()

            if msg:
                message, deltatime = msg
                timer += deltatime
                # print("[%s] @%0.6f %r" % (port_name, timer, message))
                midicmd, note, velocity = message

                # complement the received note only if it is in the defined
                # keyzone, so that you can play on one part the chords, and
                # on another part of the keyboard the leads, where you do
                # not want the notes to be complemented to chords.
                if note >= keyzone_lower_bound and note <= keyzone_upper_bound:
                    if midicmd == 144:
                        # print("NOTE ON")
                        note2, note3 = getChord(note, True)
                        note_on2 = [0x90, note2, velocity]
                        note_on3 = [0x90, note3, velocity]
                        midiout.send_message(note_on2)
                        midiout.send_message(note_on3)
                    if midicmd == 128:
                        # print("NOTE OFF")
                        note2, note3 = getChord(note)
                        note_off2 = [0x80, note2, 0]
                        note_off3 = [0x80, note3, 0]
                        midiout.send_message(note_off2)
                        midiout.send_message(note_off3)
            # time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        midiout.close_port()
        del midiin
        del midiout



def learnKeyZoneLowerBound():
    global keyzone_lower_bound, midiin

    print("\nPlay Lowest Key for base note on your device now...")
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            midicmd, note, velocity = message

            if midicmd == 144:
                keyzone_lower_bound = note
                print(c_maj_notes[note%12])
                break



def learnKeyZoneUpperBound():
    global keyzone_upper_bound, midiin

    print("\nPlay Highest Key for base note on your device now...")
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            midicmd, note, velocity = message

            if midicmd == 144:
                keyzone_upper_bound = note
                print(c_maj_notes[note%12])
                break


def selectInputPort():
    global selected_input_port
    portnrstr = input("Select the input port by typing the corresponding number: ")
    selected_input_port = int(portnrstr)


def selectOutputPort():
    global selected_output_port
    portnrstr = input("Select the output port by typing the corresponding number: ")
    selected_output_port = int(portnrstr)


def selectKey():
    global selected_key
    global key_offset
    keystr = input("\nSelect the key in which to produce the chords (e.g. C, D, F, ...): ")
    selected_key = keystr.capitalize()
    key_offset = list(c_maj_notes.keys())[list(c_maj_notes.values()).index(selected_key)]
    #print("offset = " + str(key_offset))
    pass


def selectMode():
    global selected_mode
    modestr = input("\nSelect the mode in which to produce the chords, 1=major 2=minor: ")
    selected_mode = int(modestr)


def getChord(note_midi, verbose=False):
    global selected_mode

    note = note_midi % 12

    # for major key mode
    if selected_mode == 1:
        # major, minor, diminished?
        # offset in semitones relative to C, that is why the
        # offset can be subtracted from the note that is taken
        # from the C major scale chords
        mmd = c_maj_chords[note - key_offset]
    # for minor key mode
    elif selected_mode == 2:
        # C major = A minor; A is 9 semitones above C
        mmd = c_maj_chords[((note + 9)%12) - key_offset]
    else:
        mmd = 99

    chord = [0, 0, 0]

    if mmd == 0:
        if verbose:
            print("Wrong note for key and scale!")
    elif mmd == 1:
        chord = major_chord
        if verbose:
            print(c_maj_notes[note] + " major")
    elif mmd == 2:
        chord = minor_chord
        if verbose:
            print(c_maj_notes[note] + " minor")
    elif mmd == 3:
        chord = dim_chord
        if verbose:
            print(c_maj_notes[note] + " diminished")
    else:
        print("ERROR#1 while creating chord")

    note2 = note_midi + chord[1]
    note3 = note_midi + chord[2]

    return note2, note3



def testField():
# some code to explore and test some funcitonality.
# not used for the productive part.
    midiout = rtmidi.MidiOut()
    available_ports_out = midiout.get_ports()

    print(available_ports_out)

    note_on = [0x90, 60, 112]
    note_off = [0x80, 60, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    midiout.send_message(note_off)
    note_on = [0x90, 64, 112]
    note_off = [0x80, 64, 0]
    midiout.send_message(note_on)
    time.sleep(5)
    midiout.send_message(note_off)


if __name__ == '__main__':
    chordProviderMainLoop()

