import cv2 as cv
import time
import os


frames_to_skip = 5
frames_per_second = 30
processing_buffer = 0.005
sleep_time = (frames_to_skip/frames_per_second) - processing_buffer


'''
TODOS:
- takes average pixel every 150 pixels (x and y)

- Convert frame to string:
 	- inputs a frame somehow (god knows how)
	- outputs a string that is 22500 characters long (b for white, . for black)


- Add Frame to Json
	- timestamp, frame_data

- Main function should then step a certain amount of frames

- Export Json to file
'''

def get_next_frame(capture, frame_spacing):
    if frame_spacing != 0:
        for _ in range(frame_spacing):
            if not capture.grab():
                # hit end-of-stream or failure
                return (False, None)

    # retrieve the frame grabbed last
    return capture.retrieve()


def frame_to_string(frame):
    image_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    output = ""
    for row in frame:
        for px in row:
            if (px[2] > 127):
                output += " "
            else:   
                output += "0"
        output += "\n"
    
    return output


def play_video_terminal(capture, sleep_time, frame_spacing):
    isTrue, frame = capture.read()

    while True: 
        status, next_frame = get_next_frame(capture, frame_spacing)

        resized_frame = cv.resize(next_frame, (150, 150))

        print(frame_to_string(resized_frame))
        time.sleep(sleep_time)
        os.system('cls')

def play_video_windows(capture, stop_key, sleep_time, frame_spacing):
    isTrue, frame = capture.read()

    while True: 
        status, next_frame = get_next_frame(capture, frame_spacing)

        resized_frame = cv.resize(next_frame, (150, 150))

        cv.imshow('Raw Video', next_frame)
        cv.imshow('Resized Video', resized_frame)
        
        time.sleep(sleep_time)
        
        if cv.waitKey(1) & 0xFF==ord(stop_key):
            break

    # Close the window
    cv.destroyAllWindows()


if __name__ == "__main__":
    capture = cv.VideoCapture('bad_apple_raw.mp4')

    play_video_terminal(capture, sleep_time, frames_to_skip)

    capture.release()
