import time
from math import hypot
import cv2
import dlib
import serial

# Initializiation
conversion_morse = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', ' ': 'S' , '?':'?'
}

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("C:\\Users\\ThinkPad\\Desktop\\neuroblink\\shape_predictor_68_face_landmarks.dat")


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

font = cv2.FONT_HERSHEY_PLAIN

def get_eye_ratio(eye_points, facial_landmarks, frame):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    return ver_line_length

def wrap_text(text, max_width):
    words = text.split(" ")
    wrapped_lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) <= max_width:
            current_line += word + " "
        else:
            wrapped_lines.append(current_line)
            current_line = word + " "
    wrapped_lines.append(current_line)
    return wrapped_lines

blink_start_time = None
start_time = time.time()
blink_end_time = None
blinking = False
blinking_chars = []
k = 0
detected_phrase = ""
#Serial Communication Initialization
try:
        ser = serial.Serial('COM5', 115200, timeout=2)
        print("Serial connection opened.")
except serial.SerialException as e:
        print("Failed to open serial port:", e)
        ser = None
# Blinking loop
while time.time() - start_time < 360:  # Run for 6 minutes
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype('uint8')
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye_ratio = get_eye_ratio([36, 37, 38, 39, 40, 41], landmarks, frame)
        right_eye_ratio = get_eye_ratio([42, 43, 44, 45, 46, 47], landmarks, frame)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio < 8 and not blinking:
            blink_start_time = time.time()
            blinking = True
        elif blinking_ratio > 12 and blinking:
            blink_end_time = time.time()
            blinking = False
            elapsed_time = blink_end_time - blink_start_time
            if 0.5 < elapsed_time < 2:
                blinking_chars.append(".")
            elif 2 < elapsed_time < 3:
                blinking_chars.append("-")
            elif 3 < elapsed_time < 4:
                blinking_chars.append("+")
            elif 4 < elapsed_time < 5:
                blinking_chars.append("S")
            elif  elapsed_time > 5:
                blinking_chars.append("?")
            detected_phrase = "".join(blinking_chars)

    # Wrap text for better display
    wrapped_text = wrap_text(detected_phrase, max_width=100)  # Adjust max_width as needed
    y_offset = 50
    for line in wrapped_text:
        cv2.putText(frame, line, (50, y_offset), font, 2, (255, 0, 0), 2)
        y_offset += 40

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

print("La phrase est:", detected_phrase)

message_converti = ""

i = 0
while i < len(detected_phrase):
    if detected_phrase[i] == 'S':
        message_converti += " "
        i += 1
    elif detected_phrase[i] != '+':
        letter = ""
        while i < len(detected_phrase) and detected_phrase[i] not in ['+', 'S']:
            letter += detected_phrase[i]
            i += 1
        for letter_morse, code_morse in conversion_morse.items():
            if code_morse == letter:
                message_converti += letter_morse
    elif detected_phrase[i] == '+':
        i += 1

cap.release()
cv2.destroyAllWindows()
message_converti = message_converti + "\n"
print("La phrase convertie est:", message_converti)
ser.write(message_converti.encode())
if ser:
    ser.close()
    print("Serial port closed.")