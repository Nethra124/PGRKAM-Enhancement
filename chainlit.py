import chainlit as cl
import speech_recognition as sr
import chainlit as cl
import streamlit as st 
from dotenv import load_dotenv
import pandas as pd
import openai
from datetime import date
from chainlit.input_widget import Select, Switch, Slider
load_dotenv()
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
import os
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def hindi_trans(text):
    # Transliterate from Roman script to Devanagari script (Hindi)
    return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)

def punjabi_trans(text):
    # Transliterate from Roman script to Gurmukhi script (Punjabi)
    return transliterate(text, sanscript.ITRANS, sanscript.GURMUKHI)

openai_api_key = "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"
df = pd.read_csv("naukri.csv")
nav=pd.read_excel("navigation.xlsx")
# nav=df

@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to the pgrkam job portal how can i help you?"
    await msg.update()
    #increase the size of the action button in the chatbot user interface
    settings = await cl.ChatSettings([
    Select(
            id="Model",
            label="Select Language",
            values=[ "Punjabi","Hindi"],
            initial_index=0,
            )]).send()
    
    
    
    
    # actions = [
    #     cl.Action(name="action_button", value="example_value", description="Click me!", size="large"),
    #     cl.Action(name="action_button", value="example_value", description="Click me!", size="large"),
        
    # ]
    # await cl.Message(content="Interact with this action button:", actions=actions).send()
    
@cl.on_message
async def main(message: cl.Message):
    settings = await cl.ChatSettings([
    Select(
            id="Model",
            label="Select Language",
            values=[ "Punjabi","Hindi"],
            initial_index=0,
            )]).send()
    today = date.today()
    messages = [
    {"role": "system", "content": f"{today} is the current date You are a helpful assistant to assist users from the information given the information is {df} and this is your realtime data and you are asked to reply based on the data provided and dont say something like i dont have or i am not aware or without complete information i cant dont say like that now when they ask something like ctc then it means cost of company that is the normal salary if the info is not given in data calculate and give  now when you asked about the navigating the page like i want to go enter some website or somethig to go through a website then refer {nav} which contains a list of address so just ping the address and give them where so see them as well"},
]
    messages.append({"role": "user", "content": message})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,)
    reply = chat.choices[0].message.content
    
    await cl.Message(reply).send()
    
@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
        # Creating Recogniser() class object
    recog1 = spr.Recognizer()

    # Creating microphone instance
    mc = spr.Microphone()

    # Translator method for translation
    translator = Translator()

    

    with mc as source:
        if settings["Model"] == "Punjabi":
    # you will speak hindi
            from_lang = 'pa'
            to_lang = 'en'
            await cl.Message(content="Speak a stentence... | ਇੱਕ ਸਟੈਂਟ ਬੋਲੋ...").send()
            # await cl.Message(content="").send()
            print("Speak a stentence...")
            recog1.adjust_for_ambient_noise(source, duration=0.2)

            audio = recog1.listen(source)
            get_sentence = recog1.recognize_google(audio)
            translated=punjabi_trans(get_sentence)
        
        if settings["Model"] == "Hindi":
            # you will speak hindi
            from_lang = 'hi'
            to_lang = 'en'
            await cl.Message(content="Speak a stentence... | एक आभास बोलो ... ").send()
            # await cl.Message(content="").send()
            print("Speak a stentence...")
            # recog1.adjust_for_ambient_noise(source, duration=0.2)
            audio = recog1.listen(source)
            get_sentence = recog1.recognize_google(audio)
            translated=hindi_trans(get_sentence)
        
        
        # Using recognize.google() method to
        # convert audio into text
        
        await cl.Message(content=f"Transcribed text: {translated}").send()
        # Using try and except block to improve
        # its efficiency.
        try:
            
            # Printing Speech which need to 
            # be translated.
            print("Phase to be Translated :"+ get_sentence)

            # Using translate() method which requires 
            # three arguments, 1st the sentence which
            # needs to be translated 2nd source language
            # and 3rd to which we need to translate in 
            text_to_translate = translator.translate(get_sentence, 
                                                    src= from_lang,
                                                    dest= to_lang)
            
            # Storing the translated text in text 
            # variable 
            text = text_to_translate.text 
            print(text)
            message=text
            today = date.today()
            messages = [
            {"role": "system", "content": f"{today} is the current date You are a helpful assistant to assist users from the information given the information is {df} and this is your realtime data and you are asked to reply based on the data provided and dont say something like i dont have or i am not aware or without complete information i cant dont say like that now when they ask something like ctc then it means cost of company that is the normal salary if the info is not given in data calculate and give"},
        ]
            messages.append({"role": "user", "content": message})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,)
            reply = chat.choices[0].message.content
            
            await cl.Message(reply).send()

            speak = gTTS(text=text, lang=to_lang, slow= False) 

            # Using save() method to save the translated 
            # speech in capture_voice.mp3
            speak.save("captured_voice.mp3")	 
            
            # Using OS module to run the translated voice.
            os.system("start captured_voice.mp3")

        # Here we are using except block for UnknownValue 
        # and Request Error and printing the same to
        # provide better service to the user.
        except spr.UnknownValueError:
            print("Unable to Understand the Input")
            
        except spr.RequestError as e:
            print("Unable to provide Required Output".format(e))



# @cl.on_message
# async def main(message: str):
#     """Records audio from the microphone and transcribes it.

#     Args:
#         message: The message containing the audio recording.

#     Returns:
#         None.
#     """
    
#     while True:
#         r = sr.Recognizer()
#         with sr.Microphone() as source:
#             audio = r.listen(source)

#         try:
#             transcribed_text = r.recognize_google(audio)
#             await cl.Message(content=f"Transcribed text: {transcribed_text}").send()
#             break
#         except:
#             pass

# @cl.on_chat_start
# async def main():
#     pass

# if __name__ == "__main__":
#     cl.run()