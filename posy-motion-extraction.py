#!/usr/bin/env python3
#
# A script that perform's Posy's motion extraction on a sample video clip. We
# use Python and OpenCV.
#
# https://www.youtube.com/watch?v=NSS6yAMZF78
#

import cv2
import numpy as np
from sys import argv

HORIZONTAL=1

if len(argv) != 2:
    print(f"usage: {argv[0]} <video file>")
    exit(1)

FRAME_SHIFT=10
delay_queue = []

cap = cv2.VideoCapture(argv[1])
while(cap.isOpened()):
    # first, just read the current frame
    have_frame, current_frame = cap.read()
    if not have_frame:
        break


    # Hold on to the oldest frame in the delat queue and add the current frame
    # to the delay queue, moving everything down the queue one step. Then check
    # if we reached our delay buffer's capacity yet. When we start, this buffer
    # is empty and for the rest of the code to work we need it to be filled to
    # capacity.

    delay_queue.append(current_frame)
    if len(delay_queue) < FRAME_SHIFT:
        continue


    # If we get here, we have the current frame and a suitably delayed frame.
    # For easy debugging, show these side-by-side.

    delayed_frame = delay_queue.pop(0)
    combined_frames = np.concatenate((current_frame, delayed_frame), axis=HORIZONTAL) 

    # The delayed image needs some processing, though. The first operation is to
    # invert it.

    inverted_frame = cv2.bitwise_not(delayed_frame)
    combined_frames = np.concatenate((combined_frames, inverted_frame), axis=HORIZONTAL) 

    blended_frame = cv2.addWeighted(current_frame, 0.5, inverted_frame, 0.5, 0)
    combined_frames = np.concatenate((combined_frames, blended_frame), axis=HORIZONTAL) 

    cv2.imshow('debugging', combined_frames)
    cv2.imshow('frame', blended_frame)

    # & 0xFF is required for a 64-bit system
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

