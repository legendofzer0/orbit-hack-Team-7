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
    
    # Adding intents and diverse phrases
    manager.add_intent("on the fan", [
        "turn on the fan", "fan on", "start the fan",
        "activate the fan", "enable the fan",
        "switch on the fan", "power on the fan"
    ])
    
    manager.add_intent("off the fan", [
        "turn off the fan", "fan off", "stop the fan",
        "deactivate the fan", "disable the fan",
        "switch off the fan", "power off the fan"
    ])
    
    manager.add_intent("on the light", [
        "turn on the light", "light on", "start the light",
        "activate the light", "enable the light",
        "switch on the light", "power on the light"
    ])
    
    manager.add_intent("off the light", [
        "turn off the light", "light off", "stop the light",
        "deactivate the light", "disable the light",
        "switch off the light", "power off the light"
    ])
    
    manager.add_intent("motion sensor", [
        "check the room", "activate motion sensor",
        "start motion detection", "detect motion",
        "motion sensor on", "turn on motion sensor"
    ])
    
    return manager.get_data()
