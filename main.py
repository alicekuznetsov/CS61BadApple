import cv2 as cv
import time


'''
TODOS:
- probably OpenCV
- inputs a video file
- takes average pixel every 150 pixels (x and y)


- Convert frame to string:
 	- inputs a frame somehow (god knows how)
	- outputs a string that is 22500 characters long (b for white, . for black)


- Add Frame to Json
	- timestamp, frame_data

- Main function should then step a certain amount of frames

- Export Json to file
'''
def playVideo(capture, stopKey, framesPerSecond):
    isTrue, frame = capture.read()

    # Iterate through video frames until the given key is pressed
    while True: 
        isTrue, frame = capture.read()

        cv.imshow('Raw Video', frame)


        time.sleep(1/framesPerSecond)
        
        if cv.waitKey(1) & 0xFF==ord(stopKey):
            break

    # Close the window
    capture.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    capture = cv.VideoCapture('bad_apple_raw.mp4')

    playVideo(capture, 'd', 30)

