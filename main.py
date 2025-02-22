from tkinter import *
from playsound import playsound
import yfinance as YF
import wikipedia
import pyttsx3
import requests
from PIL import ImageTk, Image

root = Tk()
root.title("Chat Bot")
# root.maxsize(844, 744)
root.minsize(root.winfo_screenwidth()-150, root.winfo_screenheight()-150)

# Some predefined things
num = 0
userMessages = 0
# Dictionary for chatBot
dictQA = {'How are u': 'I am fine',
          'How old are u': 'I am 16',
          'Who are u': 'I am your assistant',
          'Hi': 'Hello',
          "what's up": "I am good",
          'hello': 'hi'}
voice = False

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "city": response.get("city"),
        "country": response.get("country")
        }
    return location_data

def getweather():
    loc = get_location()
    city = loc.get("city")
    country = loc.get("country")
    url = 'https://wttr.in/?format=1'
    res = requests.get(url)
    temperature = res.text.split()
    try:
        displayBotMessage(f"The current temperature of {city}, {country} is {temperature[1]}")
    except Exception as e:
        displayBotMessage("Weather not available for this city")

def careerInterest(interest):
    if interest.lower()=="science":
        displayBotMessage("Engineering, Doctor")
    elif interest.lower()=="commerce":
        displayBotMessage("CA")
    elif interest.lower()=="humanities":
        displayBotMessage("IAS, Laywer")
    else:
        displayBotMessage("There are only 3 streams available")

def subOptions(subChoice):
    subScience = ["physics", "chemistry", "maths", "biology"] 
    subCommerce = ["accounts", "economics", "business-studies"] 
    subArts = ["history", "political-science"] 

    if subChoice in subScience:
        displayBotMessage("Your interest is science")
        careerInterest("Science")
    elif subChoice in subCommerce:
        displayBotMessage("Your interest is commerce")
        careerInterest("Commerce")
    elif subChoice in subArts:
        displayBotMessage("Your interest is arts")
        careerInterest("Humanities")
    else:
        print("Your interest is nowhere")

def fetchWiki(query):
    try:
        displayBotMessage(wikipedia.summary(
            wikipedia.search(query)[0], sentences=1)[0:120]+"...")
    except Exception as e:
        displayBotMessage("Try asking something else")


def changeTheme(themeColor):
    global messageFrame
    global userFrame
    if themeColor == "dark":
        messageFrame.configure(bg="black")
        userFrame.configure(bg="black")
        displayBotMessage("Theme changed to dark mode")
    elif themeColor == "light":
        messageFrame.configure(bg="light grey")
        userFrame.configure(bg="light grey")
        displayBotMessage("Theme changed to light mode")
    else:
        displayBotMessage("Theme not found")


def playBeep():
    path = "audio/beep.wav"
    playsound(path)


def displayUserMessage(t):
    global messageFrame
    display = Label(messageFrame, text=t, font=("calibri", 15, "bold"),
                    foreground="black", background="pink", padx='5', pady='5')
    display.pack(anchor="e", pady="10", padx="10")
    playBeep()

def on_click(event=None):
    global voice
    voice = not voice


def displayBotMessage(t):
    global messageFrame
    display = Label(messageFrame, text=t, font=("calibri", 15),
                    foreground="black", background="light green", padx='5', pady='5')
    display.pack(anchor="w", pady="10", padx="10")
    if voice:
        engine = pyttsx3.init()
        engine.say(t)
        engine.runAndWait()


def fetchStockPrice(ticker):
    try:
        cmp = round(YF.Ticker(ticker.upper()).info['regularMarketPrice'], 2)
        displayBotMessage(f"The stock price of {ticker.upper()} is {cmp}.")
    except Exception as e:
        displayBotMessage(
            "Invalid stock ticker entered or there is some problem with ur internet connection")


def enter_key(event):
    answer()

# creating a bot answer function


def answer():
    global userMessages
    global qText
    global display
    userEntry = chat_entry.get().lower().strip()
    if userEntry != "":
        matchFound = False
        displayUserMessage(chat_entry.get().strip())
        if userMessages == 0:  # user entered his name
            displayBotMessage(f"Hi {userEntry.capitalize()}")
            # displayBotMessage('Try asking me some questions like "What is the stock price of <ticker>"')
            userMessages = 1
        else:
            # Some Custom Functions
            if "stock price" in userEntry:
                words = userEntry.split()
                fetchStockPrice(words[len(words)-1])
                matchFound = True
            elif "theme" in userEntry:
                themeColor = userEntry.split()[-1]
                # print(themeColor)
                changeTheme(themeColor)
                matchFound = True
            elif "temperature" in userEntry or "weather" in userEntry:
                getweather()
                matchFound = True
            elif "career interest" in userEntry:
                careerInterest(userEntry.split()[-1])
                matchFound = True
            elif "career subchoice" in userEntry:
                subOptions(userEntry.split()[-1])
                matchFound = True
            else:
                for i in dictQA.keys():
                    if i.lower() in userEntry:  # if message exists in dictionary
                        displayBotMessage(dictQA[i].capitalize())
                        matchFound = True
            if matchFound == False:
                fetchWiki(chat_entry.get().strip())

    # when messages are filled up
    clear = True
    if userMessages == 4:
        clear_frame()
        displayBotMessage("Screen cleared up!")
        userMessages = 0
        clear = False
    userMessages += 1
    if clear == True:
        chat_entry.delete(0, END)
    else:
        answer()
    # print(userMessages)


def clear_frame():
    global messageFrame
    for widgets in messageFrame.winfo_children():
        # print(widgets.winfo_name())
        if (widgets.winfo_name() != "!label"):
            widgets.destroy()


# creating message frame
messageFrame = Frame(root, bg="light grey")
messageFrame.pack(fill=BOTH, expand=True)
# place header
img = PhotoImage(file="img/header.png")
photoimage = img.subsample(3, 3)
Label(messageFrame, image=photoimage).pack(
    side=TOP, anchor="w", padx=10, pady=10)

# display first question
displayBotMessage("What is your name?")

# USER FRAME
userFrame = Frame(root, bg="light grey")
userFrame.pack(side=BOTTOM, fill="x")

# Displaying the button
button = Button(userFrame, text="SEND", font=("calibri", 13, "bold"),
                foreground="black", background="yellow", command=answer)
button.pack(side="bottom", pady=(0, 10))
#Display
image = Image.open("img/speaker_on.png")
photo = ImageTk.PhotoImage(image)
b = Button(userFrame, image=photo, command=on_click)
b.pack(after=button, side="right")

# creating a user input entry
chat_var = StringVar()
chat_entry = Entry(userFrame, textvariable=chat_var, font=(
    'calibri', 15, 'italic'), highlightthickness=1)
chat_entry.config(highlightbackground="red", highlightcolor="red")
chat_entry.pack(side="bottom", fill="x", pady=5, padx=5)

# binding enter key with a function
root.bind('<Return>', enter_key)

root.mainloop()
