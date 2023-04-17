#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image as ROSImage
from std_msgs.msg import String
from abjad import Block, LilyPondFile, Staff, Voice
from abjad.persist import as_midi
import os
import tempfile
from sound_play.msg import SoundRequest
from midi2audio import FluidSynth

# create lilypond file from sentence
def create_lilypond_file(sentence):
    # generate abjad staff
    voice = Voice(sentence)
    staff = Staff([voice])

    # generate lilypond file
    header_block = Block(name="header")
    header_block.tagline = "#ff"
    lilypond_file = LilyPondFile(
        items=[
            header_block,
            """#(set-default-paper-size "a8" 'landscape)""",
            "#(set-global-staff-size 16)",
            staff,
        ]
    )

    return lilypond_file

# create audio from lilypond
def create_audio_from_lilypond(sentence):
    lilypond_file  = create_lilypond_file(sentence)

    # store lilypond as midi temporarily
    # store temporarily due to parser limitations concerning '\midi' https://abjad.github.io/api/abjad/parsers/parser.html 
    temp_ = tempfile.TemporaryFile()
    as_midi(lilypond_file, str(temp_.name), remove_ly=True, resolution=200)
    midi_filename = str(temp_.name) + ".mid"

    # create audio from midi
    # it is hardcoded for now, could be changed to a temporary file as well
    audio_filename = "vision_result_audio.wav"
    FluidSynth().midi_to_audio(midi_filename, audio_filename)

    return audio_filename

# callback for vision node, includes audio publisher
def callback_vision_results(data: String, callback_args):
    rospy.logdebug("received recognized sentence")
    audio_publisher = callback_args

    audio_filename = create_audio_from_lilypond(data.data)
    rospy.logdebug(f"created audio file {audio_filename}")

    # send audio to audio node (sound_play package)
    # http://docs.ros.org/en/api/sound_play/html/msg/SoundRequest.html
    sound_request = SoundRequest()
    sound_request.sound = -2
    sound_request.command = 1
    sound_request.volume = 0.5
    sound_request.arg = audio_filename

    audio_publisher.publish(sound_request)


# create audio from lilypond publisher
# send audio to audio node (sound_play package)
def listener():
    rospy.init_node('visualization_node')

    # TODO: create audio from lilypond publisher
    pub = rospy.Publisher('soundplay_node/SoundRequest', ROSImage, queue_size=50)
    rospy.Subscriber("vision_node/recognized_sentence", String, callback_vision_results, callback_args=(pub))

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
