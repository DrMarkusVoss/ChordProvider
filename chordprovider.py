# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
import rtmidi
from rtmidi.midiutil import list_input_ports, list_output_ports, open_midiinput

minor_chord = [0,3,7]
major_chord = [0,4,7]
dim_chord = [0,3,6]

# 0 = wrong, 1 = major, 2 = minor, 3 = dim
# C, D, E, F, G, A, B
c_maj_chords =  [1,0,2,0,2,1,0,1,0,2,0,3]

c_maj_notes = {0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"}


def getChord(note_midi, verbose=False):

    note = note_midi % 12
    #major, minor, diminished?
    mmd = c_maj_chords[note]
    chord = [0,0,0]
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


def chordProviderMainLoop():

    midiout = rtmidi.MidiOut()
    available_ports_out = midiout.get_ports()

    #print(available_ports_out)
    list_input_ports()
    list_output_ports()



    # Attempt to open the port
    if available_ports_out:
        midiout.open_port(3)
    else:
        midiout.open_virtual_port("My virtual output")

    note_on = [0x90, 60, 112]
    note_off = [0x80, 60, 0]
    midiout.send_message(note_on)
    time.sleep(0.5)
    # I tried running the script without having to invoke the sleep function but it doesn't work.
    # If someone could enlighten me as to why this is, I'd be more than grateful.
    midiout.send_message(note_off)
    note_on = [0x90, 64, 112]
    note_off = [0x80, 64, 0]
    midiout.send_message(note_on)
    time.sleep(5)
    # I tried running the script     without having to invoke the sleep function but it doesn't work.
    # If someone could enlighten me as to why this is, I'd be more than grateful.
    midiout.send_message(note_off)

    try:
        midiin, port_name = open_midiinput(3)
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    print("Entering main loop. Press Control-C to exit.")
    try:
        timer = time.time()
        while True:
            msg = midiin.get_message()

            if msg:
                message, deltatime = msg
                timer += deltatime
                #print("[%s] @%0.6f %r" % (port_name, timer, message))
                midicmd, note, velocity = message

                if midicmd == 144:
                    #print("NOTE ON")
                    note2, note3 = getChord(note, True)
                    note_on2 = [0x90, note2, velocity]
                    note_on3 = [0x90, note3, velocity]
                    midiout.send_message(note_on2)
                    midiout.send_message(note_on3)
                if midicmd ==128:
                    #print("NOTE OFF")
                    note2, note3 = getChord(note)
                    note_off2 = [0x80, note2, 0]
                    note_off3 = [0x80, note3, 0]
                    midiout.send_message(note_off2)
                    midiout.send_message(note_off3)



            time.sleep(0.01)
    except KeyboardInterrupt:
        print('')
    finally:
        print("Exit.")
        midiin.close_port()
        midiout.close_port()
        del midiin
        del midiout


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chordProviderMainLoop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
