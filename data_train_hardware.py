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
    
    manager.add_intent("on the fan", [
        "",
        
    ])
    
    manager.add_intent("off the fan", [
        "",
        
    ])

    return manager.get_data()
