import json
import requests
import base64
from rich import print
from Nara.Extra import TimeIt


stream = True
url = "https://proxy.tune.app/chat/completions"

headers = {
    "Authorization": "sk-tune-5yUVUjlhJMLO9YVIOuU2AhUOKe1N1W527JS",
    "Content-Type": "application/json",
}


system = """sys"""

session = requests.session()

def GPT(prompt:str ,image_B64:str):
    """
    GPT API call to generate response for a given prompt and image.

    Args
    ----
    prompt : str
    image_B64 : str

    Returns
    -------
    response : str
    """

    base64_image = image_B64

    data = {
    "temperature": 0.0,
    
        "messages":  [
    {
        "role": "system",
        "content": [
        {
            "type": "text",
            "text": system
        }
        ]
    },
    {
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": prompt
        },
        {
            "type": "image_url", "image_url": 
            {
                "url": f"data:image/png;base64,{base64_image}"
            }
            
        }
        ]
    },
    ],
        "model": "rohan/tune-gpt-4o",
        "stream": stream,
        "frequency_penalty":  0,
        "max_tokens": 900
    }
    response = session.post(url, headers=headers, json=data)
    text = ""
    if stream:
        for line in response.iter_lines():
            if line:
                l = line[6:]
                if l != b'[DONE]' and "content" in json.loads(l)["choices"][0]["delta"]:
                    text += json.loads(l)["choices"][0]["delta"]["content"]
                    print(json.loads(l)["choices"][0]["delta"]["content"], end="")
    else:
        print("METHOD NOT IMPLEMENTED")
    return text


def FileToBase64(file_path:str):
    """
    Convert image file to base64 string.

    Args
    ----
    file_path : str

    Returns
    -------
    base64_image : str
    """
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_image



if __name__ == "__main__":
    response = GPT(prompt="what is inside the image",image_B64=FileToBase64("img.png"))
