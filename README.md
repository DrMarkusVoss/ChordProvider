# ChordProvider
Extend single base notes played on a Keyboard or Synthesizer attached via USB MIDI by further notes to form chords according to selected key.
These further notes are transmitted back to to the sender of the original base note, so that by playing one note on the keyboard or synth you get
a full chord with just one finger used.

### Use Cases:
#### Use Case #1:
You have a keyboard or synthesizer, and you want to play with two hands, left hand chords, right hand melody/leads. You are not as good
yet with both. That is why you are only able to play a single base note
with your left hand. Wouldn't it be cool if automatically 2 further notes would be created that form a triad 
that matches the key you are playing in?

On the Korg Wavestate Synthesizer you could do this be using 3 of the 4 layers it offers, by programming
each layer to play one of the notes of the triads, using the pitch lane. So e.g. Layer A keeps the pitch
at 0, while Layers B and C add the third and fifth to the chord by pitching up e.g. 3 semitones and 7 semitones
for a minor chord. Furthermore, you can configure the key which shall be considered when pitching in the Pitch
Lane. The drawback is, that this approach consumes 3 of the 4 lanes of the Synthesizer. When you want to play
a complete song with the Synth, then this approach would not work as you only have one Layer left for all 
other instruments to play.

Here ChordProvider is the solution. With ChordProvider you only need one Layer for complete chords. You play
the base note, the base note is received on your computer via USB MIDI, the computer calculates the complementary
2 notes to create a triad chord and sends them right back to your Synthesizer via USB-MIDI to be played directly.
The latency is negligible. For that, of course, you need to tell your computer which key you want to 
play in, same as you would do on the Wavestate in the configuration of the Pitch Lane. Furthermore, you need
to restrict the Keyzone that shall be used, so that the computer does not make chords out of your lead notes. 

### Installation
#### System setup
- you need a USB-MIDI capable keyboard or synthesizer (like e.g. the Korg Wavestate in my case)
- connect that synthesizer to your computer (Apple Mac Studio in my case) via USB with Python3 and git installed
- open a console and then follow the installation instructions

#### Install latest development
ChordProvider is a Python3 program. So you need to make sure that you have Python3 (e.g. Python 3.8) installed
on your computer. Furthermore, ChordProvider uses the Python binding of the RtMidi library, which provides
an API to utilize MIDI devices that are connected to your computer. 

So, in order to use ChordProvider, you need to install the RtMidi binding first, using pip3:

    pip3 install python-rtmidi

Then download the latest version of ChordProvider. To get the latest developments, clone this git repo to a place somewhere on your Mac/Raspberry Pi or other Unix-like
system:

    git clone https://github.com/DrMarkusVoss/ChordProvider.git
    cd ChordProvider

Then just execute the Python program:

    python3 chordprovider.py


### User's Guide
- select the port of your Input MIDI device (e.g. your Keyboard or Synthesizer)
   where you are going to play the base note
- select the port of your Output MIDI device, where the complementary notes shall
  played. Typically, for Use Case #1, this is the same device as the Input device
- enter the key to which the chords shall belong
- enter the mode of the key to which the chords shall belong
- on your input device, play the lower key for the range of keys where you are going
  to play the base notes
- then play the upper key for the range of keys where you are going to play the base
  notes
- Now you are ready to go! You can play the base notes with one finger and ChordProvider 
  will make a chord out of it, while you play melodies or leads with your other hand/fingers
  on the rest of the keyboard that is not reserved for the base notes.