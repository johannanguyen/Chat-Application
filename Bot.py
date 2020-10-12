import random
import requests

class Bot:
    def __init__(self, input_data):
        self.input_data = input_data

    def bot_action(self):
        input_data = self.input_data
        #input_data["new_username"] = "DEXTER"
        
        if (input_data["new_message"] == "!!about"):
            print("Function entered !!about")
            input_data['new_message'] = "This is the best chat ever"
            print("TEST: ", input_data)
            return input_data['new_message']
                
        elif (input_data["new_message"] == "!!pokemon"):
            poke_num = random.randint(1, 300)
            api_link = f"https://pokeapi.co/api/v2/pokemon/{poke_num}"
            poke_data = requests.get(api_link)
            pack_data = poke_data.json()
            poke_name = pack_data['species']['name']
            poke_type = pack_data['types'][0]['type']['name']
            print(poke_name, poke_type)
            
            input_data['new_message'] = poke_name + " is a " + poke_type + " pokemon! :)"
            return input_data['new_message']
                
        elif (input_data["new_message"] == "!!mood"):
            moods = [ "I'm feeling happy.",
                    "I'm feeling sleepy.",
                    "I'm feeling awkward.",
                    "I'm feeling lovely.",
                    "I'm feeling hungry.",
                    "I'm feeling evil.",
                    "I'm feeling bored.",
                    "I'm feeling lazy....."]
            input_data['new_message'] = random.choice(moods)
            return input_data['new_message']
                
        elif (input_data["new_message"] == "!!help"):
            input_data['new_message'] = "Select from one of these: !!about -  !!funtranslate [message] - !!mood -  !!pokemon - !!help"
            return input_data['new_message']
                
        elif (input_data["new_message"].split()[0] == "!!funtranslate"):
            phrase= input_data["new_message"][15:]
            api_link = f"https://api.funtranslations.com/translate/doge.json?text={phrase}"
            doge_data = requests.get(api_link)
            pack_data = doge_data.json()
            translated = pack_data['contents']['translated']
            input_data['new_message'] = translated
            
            return input_data['new_message']
            
        else:
            input_data['new_message'] = "Sorry, that is not a valid command. :/"
            return input_data['new_message']