# import cv2
# import base64

# def capture_and_encode_base64_and_save():
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         print("Error: Couldn't open webcam")
#         return None

#     ret, frame = cap.read()

#     if ret:
#         cv2.imwrite("captured_image.png", frame)

#         _, buffer = cv2.imencode('.png', frame)
#         base64_image = base64.b64encode(buffer).decode('utf-8')
#         cap.release()
#         return base64_image
#     else:
#         print("Error: Couldn't capture frame")
#         cap.release()
#         return None

import cv2
import base64
from Nara.Extra import TimeIt



@TimeIt
def capture_and_encode_base64():
    """
    Captures a frame from the webcam and encodes it as base64.

    Returns:
    str: Base64-encoded image data
    """
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Couldn't open webcam")
        exit()
    ret, frame = cap.read()

    if ret:
        _, buffer = cv2.imencode('.png', frame)
        base64_image = base64.b64encode(buffer).decode('utf-8')
        cap.release()
        return base64_image
    else:
        print("Error: Couldn't capture frame")
        cap.release()
        return None

    

if __name__ == '__main__':
    for i in range(10):
        base64_image = capture_and_encode_base64()
        if base64_image is not None:
            print("Base64 Encoded Image:", base64_image[:50], "...")
        else:
            print("Error occurred during image capture and encoding.")