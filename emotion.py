import cv2
from deepface import DeepFace
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Mapping emotions to emojis
emotion_to_emoji = {
    'happy': '😊',
    'sad': '😢',
    'angry': '😠',
    'surprise': '😮',
    'neutral': '😐'
}

def start_emotion_to_emoji_app():
    # Initialize the webcam
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot open webcam")
        return  # Exit the function if the webcam is not opened

    # Initialize Tkinter window
    root = tk.Tk()
    root.title("Emotion to Emoji")

    # Create frames for better layout
    frame_video = tk.Frame(root, bg='white')
    frame_video.pack(side=tk.LEFT, padx=10, pady=10)

    frame_emoji = tk.Frame(root, bg='white')
    frame_emoji.pack(side=tk.RIGHT, padx=10, pady=10)

    # Video feed label
    video_label = tk.Label(frame_video)
    video_label.pack()

    # Emoji label
    emoji_label = tk.Label(frame_emoji, font=("Helvetica", 100), bg='white')
    emoji_label.pack()

    def update_frame():
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            return

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform emotion recognition
        results = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)

        if isinstance(results, list) and results:
            result = results[0]
            dominant_emotion = result['dominant_emotion']
        else:
            dominant_emotion = 'neutral'

        # Update the emoji based on the detected emotion
        emoji = emotion_to_emoji.get(dominant_emotion, '😐')
        emoji_label.config(text=emoji)

        # Convert the frame to ImageTk format and update the video label
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Schedule the function to run again after 100 milliseconds
        root.after(100, update_frame)

    # Start the update loop
    update_frame()

    # Start the Tkinter main loop
    root.mainloop()

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
