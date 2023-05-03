import speech_recognition as sr

def tuvasta_hääl(mikrofoni_salvestus):
    # Initialize recognizer class (for recognizing the speech)

    r = sr.Recognizer()

    audioFile = sr.AudioFile(mikrofoni_salvestus)

    # Reading AudioFile as source

    with audioFile as source:
        #recognizer.adjust_for_ambient_noise(source)
        audio_text = r.record(source)

        #audio_text = r.adjust_for_ambient_noise(source)

        # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            whole_thing = r.recognize_google(audio_text, language="et", show_all=True)
            return whole_thing
            #for transcript in whole_thing['alternative']:
                #return(transcript)
            # print("Text: "+ whole_thing)
        except:
            print("Sorry, I did not get that")

#print(voice_input())