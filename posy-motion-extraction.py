#!/usr/bin/env python3
#
# A script that perform's Posy's motion extraction on a sample video clip. We
# use Python and OpenCV.
#

import cv2
import numpy as np
from os import path
from sys import argv

HORIZONTAL=1


# Define the time/frame shifting buffer. The amount of shift is tracked as
# `frame_shift` and we keep the frames in the `delay_queue` until they have been
# shifted enough to be processed.
#
# The value of `frame_shift` and thus the capacity of the delay queue gets set
# dynamically from the trackbar on the main window, using the
# `set_frame_shift()` callback function.
#
# We shift a minimum of 2 frames, otherwise the output is just a gray box.

frame_shift=20
delay_queue = []

def set_frame_shift(new_frame_shift):
    global frame_shift
    if new_frame_shift < 2:
        cv2.setTrackbarPos("delay (frames)", MAIN_WINDOW, 2)
    else:
        frame_shift = new_frame_shift


# Define the mixing proportions between the processed frame and the current frame in percentages.

processed_proportion=50

def set_processed_proportion(new_processed_proportion):
    global processed_proportion
    processed_proportion = new_processed_proportion


# Open the specified video source and name the main window so the user knows
# what they are looking at and the code has a reference for the trackbars. With
# this information, build the basic layout of the main window and attach
# trackbar callbacks to handle user input.

if len(argv) == 1:
    MAIN_WINDOW="webcam"
    video_source = cv2.VideoCapture(0)
elif len(argv) == 2:
    if path.exists(argv[1]):
        MAIN_WINDOW=path.basename(argv[1])
        video_source = cv2.VideoCapture(argv[1])
    else:
        print(f"No such file: {argv[1]}")
        exit(1)
else:
    print(f"usage: {argv[0]} [<video file>]")
    print(f"    Opens the specified video file. If no video file is specified, open the conputer's webcam instead.")
    exit(1)

cv2.namedWindow(MAIN_WINDOW)
cv2.createTrackbar("delay (frames)",        MAIN_WINDOW, frame_shift,          100, set_frame_shift)
cv2.createTrackbar("mix current/processed", MAIN_WINDOW, processed_proportion, 100, set_processed_proportion)


# Process each frame in turn.
while(video_source.isOpened()):
    # first, just read the current frame
    have_frame, current_frame = video_source.read()
    if not have_frame:
        if len(argv) == 2: # i.e. we have a video file
            # reset to the start of the file and clear the delay queue
            video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
            delay_queue = []
            _, current_frame = video_source.read()
        else:
            break # video done, release() and destroy windows


    # We append the current frame to the end of the delay queue, then take the
    # oldest frame from the queue for use as the delayed frame, below. This
    # gives us the time shift that the algorithm asks for.
    #
    # A complicating factor is that we allow the user to set the time shift from
    # the trackbar above the video. Since that can change at any time, we have
    # to allow the buffer to expand and contract based on that setting. We solve
    # this by clipping the buffer to the capacity if it is longer than what the
    # user specified. This will handle reductions well.

    delay_queue.append(current_frame)
    delay_queue = delay_queue[-frame_shift:]
    delayed_frame = delay_queue[0]

    # If we get here, we have the current frame and a suitably delayed frame.
    # For easy debugging, show these side-by-side.

    combined_frames = np.concatenate((current_frame, delayed_frame), axis=HORIZONTAL)


    # The delayed image needs some processing, though. The first operation is to
    # invert it.

    inverted_frame = cv2.bitwise_not(delayed_frame)
    combined_frames = np.concatenate((combined_frames, inverted_frame), axis=HORIZONTAL)


    # Then we blend the inverted and original frames, each at 50% alpha.

    mix_processed = processed_proportion / 100.0
    mix_current = 1.0 - mix_processed
    blended_frame = cv2.addWeighted(current_frame, mix_current, inverted_frame, mix_processed, 0)
    combined_frames = np.concatenate((combined_frames, blended_frame), axis=HORIZONTAL)


    # We can now render the frames.

    cv2.imshow('debugging', combined_frames)
    cv2.imshow(MAIN_WINDOW, blended_frame)

    # & 0xFF is required for a 64-bit system
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_source.release()
cv2.destroyAllWindows()

