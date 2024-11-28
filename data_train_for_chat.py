class Intent:
    def __init__(self, name, phrases):
        self.name = name
        self.phrases = phrases

class IntentManager:
    def __init__(self):
        self.intents = []

    def add_intent(self, name, phrases):
        self.intents.append(Intent(name, phrases))

    def get_data(self):
        return [{"text": phrase, "intent": intent.name} for intent in self.intents for phrase in intent.phrases]

def load_data():
    manager = IntentManager()
    
    manager.add_intent("OpenApp", [
        "Open Instagram",
        "Start Instagram",
        "Go to Instagram",
        "Launch Instagram",
        "I'd like to watch Instagram",
        "Can you open Instagram?",
        "Please open Instagram",
        "Navigate to Instagram",
        "I'd like to browse Instagram",
        "Play Instagram",
        "Access Instagram",
        "Fire up Instagram",
        "Open the Instagram website",
        "Can you start Instagram?",
        "I want to watch videos on Instagram",
        "Open YouTube",
        "Start YouTube",
        "Go to YouTube",
        "Launch YouTube",
        "I'd like to watch YouTube",
        "Can you open YouTube?",
        "Please open YouTube",
        "Navigate to YouTube",
        "I'd like to browse YouTube",
        "Play YouTube",
        "Access YouTube",
        "Fire up YouTube",
        "Open the YouTube website",
        "Can you start YouTube?",
        "I want to watch videos on YouTube",
        "Open Google",
        "Start Google",
        "Go to Google",
        "Launch Google",
        "I'd like to use Google",
        "Can you open Google?",
        "Please open Google",
        "Navigate to Google",
        "I'd like to browse Google",
        "Access Google",
        "Fire up Google",
        "Open the Google website",
        "Can you start Google?",
        "I want to search on Google",
    ])
    
    manager.add_intent("CloseApp", [
        "Close Instagram",
        "Exit Instagram",
        "Stop Instagram",
        "Shut down Instagram",
        "I'd like to close Instagram",
        "Can you close Instagram?",
        "Please close Instagram",
        "Quit Instagram",
        "Turn off Instagram",
        "End Instagram session",
        "Leave Instagram",
        "Close the Instagram website",
        "Close YouTube",
        "Exit YouTube",
        "Stop YouTube",
        "Shut down YouTube",
        "I'd like to close YouTube",
        "Can you close YouTube?",
        "Please close YouTube",
        "Quit YouTube",
        "Turn off YouTube",
        "End YouTube session",
        "Leave YouTube",
        "Close the YouTube website",
        "Close Google",
        "Exit Google",
        "Stop Google",
        "Shut down Google",
        "I'd like to close Google",
        "Can you close Google?",
        "Please close Google",
        "Quit Google",
        "Turn off Google",
        "End Google session",
        "Leave Google",
        "Close the Google website",
    ])

    return manager.get_data()
