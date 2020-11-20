# CS 421: Natural Language Processing
# University of Illinois at Chicago
# Fall 2020
# Chatbot Project - Evaluation
#
# Do not rename/delete any functions or global variables provided in this template and write your solution
# in the specified sections. Use the main function to test your code when running it from a terminal.
# Avoid writing that code in the global scope; however, you should write additional functions/classes
# as needed in the global scope. These templates may also contain important information and/or examples
# in comments so please read them carefully.
# =========================================================================================================

# Import any necessary libraries here, but check with the course staff before requiring any external
# libraries.
import re
import random
from collections import defaultdict

dst = defaultdict(list)
# State transitions are defined as a dictionary with key = to initial state and value = to a dictionary{ key is transition ("yes" or "no"): value is next state}
state_transition = { 
    "greeting": {"yes": "activity_check_in", "no" : "end"},
    "activity_check_in": {"yes": "next_activity","no":"ability_check_in"}, 
    "ability_check_in": {"yes":"next_activity", "no": "sub_activity"},
    "sub_activity": {"yes": "activity_check_in", "no": "finish_check_in"},
    "next_activity": {"yes": "activity_check_in", "no": "finish_check_in"},
    "finish_check_in": {"yes": "end", "no": "next_activity"},
    "end": {"yes" : "terminate", "no": "terminate"}
     #end state does not have a tansition, will be marker for end
}

# The slot for this will be:
states = ["greeting", "activity_check_in","ability_check_in", "sub_activity", "next_activity", "finish_check_in", "end","dialogue_state_history"]
# activity_queue = ["bed","sit_up","teeth","walk_around","shower","wash_face"]
activity_queue = ["bed","sit_up","teeth","walk_around"]
current_activity = "bed"
#https://www.powerthesaurus.org/yes/synonyms
yes_words = ["yes","yeah", "yee", "yeet", "ya", "yah", "yey", "yay", "yep", "yup","ok", "okey", "okey-doke","okay", "sure", "will do", "alright", "absolutely", 
             "indeed", "affirmative", "certainly", "aye", "very well", "all right", "of course", "roger", "righto", "uh-huh"]

#https://www.powerthesaurus.org/no/synonyms
no_words = ["yesn't", "negative", "nix", "refuse", "no", "nope", "nah", "na", "not", "never", "negative", "nay", "nae", "naw", "can't", "cannot", "wont", "wouldn't", "shant"]

# State                             Permissible values              Description
# ----------------------            ---------------------           -----------------------------------------------------------------
# "greeting"                        String                          Will store the emotional state of user
# "activity_check_in"               String, list of Strings         Will store the activity that was checked in, answer if yes or no after
# "ability_check_in"                String                          Will store the user answer of yes or no for feeling able to do activity
# "sub_activity"                    String, list of Strings         Will store the subactivity as the activity to check in, yes or no
# "next_activity"                   String, list of Strings         Will store the activity as the activity to check in, yes or no
# "finish_check_in"                 String                          yes or no for going to check in
# "end"                             list of Strings                 List of all accomplishments
# "dialogue_state_history"          list of Strings                 List of all visited states
def check_yes_input(input=""):

    for yes_word in yes_words:
        if yes_word in input:
            return True

    return False 
def check_no_input(input=""):

    for no_word in no_words:
        if no_word in input:
            return True

    return False

def ask_again():
    print("Im sorry I did not understand. Is that a yes or no?")
    user_input = input()

    user_input = user_input.lower()

    if(check_yes_input(user_input)):
        return "yes"
    elif(check_no_input(user_input)):
        return "no"
    else:
        return "unsure"


def get_next_activity():
    global activity_queue
    #if lenght of list of activites is greater than zero there is an element
    if len(activity_queue) > 0:
        # pop the first activity
        activity = activity_queue.pop(0)
    return activity


# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):
    global current_activity
    # lower case input incase of capital letter yes/no sentiment
    input = input.lower()
    # Dummy code for sample output (delete or comment out when writing your code!):
    slots_and_values = []
    
    # To narrow the set of expected slots, you may (optionally) first want to determine the user's intent,
    # based on what the chatbot said most recently.

    if "dialogue_state_history" in dst and len(dst["dialogue_state_history"]) > 0:
            current_state = dst["dialogue_state_history"][0]

            if check_yes_input(input):
                slots_and_values.append((current_state,"yes")) 
            elif check_no_input(input):
                slots_and_values.append((current_state,"no"))
            else:
                answer = ask_again()
                while answer == "unsure":
                    answer = ask_again()
                slots_and_values.append((current_state, answer))

            if current_state == "activity_check_in":
                slots_and_values.append((current_state, current_activity))
            
            if current_state == "sub_activity":
                current_activity = get_next_activity()
                slots_and_values.append((current_state, current_activity))

            if current_state == "next_activity":
                current_activity = get_next_activity()
                slots_and_values.append((current_state, current_activity))
            if current_state == "end":
                slots_and_values.append((current_state, "yes"))
        # TODO add remaining states
        #states = ["greeting", "activity_check_in","ability_check_in", "sub_activity", "next_activity", "finish_check_in", "end","dialogue_state_history"]

    return slots_and_values

# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
    global dst

    for key, value in input:
        #check if key is a valid state
        if key in states:

            # Check if the key is dialogue_state_history
            if key == "dialogue_state_history":
                #checking if value is a string
                if isinstance(value, str):                        
                    dst[key].insert(0,value)
                #checking if value is a list
                elif isinstance(value, list):
                    # check if all elements in list of strings is valid state
                    test = [elem for elem in value if elem in states] 
                    # if test list is same as value list it means all values are valid state inputs
                    if test == value:
                        # add the state to dialogue tracker
                        for val in value:
                            dst[key].insert(0,val)
                    else:
                        print("dialogue_state_history: Invalid list of dialogue states changing to empty list")  
                        dst[key] = []
                else:
                    print("Incorrect state to add to state history changing to empty list")
                    dst[key] = []
            # if key is valid
            elif key in states: 
                #checking if value is a string
                if isinstance(value, str):                        
                    dst[key].append(value)
                #checking if value is a list
                elif isinstance(value, list):
                    # check if values in list are strings
                    for val in value:
                        if isinstance(val, str):
                            dst[key].append(val)
                else:
                    print("{} : Invalid data type for input making slot empty".format(key))
                    dst[key] = ""
        else:
            print("Invalid Key")
    return

# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):

    dummy_state = defaultdict(list)

    # Check if slot is empty
    if slot == "":
        return dst # return full dialogue state dictionary if slot is empty
    # Check is slot is a valid dialogue state key
    elif slot in states:
        # Check if there exists something in this slot
        if bool(dst[slot]):
            dummy_state[slot] = dst[slot]   # if yes then set dummy state of slot to that value
            return dummy_state              # return the dummy state
        else:
            print("Slot is empty")          # if slot empty print message
            return                          # return nothing if slot empty
    # If slot not empty or valid state then invalid slot
    else:
        print("slot provided is invalid")   # message that slot is invalid
        return                              # if slot invalid, return nothing


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list of no (slot, value) pairs
#          are needed).
def dialogue_policy(dst=[]):
    global current_activity
    next_state = ""
    slot_values = []
    if dst:
        if "dialogue_state_history" in dst and len(dst["dialogue_state_history"]):
            # check dialogue history, and get most recent state
            last_state = dst["dialogue_state_history"][0]

            if last_state == "end":
                next_state = "terminate"
                slot_values = []
            else:
                # get the transition rule for most recent state
                transition = state_transition[last_state]

                # get the slot values for the state in dialogue state dictionary
                status = dst[last_state]

                # if there is a yes string in status of recent state then use yes transition
                if "yes" in status:
                    next_state = transition["yes"]
                # otherwise use no transition
                elif "no" in status:
                    next_state = transition["no"]

                dst["dialogue_state_history"].insert(0,next_state)
                slot_values = []
    else:
        next_state = "greeting"
        slot_values = []
        update_dst([("dialogue_state_history", "greeting")])
    return next_state, slot_values
	
# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
# states = ["greeting", "activity_check_in","ability_check_in", "sub_activity", "next_activity", "finish_check_in", "end","dialogue_state_history"]
def nlg(state, slots=[]):
    global current_activity
    # Dummy code for sample output (delete or comment out when writing your code!):
    templates = defaultdict(list)

    # activity_queue = ["bed","sit_up","teeth","walk_around","shower","wash_face"]

    # Build at least two templates for each dialogue state that your chatbot might use.
    templates["greeting"] = []
    templates["greeting"].append("Hello. I am your Buddy here to help you track your goals. You ready to start?")
    templates["greeting"].append("Good morning :) I am Buddy. I am your friend and daily helper. Should we get started?")
    
    templates["activity_check_in_bed"] = []
    templates["activity_check_in_bed"].append("Have you gotten out of bed yet?") 
    templates["activity_check_in_bed"].append("Have you left your bed today?") 

    templates["activity_check_in_teeth"] = []
    templates["activity_check_in_teeth"].append("Have you brushed your teeth yet?") 
    templates["activity_check_in_teeth"].append("Have you brushed your teeth today?") 
    
   # templates["activity_check_in_shower"] = []
   # templates["activity_check_in_shower"].append("Have you showered yet?") 
   # templates["activity_check_in_shower"].append("Have you showered today?") 

    # TODO write out the rest of the ability check in for subactivity and for regular activities
    templates["ability_check_in_bed"] = []
    templates["ability_check_in_bed"].append("Do you feel able to get out of bed?")
    templates["ability_check_in_bed"].append("Are you able to get out of bed?")

    templates["ability_check_in_teeth"] = []
    templates["ability_check_in_teeth"].append("Are you able to go brush you teeth?") 
    templates["ability_check_in_teeth"].append("Do you feel like you could brush your teeth right now?") 

    templates["ability_check_in_walk_around"] = []
    templates["ability_check_in_walk_around"].append("Would you feel up to walking aroung your room for 5 minutes first?")
    templates["ability_check_in_walk_around"].append("Does walking around for a little before brushing your teeth seem doable?")

    templates["ability_check_in_sit_up"] = []
    templates["ability_check_in_sit_up"].append("Do you feel able to get to sit up in bed for a little while?")
    templates["ability_check_in_sit_up"].append("Are you able to sit up in bed first?")

    # TODO create the rest of the subactivity questions
    templates["sub_activity_sit_up"] = []
    templates["sub_activity_sit_up"].append("Do you want to try sitting up for 30 minutes? You could put on music, look at your phone, or anything. Then you could try getting out of bed")
    templates["sub_activity_sit_up"].append("Would you like to sit up for some time? If you do that then getting out of bed is just the next step")

    templates["sub_activity_walk_around"] = []
    templates["sub_activity_walk_around"].append("Do you want to try walking around for a few minutes? It might make it easier to walk over to brush your teeth after")
    templates["sub_activity_walk_around"].append("Would you want to walk around your room first? It maybe easier and then you could walk over to the bathroom and brush your teeth")

    # TODO determine if this is a necessary state
    templates["next_activity"] = []
    templates["next_activity"].append("Do you want to move on to the next goal?")
    templates["next_activity"].append("Should we move on to the next activity?")

    templates["finish_check_in"] = []
    templates["finish_check_in"].append("Would you like to stop for today?")
    templates["finish_check_in"].append("You ready to finish up?")

    templates["end"] = []
    templates["end"].append("I am so proud of you for trying today.")
    templates["end"].append("Great job! You accomplished as much as you could.")

    # When you implement this for real, you'll need to randomly select one of the templates for
    # the specified state, rather than always selecting template 0.  You probably also will not
    # want to rely on hardcoded input slot positions (e.g., slots[0][1]).  Optionally, you might
    # want to include logic that handles a/an and singular/plural terms, to make your chatbot's
    # output more natural (e.g., avoiding "did you say you want 1 pizzas?").
    
    # if state is activity_check_in state then slot is an activity string
    # concatenate the string to get template key
    if state == "activity_check_in" or state == "ability_check_in" or state == "sub_activity":
        # key for template is the state and current activity being checked
        template_key = state + "_" + current_activity

        # get amount of responses in state template
        amt_response = len(templates[template_key]) - 1
        response_idx = random.randint(0,amt_response)

        # output will be a random response from template of input state
        output = templates[template_key][response_idx]

        return output

    if state in templates:

        # get amount of responses in state template
        amt_response = len(templates[state]) - 1
        response_idx = random.randint(0,amt_response)

        # output will be a random response from template of input state
        output = templates[state][response_idx]

        return output
    if state == "terminate":
        return "goodbye"
    else:
        return ""
# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 chatbot.py

def main():
    
    # You can choose whether your chatbot or the participant will make the first dialogue utterance.
    # In the sample here, the chatbot makes the first utterance.
    current_state_tracker = get_dst()
   
    next_state, slot_values = dialogue_policy(current_state_tracker)
    
    output = nlg(next_state, slot_values)
    print(output)
    
    # With our first utterance complete, we'll enter a loop for the rest of the dialogue.  In some cases,
    # especially if the participant makes the first utterance, you can enter this loop directly without
    # needing the previous code block.
    while next_state != "terminate":
        # Accept the user's input.
        user_input = input()
        
        # Perform natural language understanding on the user's input.
        slots_and_values = nlu(user_input)
        
        # Store the extracted slots and values in the dialogue state tracker.
        update_dst(slots_and_values)
        
        # Get the full contents of the dialogue state tracker at this time.
        current_state_tracker = get_dst()
        
        # Determine which state the chatbot should enter next.
        next_state, slot_values = dialogue_policy(current_state_tracker)
        
        # Generate a natural language realization for the specified state and slot values.
        output = nlg(next_state, slot_values)
        
        # Print the output to the terminal.
        print(output)

        


################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()
