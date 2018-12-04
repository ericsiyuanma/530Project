import speech_recognition as sr2
from os import path
import string
import sys
import ac_encode as ac
import pyaudio
from compare_pitch import compare_pitch_function
from compare_pitch import calculate_entropy
from readpitch import read_pitch

def main():
    choice = input(
        "Press 1 for live mic input, press 2 for file name, press 3 for comparison of two files, press 4 for comparison of two mic inputs ")
    r = sr2.Recognizer()
    if choice == "1":
        with sr2.Microphone() as source:
            print("Please say your password ")
            audio = r.listen(source)
            with open("microphone-result1.wav", "wb") as f:
                f.write(audio.get_wav_data())
            try:
                message = r.recognize_google(audio)
                lowerbound = len(
                    ac.encode(str(ac.concat_list(ac.tobits(message))), 10, 1))
                print("We think you said '{0}' was your password ".format(
                    message))
                print(
                    "The entropy of the said password given is: {0} bits ".format(
                        lowerbound))
                read_pitch("microphone-result1.wav")
            except sr2.UnknownValueError:
                print("Could not understand audio")
            except sr2.RequestError as e:
                print("Could not get results from google; {0}".format(e))
    elif choice == "2":
        filename = input("What is the name of the sound file? ")
        audiofile = path.join(path.dirname(path.realpath(__file__)), filename)
        with sr2.AudioFile(audiofile) as source:
            audio = r.record(source)
        try:
            message = r.recognize_google(audio)
            lowerbound = len(
                ac.encode(str(ac.concat_list(ac.tobits(message))), 10, 1))
            print("We think the file said '{0}' was your password ".format(
                message))
            print("The entropy of the audio file given is: {0} bits ".format(
                lowerbound))
            read_pitch(audiofile)
        except sr2.UnknownValueError:
            print("Could not understand audio")
        except sr2.RequestError as e:
            print("Could not get results from google; {0}".format(e))

    elif choice == "3":
        file1 = input("What is the name of the first file? ")
        file2 = input("What is the name of second file? ")
        audiofile1 = path.join(path.dirname(path.realpath(__file__)), file1)
        audiofile2 = path.join(path.dirname(path.realpath(__file__)), file2)
        with sr2.AudioFile(audiofile1) as source1:
            with sr2.AudioFile(audiofile2) as source2:
                audio1 = r.record(source1)
                audio2 = r.record(source2)
            try:
                message1 = r.recognize_google(audio1)
                message2 = r.recognize_google(audio2)
                if message1 == message2:
                    print(
                        "Congrats your passwords match. It has an entropy of: {0} bits ".format(
                            ac.encode(message1, 10, 1)))
                else:
                    print(
                        "The two messages given were: '{0}' and '{1} with respective entropies: '{2}','{3}' ".format(
                            message1, message2, len(ac.encode(
                                str(ac.concat_list(ac.tobits(message1))), 10,
                                1)),
                            len(ac.encode(
                                str(ac.concat_list(ac.tobits(message2))), 10,
                                1))))
                compare_pitch_function(message1, message2, audiofile1, audiofile2, 0.05)

            except sr2.UnknownValueError:
                print("Could not understand audio")
            except sr2.RequestError as e:
                print("Could not get results from google; {0}".format(e))
    elif choice == "4":
        with sr2.Microphone() as source:
            print("Please say your password ")
            audio1 = r.listen(source)
            with open("microphone-result1.wav", "wb") as f:
                f.write(audio1.get_wav_data())
            print("Please say it again ")
            audio2 = r.listen(source)
            with open("microphone-result2.wav", "wb") as f:
                f.write(audio2.get_wav_data())
            try:
                message1 = r.recognize_google(audio1)
                message2 = r.recognize_google(audio2)
                lowerbound1 = len(
                    ac.encode(str(ac.concat_list(ac.tobits(message1))), 10, 1))
                lowerbound2 = len(
                    ac.encode(str(ac.concat_list(ac.tobits(message2))), 10, 1))
                if message1 == message2:
                    print(
                        "We think you said '{0}' both times. Your password has an entropy of: '{1}'".format(
                            message1,
                            lowerbound1))
                    calculate_entropy(lowerbound1)

                else:
                    print(
                        "We heard you say '{0}' and then '{1}'. These do not match and have respective entropies: "
                        "'{2}' bits and '{3}' bits ".format(
                            message1, message2, lowerbound1, lowerbound2))
                compare_pitch_function(message1, message2, "microphone-result1.wav",
                                       "microphone-result2.wav", 0.05)
            except sr2.UnknownValueError:
                print("Could not understand audio")
            except sr2.RequestError as e:
                print("Could not get results from google; {0}".format(e))


if __name__ == "__main__":
    main()
