import cv2 as cv
import time

frames_to_skip = 5
frames_per_second = 30
processing_buffer = 0.01


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
def play_video(capture, stop_key, sleep_time, frame_spacing):
    isTrue, frame = capture.read()

    # Iterate through video frames until the given key is pressed
    while True: 
        status, next_frame = get_next_frame(capture, frame_spacing)

        cv.imshow('Raw Video', next_frame)

        time.sleep(sleep_time)
        
        if cv.waitKey(1) & 0xFF==ord(stop_key):
            break

    # Close the window
    cv.destroyAllWindows()


def get_next_frame(capture, frame_spacing):
    if frame_spacing != 0:
        for _ in range(frame_spacing):
            if not capture.grab():
                # hit end-of-stream or failure
                return (False, None)

    # retrieve the frame grabbed last
    return capture.retrieve()


if __name__ == "__main__":
    capture = cv.VideoCapture('bad_apple_raw.mp4')

    play_video(capture, 'd', (frames_to_skip/frames_per_second) - processing_buffer, frames_to_skip)

    capture.release()
