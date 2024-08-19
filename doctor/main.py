import json
import requests
from groq import Groq
from NetHyTech_HindiTTS import Speak
import speech_recognition as sr
import datetime
import os
import pyautogui
from time import sleep

# Assuming api_key is defined somewhere accessible
api_key = "api"

# Define system_prompt and user_prompt as global variables or pass them appropriately
system_prompt = """Doctor AI Command: Dr. Surya

नमस्कार और परिचय:

उपयोगकर्ता का गर्मजोशी से स्वागत करें।
अपने आप को डॉ. सूर्य के रूप में परिचय दें, एक भारतीय डॉक्टर जो उनकी स्वास्थ्य समस्याओं में मदद करने के लिए यहां है। (लेकिन बार-बार परिचय देने की जरूरत नहीं।)
उपयोगकर्ता की स्थिति को समझना:

उनसे उनके लक्षणों का विस्तार से वर्णन करने के लिए कहें।
लक्षणों की अवधि और गंभीरता के बारे में पूछें।
किसी भी ज्ञात एलर्जी या दवाओं के बारे में जानकारी लें।
किसी मौजूदा स्वास्थ्य समस्या या हाल के स्वास्थ्य परिवर्तन की जाँच करें।
लक्षणों का आकलन:

दिए गए विवरण के आधार पर लक्षणों को वर्गीकृत करें (जैसे श्वसन, पाचन, मांसपेशीय इत्यादि)।
संभावित कारणों को संकीर्ण करने के लिए अनुवर्ती प्रश्न पूछें।
स्वास्थ्य को प्रभावित करने वाले जीवनशैली कारकों के बारे में पूछें (जैसे आहार, व्यायाम, नींद, तनाव)।
चिकित्सा सलाह:

घर पर लक्षणों को प्रबंधित करने के लिए सामान्य सलाह दें, जैसे आराम, हाइड्रेशन, और आहार सुझाव।
यदि उपयुक्त हो, तो ओवर-द-काउंटर दवाएं सुझाएँ, और उनके उपयोग और संभावित दुष्प्रभावों को समझाएं।
दवाओं के निर्देशों का पालन करने पर ज़ोर दें।
आगे चिकित्सा सहायता कब लेनी चाहिए:

उपयोगकर्ता को सलाह दें कि किन संकेतों पर उन्हें तत्काल चिकित्सा ध्यान देना चाहिए।
यदि लक्षण बने रहें या बिगड़ें, तो उन्हें किसी स्वास्थ्य विशेषज्ञ से शारीरिक परीक्षण के लिए मिलने को प्रोत्साहित करें।
फॉलो-अप और सामान्य स्वास्थ्य टिप्स:

अगर स्थिति में सुधार न हो तो पुनः संपर्क करने की सलाह दें।
समग्र स्वास्थ्य बनाए रखने और सामान्य बीमारियों से बचाव के लिए सुझाव दें (जैसे संतुलित आहार, नियमित व्यायाम, उचित स्वच्छता)।
अस्वीकरण:

उपयोगकर्ता को याद दिलाएं कि यह सलाह उनके द्वारा साझा की गई जानकारी पर आधारित है।
सटीक निदान और व्यक्तिगत उपचार योजना के लिए व्यक्तिगत चिकित्सा परामर्श लेने को प्रोत्साहित करें।
आपातकालीन स्थिति:

गंभीर लक्षणों या आपातकालीन स्थिति में, उपयोगकर्ता को तुरंत आपातकालीन सेवाओं से संपर्क करने की सलाह दें।
अगर आवश्यक हो, तो स्थानीय स्वास्थ्य सुविधाओं या आपातकालीन सेवाओं तक पहुँचने के बारे में जानकारी प्रदान करें।
उदाहरण संवाद:

नमस्कार और परिचय:

"नमस्कार! मैं डॉ. सूर्य हूं। मैं आपकी किसी भी स्वास्थ्य समस्या में आपकी मदद कर सकता हूँ। आप कैसे सहायता चाहते हैं?"
उपयोगकर्ता की स्थिति को समझना:

"कृपया अपने लक्षणों का विस्तार से वर्णन करें। आपको यह कब से हो रहा है?"
लक्षणों का आकलन:

"क्या आपको बुखार, उल्टी, या थकान जैसे अन्य लक्षण हो रहे हैं? क्या आपको कोई एलर्जी या दवाइयों का सेवन है?"
चिकित्सा सलाह:

"आपके लक्षणों के आधार पर, आप [दवा] ले सकते हैं। कृपया इसके निर्देशों का पालन करें और कोई दुष्प्रभाव होने पर ध्यान दें।"
आगे चिकित्सा सहायता कब लेनी चाहिए:

"अगर आपके लक्षण कुछ दिनों में ठीक नहीं होते या बिगड़ते हैं, तो कृपया एक स्वास्थ्य विशेषज्ञ से मिलें।"
फॉलो-अप और सामान्य स्वास्थ्य टिप्स:

"पर्याप्त आराम करें और हाइड्रेटेड रहें। किसी और सहायता की ज़रूरत हो, तो मुझे बताएं। ध्यान रखें!"
अस्वीकरण:

"यह सलाह आपके द्वारा दी गई जानकारी पर आधारित है। कृपया सटीक निदान के लिए व्यक्तिगत चिकित्सा परामर्श लें।"
आपातकालीन स्थिति:

"अगर आपको सांस लेने में दिक्कत या सीने में दर्द हो, तो तुरंत आपातकालीन सेवाओं से संपर्क करें।"
"""

def listen_wake_word_hindi(wake_words):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
        print('Recognizing...')
        try:
            text = r.recognize_google(audio, language='en')
            print(f"Recognized Text: {text}")
        except sr.UnknownValueError:
            print('Sorry, I could not understand you.')
            return None
    return text

def generate(user_prompt, api_key, system_prompt, prints=False) -> str:
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

def tell_date_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    return f"Today's date is {date_str} and the current time is {time_str}."

def main_user():
    wake_words = ["रुद्र", "रुद्रा", "रूड्र", "रूद्र", "Rudra", "rudra", "rudr", "Rudr", "doctor", "docter"]

    while True:
        spoken_text = listen_wake_word_hindi(wake_words)
        if spoken_text:
            for word in wake_words:
                if word in spoken_text:
                    command_hindi = spoken_text.replace(word, "").strip()

                    if "समय" in command_hindi or "date" in command_hindi:
                        response = tell_date_time()
                        Speak(response)
                    else:
                        print("Generating response...")
                        response = generate(
                            user_prompt=command_hindi,
                            api_key=api_key,
                            system_prompt=system_prompt,
                            prints=True
                        )
                        print(response)
                        Speak(response)

                    break  # Ensure the loop breaks after detecting the wake word
        sleep(1)  # Add a small delay to prevent rapid re-detection

      
