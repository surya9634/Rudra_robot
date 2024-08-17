from Cam import capture_and_encode_base64
from Gpt import GPT
from NetHyTech_HindiTTS import Speak

def main(query="what can you see?"):
    base64_image = capture_and_encode_base64()
    if base64_image is not None:
        print("Base64 Encoded Image:", base64_image[:50], "...")
    else:
        print("Error occurred during image capture and encoding.")
        return "Image capture failed."

    # Use the query provided to the function
    response = GPT(prompt=query, image_B64=base64_image)
    
    if response:
        print("Response from GPT:", response)
        return response
    else:
        return "No response from GPT."

if __name__ == "__main__":
    main()
