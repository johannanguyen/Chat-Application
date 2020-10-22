import random
import requests

class Bot:
    def __init__(self, input_data):
        self.input_data = input_data

    def bot_action(self):
        input_data = self.input_data
        
        if (input_data["new_message"] == "!!about"):
            print("Function entered !!about")
            input_data['new_message'] = "Hey! I'm Dexter, here to help you along your journey to become a Pokemon master!"
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
                
        elif (input_data["new_message"] == "!!quote"):
            quotes = [ "Hey, I know. I’ll use my trusty frying pan as a drying pan. -Brock",
                    "Err...my name is...Tom Ato! -Ash",
                    "I see now that one’s birth is irrelevant. It’s what you do that determines who you are. -Mewtwo",
                    "A Caterpie may change into a Butterfree, but the heart that beats inside remains the same. -Brock",
                    "There’s no sense in going out of your way to get somebody to like you. -Ash",
                    "It's following Pikachu around like its a streaker or something. -Ash",
                    "A wildfire destroys everything in its path. It will be the same with your powers unless you learn to control them. -Giovanni",
                    "Take charge of your destiny. -Rayquaza",
                    "I’m totally unprepared to deal with life’s realities. -Meowth"]
                    
            input_data['new_message'] = random.choice(quotes)
            return input_data['new_message']
                
        elif (input_data["new_message"] == "!!help"):
            input_data['new_message'] = "Select from one of these: !!about !!funtranslate [message] !!quote !!pokemon !!help"
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