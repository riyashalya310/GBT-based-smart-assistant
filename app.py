import os
import openai
import speech_recognition as sr  # Converts voice commands to text
import pyttsx3  # Read out text output to voice
import webbrowser

# Model selection
Model = 'gpt-3.5-turbo'

# Retrieve OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

def Reply(question):
    completion = client.chat.completions.create(
        model=Model,
        messages=[
            {'role': "system", "content": "You are a helpful assistant"},
            {'role': 'user', 'content': question}
        ],
        max_tokens=200
    )
    answer = completion.choices[0].message['content']
    return answer

# Text-to-speech setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening .......')
        r.pause_threshold = 1  # Wait for 1 sec before considering the end of a phrase
        audio = r.listen(source)
    try:
        print('Recognizing ....')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except Exception as e:
        print("Say that again .....")
        return "None"
    return query

if __name__ == '__main__':
    speak("Hello! How are you?")
    while True:
        query = takeCommand().lower()
        if query == 'none':
            continue

        ans = Reply(query)
        print(ans)
        speak(ans)

        # Specific browser-related tasks
        if "open youtube" in query:
            webbrowser.open('www.youtube.com')
        if "open google" in query:
            webbrowser.open('www.google.com')
        if "bye" in query:
            break
