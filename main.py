import cv2 as cv
import time
import os

class constants_proj0:
    frames_to_skip = 2
    frames_per_second = 30
    processing_buffer = 0.005
    new_frame_width = int(480 * 0.4)
    new_frame_height = int(360 * 0.4)
    sleep_time = (frames_to_skip/frames_per_second) - processing_buffer

class constants_terminal:
    frames_to_skip = 3
    frames_per_second = 60
    processing_buffer = 0.01
    new_frame_width = int(480 * 0.4)
    new_frame_height = int(360 * 0.4)
    sleep_time = (frames_to_skip/frames_per_second) - processing_buffer

def get_next_frame(capture, frame_spacing):
    """
    Retrieve the next frame from a capture, skipping frame_spacing frames.
    Returns: status (success/fail), frame
    """
    if frame_spacing != 0:
        for _ in range(frame_spacing):
            if not capture.grab():
                # hit end-of-stream or failure
                return (False, None)

    # retrieve the frame grabbed last
    return capture.retrieve()


def frame_to_string(frame, new_lines):
    """
    Note: new_lines is used to add lines between each row in a given frame, not between frames.
    """
    image_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    output = ""
    for row in frame:
        for px in row:
            if (px[2] > 127):
                output += "b"
            else:   
                output += "."
        if(new_lines):
            output += "\n"
    
    return output


def play_video_terminal(capture, sleep_time, frame_spacing):
    isTrue, frame = capture.read()

    while True: 
        status, next_frame = get_next_frame(capture, frame_spacing)

        resized_frame = cv.resize(next_frame, (constants_terminal.new_frame_width, constants_terminal.new_frame_height))

        print(frame_to_string(resized_frame, True))
        time.sleep(sleep_time)
        os.system('cls')

def play_video_windows(capture, stop_key, sleep_time, frame_spacing):
    isTrue, frame = capture.read()

    while True: 
        status, next_frame = get_next_frame(capture, frame_spacing)

        resized_frame = cv.resize(next_frame, (constants_proj0.new_frame_width, constants_proj0.new_frame_height))

        cv.imshow('Raw Video', next_frame)
        cv.imshow('Resized Video', resized_frame)
        
        time.sleep(sleep_time)
        
        if cv.waitKey(1) & 0xFF==ord(stop_key):
            break

    # Close the window
    cv.destroyAllWindows()

def write_to_txt(capture, frame_spacing):
    # Credit to https://www.geeksforgeeks.org/python/writing-to-file-in-python/
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("If it has 2 colors, it can play Bad Apple\n")

    status, next_frame = get_next_frame(capture, frame_spacing)
    resized_frame = cv.resize(next_frame, (constants_proj0.new_frame_width, constants_proj0.new_frame_height))

    while status:
        resized_frame = cv.resize(next_frame, (constants_proj0.new_frame_width, constants_proj0.new_frame_height))
        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(frame_to_string(resized_frame, True))
        status, next_frame = get_next_frame(capture, frame_spacing)


if __name__ == "__main__":
    capture = cv.VideoCapture('bad_apple_raw.mp4')

    choice = ""
    def valid_choice(x):
        return (x == "terminal") or (x == "proj0")
    
    while not valid_choice(choice):
        choice = input("Where would you like Bad Apple to play? (terminal or proj0): ")
        choice = choice.lower()
        if not valid_choice(choice):
            print("Invalid input provided! :(")

    if (choice == "terminal"):
        play_video_terminal(capture, constants_terminal.sleep_time, constants_terminal.frames_to_skip)
    else:
        start_time = time.time()
        
        print(f"Beginning write to output.txt...")
        write_to_txt(capture, constants_proj0.frames_to_skip)
        print(f"All frames added to output.txt. Took {time.time() - start_time} seconds.")
        
        capture.release()
