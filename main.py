import cv2
import mediapipe as mp
import pyautogui
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import openai
from config import apikey
import os
import random

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n ********************************** \n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/prompt - {random.randint(1, 536547895)}", "w") as f:
        f.write(text)

    first_sentence = text.split('.')[0]
    first_sentence.replace("OpenAI response for Prompt:  write a 100 word abstract about 4 gpt ", "")
    engine.say(first_sentence)
    engine.runAndWait()
    engine.say("You can read the following text in the terminal")
    engine.runAndWait()

    if len(text) > len(first_sentence):
        print("You can read the following text in the terminal:")
        print(text)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    speak("Hello!")
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 15:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        speak("Sorry! I did not understand. Please say that again.")
        print("Sorry! I did not understand. Please say that again.\n")
        return "None"

    return query


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    # print(landmark_points)

    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            # print(x, y)

            if id == 1:
                screen_x = int(landmark.x * screen_w)
                screen_y = int(landmark.y * screen_h)
                pyautogui.moveTo(screen_x, screen_y)
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        # print(left[0].y - left[1].y)

        if left[0].y - left[1].y < 0.01:
            # print('click')
            pyautogui.click()
            pyautogui.sleep(1)

        right = [landmarks[475], landmarks[477]]
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        # print(right[1].y - right[0].y)
        if right[1].y - right[0].y < 0.024:
            # print('click')
            pyautogui.rightClick()
            pyautogui.sleep(1)

        if right[1].y - right[0].y < 0.024 and left[0].y - left[1].y < 0.01:
            cam.release()
            cv2.destroyAllWindows()
            start = takeCommand().lower()
            wishMe()
            flag = True
            while flag == True:
                query = takeCommand().lower()

                if 'wikipedia' in query:
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=1)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)

                elif "using artificial intelligence".lower() in query.lower():
                    query = query.replace("using artificial intelligence", "")
                    ai(prompt=query)

                elif 'time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    print(f"Time: {strTime}")
                    speak(f"The time is {strTime}")

                elif "date" in query:
                    strDate = datetime.datetime.now().strftime("%d%m%Y")
                    months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                              'September', 'October', 'November', 'December']
                    print(strDate)
                    speak(f"today's date is {months[(int(strDate[:2]))]} {strDate[2:4]} {strDate[4:]}")

                elif 'search' in query or 'what is' in query:
                    webbrowser.open(
                        f"https://www.google.com/search?q={query}&rlz=1C1RLNS_enIN973IN973&sxsrf=ALiCzsaCNlbRllUgWsk_jitXE3vy25mzgA%3A1665244874925&ei=yp5BY__9N8yI4-EPlq2-8A4&ved=0ahUKEwj_iu_JgNH6AhVMxDgGHZaWD-4Q4dUDCA4&uact=5&oq=bye&gs_lcp=Cgdnd3Mtd2l6EAMyCgguELEDENQCEEMyCgguELEDENQCEEMyCgguELEDENQCEEMyCgguELEDENQCEEMyBAgAEEMyBAguEEMyBwgAELEDEEMyBwgAELEDEEMyBQgAEIAEMgcIABCxAxBDOgoIABBHENYEELADOg0IABBHENYEELADEMkDOgcIABCwAxBDOg0IABDkAhDWBBCwAxgBOgwILhDIAxCwAxBDGAI6DwguENQCEMgDELADEEMYAjoHCCMQ6gIQJzoECCMQJzoECC4QJzoFCAAQkQI6CAguEIAEELEDOgsIABCABBCxAxCDAUoECEEYAEoECEYYAVCrEVirHGD9ImgCcAF4BYAB0wWIAZoSkgELMC4xLjQuNS0xLjGYAQCgAQGwAQrIARPAAQHaAQYIARABGAnaAQYIAhABGAg&sclient=gws-wiz")

                elif 'open youtube' in query:
                    webbrowser.open("youtube.com")

                elif 'open mail' in query:
                    webbrowser.open("gmail.com")

                elif 'open google' in query:
                    webbrowser.open("google.com")

                elif 'goodbye' in query:
                    speak("Goodbye. Have a good day.")
                    print("Bye Bye")
                    flag = False
        # _, frame = cam.read()


    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)


