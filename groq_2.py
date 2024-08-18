import json
import requests
from groq import Groq
from NetHyTech_HindiTTS import Speak
import speech_recognition as sr
import datetime
import os
from emotion import start_emotion_to_emoji_app
from time import sleep
from main import main as vision_main  # Import the vision main function



def listen_wake_word_hindi(wake_words):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
        print('Recognizing...')
        try:
            text = r.recognize_google(audio, language='hi')
            print(text)
        except sr.UnknownValueError:
            print('Sorry, I could not understand you.')
            return None
    return text

def get_web_info(query, max_results=4, prints=False) -> str:
    url = f"https://oevortex-webscout.hf.space/api/search?q={query}&max_results={max_results}&safesearch=moderate&region=wt-wt"
    response = requests.get(url).json()['results']
    if prints: print(response)

    formatted_results = []
    for result in response:
        body = result.get('body', 'No description')
        formatted_results.append(body)

    return "\n\n".join(formatted_results)

def tell_date_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    return f"Today's date is {date_str} and the current time is {time_str}."

def generate(user_prompt, api_key, system_prompt, prints=False) -> str:
    if "वेब पर ढूंढो" in user_prompt.lower() or "वेब पर सर्च करो" in user_prompt.lower() or "वेब सर्च" in user_prompt.lower() or "search on web" in user_prompt.lower():
        query = user_prompt.lower().replace("वेब पर ढूंढो", "").replace("वेब पर सर्च करो", "").replace("वेब सर्च", "").replace("ask from web", "").strip()
        return get_web_info(query, prints=prints)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = Groq(api_key=api_key).chat.completions.create(
        model='llama3-70b-8192',
        messages=messages,
        max_tokens=4096
    )

    response_message = response.choices[0].message

    return response_message.content

def handle_vision_request(command_hindi):
    # Extract the query after "तुम क्या देख सकते हो" or "आप क्या देख सकते हो"
    vision_query = command_hindi.replace("देख सकते हो", "").replace("आप क्या देख सकते हो", "").replace("देख कर", "").replace("दो से पुछो", "").strip()
    if not vision_query:
        vision_query = "what can you see?"
    
    # Call the vision main function with the vision query
    vision_response = vision_main(vision_query)
    return vision_response

if __name__ == "__main__":
    wake_words = ["रुद्र", "रुद्रा", "रूद्र", "रुद्र", "रूद्रा", "रूद्र", "रूद्र"]

    api_key = "groq api key"

    while True:
        spoken_text = listen_wake_word_hindi(wake_words)
        if spoken_text:
            for word in wake_words:
                if word in spoken_text:
                    command_hindi = spoken_text.replace(word, "").strip()

                    if "समय" in command_hindi or "तारीख" in command_hindi:
                        response = tell_date_time()
                        Speak(response)

                    elif "पता" in command_hindi:
                        start_emotion_to_emoji_app()

                    elif "तुम क्या देख सकते हो" in command_hindi or "देख सकते हो" in command_hindi or "देख कर" in command_hindi:
                        # Handle vision request and pass the command to the vision model
                        vision_response = handle_vision_request(command_hindi)
                        Speak(vision_response)

                    else:
                        response = generate(user_prompt=command_hindi, api_key=api_key, system_prompt="sys prompt", prints=True)
                        print(response)
                        Speak(response)
