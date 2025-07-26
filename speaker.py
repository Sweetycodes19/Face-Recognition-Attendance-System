
import pythoncom
from win32com.client import Dispatch

def speak(text):
    try:
        pythoncom.CoInitialize()
        speaker = Dispatch("SAPI.SpVoice")
        speaker.Speak(text)
    except:
        pass  
