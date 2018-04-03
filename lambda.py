from __future__ import print_function
import random
import json

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response_crickets_start(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak><audio src=\"https://s3.amazonaws.com/cricket-sound-for-alexa/alexa-crickets-sound.mp3\"/> " + output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_crickets_end(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak> " + output + "<audio src=\"https://s3.amazonaws.com/cricket-sound-for-alexa/alexa-crickets-sound.mp3\"/></speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# ---------------------------- Data for the skill ------------------------------

ques = ["How many species of crickets exist?",
        "Only male crickets chirp.",
        "When in groups,what are crickets called? ",
        "The hind wings of a cricket are what type? ",
        "What color crickets are not found in nature? ",
        "What type of eyes do crickets have? ",
        "Can crickets fly? ",
        "What category of consumers do crickets fall in?",
        "When do crickets lay eggs?",
        "Are male crickets chivalrous?"
        ]

opA = ["100",
       "True",
       "Orchestra",
       "Membranous",
       "Green",
       "Simple",
       "Yes",
       "Herbivores",
       "Summer",
       "Yes"
       ]

opB = ["200",
       "False",
       "Chatter",
       "Fringed",
       "Yellow",
       "Compound",
       "No",
       "Carnivores",
       "Winter",
       "No"
       ]

opC = ["500",
       "",
       "Seething",
       "Scaly",
       "Red",
       "",
       "",
       "Omnivores",
       "Spring",
       ""
       ]

opD = ["900",
       "",
       "Parade",
       "Haltere",
       "Black",
       "",
       "",
       "Decomposers",
       "Autumn",
       ""
       ]

ans = ["D",
       "A",
       "A",
       "A",
       "B",
       "B",
       "B",
       "C",
       "D",
       "A"
       ]

ansInfo = ["Our planet has about 900 different species of crickets. They all come with a short existence. And cannot live more than a year.",
           "Crickets are known for their musical chirping sounds. But only male crickets chirp. Some species of crickets are mute.",
           "",
           "Crickets have membranous hind wings. Membranous wings are easily foldable when not in use. Still there are some species that cannot fly at all.",
           "Crickets can be black, red, light brown or green in color.",
           "Crickets are said to have compound eyes and great vision. Their eyes enable them to look in different directions at one time.",
           "Even though crickets have wings, they do not fly. Crickets can jump or travel short distances by producing jerky moves.",
           "Crickets are omnivores. Their diet includes various types of insects, fungi and plant materials.",
           "Crickets lay eggs in autumn. Eggs remain incubated during the cold winter period and hatch at the beginning of spring.",
           "Male crickets are known for their chivalric attitude for their female partners who are carrying their eggs. They would protect their females, even at the expense of their own lives."
           ]

# --------------------------- Global variables ---------------------------------

totalQues = 10
quesInOneSession = 6
maxScore = quesInOneSession

score = 0
currQues = -1
askedQuesCount = 0
askedQues = []
session_attributes = {}
rulecount = 0

quesAnswered = True

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hi! This is a cricket quiz! Cricket - the insect! "\
                    "For rules of the game, just say rules! " \
                    "Shall we check your knowledge of crickets? Say start quiz to begin" 
                    
    reprompt_text = "Hey! I am waiting! " \
                    "Shall we get started? Say begin to get started!" 

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response_crickets_start(card_title, speech_output, reprompt_text, should_end_session))

def result():
    
    init = "Yay! You completed the quiz! " + " You got " + str(score) + " out of " + str(quesInOneSession) + " correct. "
    if score == quesInOneSession:
        init = init + " Perfect score! You really know crickets! Wow! "
    elif score >= (quesInOneSession/1.5)+1:
        init = init + " Great score! Keep playing, keep getting better! "
    elif score >= (quesInOneSession/2.5)+1:
        init = init + " Good effort! You will do better, next time! I believe in you! "
    else:
        init = init + " You can do better! Play again, get better!  "

    init = init + "  Wanna play again? Just say, Replay!"
    
    return (init)

def ret_question():

    q = ques[currQues] + " . "
    return (q)

def ret_options():

    o3 = ""
    o4 = ""
    
    o1 = "Option 1 . " + opA[currQues] + ". "
    o2 = "Option 2 . " + opB[currQues] + ". "

    if opC[currQues] != "":
        o3 = "Option 3 . " + opC[currQues] + ". "
        o4 = "Option 4 . " + opD[currQues] + ". "

    o = o1+o2+o3+o4
    return (o)
    

def quiz(intent, session):

    global askedQuesCount
    global currQues
    global askedQues
    global quesAnswered

    card_title = "Quiz"

    if askedQuesCount == 0:
        init = "Alright! Let us start. "
    else:
        init = ""

    speech_output = ""
    reprompt_text = ""
    
    if askedQuesCount == quesInOneSession:
         
                speech_output = result()
                reprompt_text = " Hey! Wanna play again? Say Replay to play again. Or Exit to stop playing "
                should_end_session = False

                return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
            
    if quesAnswered == False:   #I don't think this if is required either
        card_title = "Alert!"

        speech_output = "Please answer the last question I asked you."
        reprompt_text = "I am waiting for your answer! If you missed the question, say repeat question."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
             
    
    askedQuesCount = askedQuesCount+1   
    quesNo = askedQuesCount
    x =  random.randint(0,totalQues-1)
    while x in askedQues:
            x =  random.randint(0,totalQues-1)
        
    askedQues.append(x);
    currQues = x
    
    question = "Question " + str(quesNo) + ".  " + ret_question() 
    options = "Your options are. " + ret_options()
    
    session_attributes['question'] = ques[x]
    session_attributes['options']= options
    
    quesAnswered = False
    
    speech_output = init + question + options
    reprompt_text = ""

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    

def convert(val):

    if val == '1':
        val = "A"
    elif val == '2':
        val = "B"
    elif val == '3':
        val = "C"
    elif val == '4':
        val = "D"
    else:
        val = "E"

    return val    
    
def convertRev(val):

    if val == "A":
        val = "1"
    elif val == "B":
        val = "2"
    elif val == "C":
        val = "3"
    else:
        val = "4"

    return val    

def get_answer(intent, session):

    global score
    global quesAnswered

    card_title = "Answer"

    if quesAnswered == True:    # -- only for last ques
        speech_output = "You have already answered this question, buddy."
        reprompt_text = "" #I don't think this if is required.

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

        
    correctAns = ans[currQues]

    if 'value' not in intent['slots']['option']:
        speech_output = "You need to select an option! Select an option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
        
    ans_input = intent['slots']['option']['value']
    ans_input = convert(ans_input)

    if ans_input == "E":
        speech_output = "You need to select a valid option! Select a valid option."
        reprompt_text = "If you missed the options, say repeat options."

        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

    if ans_input == correctAns:
        speak = "That is the correct answer! "
        score = score + 1
    else:
        speak = "That answer is incorrect. The correct answer is option " + convertRev(correctAns) + ". "

    session_attributes['score'] = score
    quesAnswered = True
    
    speech_output = speak + ansInfo[currQues]
    
    b = quiz(intent,session)
    ques = b['response']['outputSpeech']['text']
    
    speech_output = speech_output + " . \n" + ques
    reprompt_text = "I am waiting for your answer. If you missed the question, say repeat question!" 
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def repeat_question(intent, session):

    card_title = "Question"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    if quesAnswered == True:            #I don't think this if will be required either -- only for last ques
        speak = "Your question was. "
        re = "Wanna play again? Say replay." 
    else:
        speak = "Your question is. "
        re = "Hey. I am waiting for your answer." 

    speech_output = speak + ret_question() + " . Options.  " + ret_options()
    reprompt_text = re
    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    

def repeat_options(intent, session):

    card_title = "Option"

    if currQues == -1:
        speech_output = "The quiz has not started yet! Say begin to start the quiz"
        reprompt_text = "Say begin to start the quiz"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
    
    
    if quesAnswered == True:                #I don't think this if will be required either -- only for last ques
        speak = "Your options were. "
        re = "Wanna play again? Say replay." 
    else:
        speak = "Your options are. "
        re = "Hey. I am waiting for your answer."

    speech_output =  speak + ret_options()
    reprompt_text = re

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def current_score(intent, session):

    card_title = "Score"

    sc = str(score)
    if askedQuesCount == quesInOneSession:
        speak = "You finished the quiz! You final score is "+ sc + ". Say, replay to play again."
        re = "Say replay to start the quiz again! Or say exit to exit the game"
    else:
        if quesAnswered == True:    # this if will not be required either -- only for last ques
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount) + " questions."
            re = "Wanna play again? Say replay."
        else:
            speak = "Your score is " + sc + " because you have answered " + sc + " correctly, out of " + str(askedQuesCount-1) + " questions."
            re = "I am waiting for your answer! Say, repeat question, if you want me to repeat the question."

    speech_output = speak
    reprompt_text = re
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    


def replay_quiz(intent, session):
    
    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered
    
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    session_attributes = {}
    quesAnswered = True
    
    return quiz(intent, session)    


def no_response():

    card_title = "No!"
    
    speech_output = "I am sorry, I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    
	
	
def yes_response():

    card_title = "Yes!"
    
    speech_output = "Yes yes but I don't understand!"
    reprompt_text = "For rules, say rules!"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))    

    
def get_help_response():
    
    global rulecount
    
    card_title = "Help"
    
    rulecount = rulecount + 1
    if rulecount == 1:
        speech_output = "This is a quiz about crickets and the rules are simple. " \
                        "I will ask you a question. You choose your answer, by saying, Option 1, or, Option 2, etc.. "\
                        "I will tell you, if you were correct. "
    else:
        speech_output = "Hi! Welcome to I Know Cricket - The Insect! " \
                        "This is quiz about crickets and the rules are simple. " \
                        "After you start the quiz, you will be prompted with a question. "\
                        "Options for the same will be provided. You have to choose one option, by saying, Option 1, or, Option 2, or, Option 3, or, Option 4. " \
                        "After you answer the question, I will tell you, whether you were right, or not. "\
                        "You can get a question repeated, by saying, Repeat question. You can also get the options for a question, repeated, by saying, repeat options. "\
                        "You can also know more about the answer, of a question, by saying, tell me more. "\
                        "You will be asked 6 questions. You will get the final score after the game. To get your score between the game, you can ask, what is my score. "
        rulecount = 0                

    if askedQuesCount == 0:
        speech_output = speech_output + "That's all! We're all set to begin! Say begin to get started!"
    else:
        speech_output = speech_output + "Alright! Shall we continue? Say begin to continue!"
                    
    speech_output = speech_output + " For detailed rules, say rules again. "
    reprompt_text = "Hey there! What are you waiting for? " \
                    "Say begin!"
                    
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():

    card_title = "Session Ended"
    speech_output = "I hope you had fun! " \
                    " Goodbye!"
    
    should_end_session = True
    
    return build_response({}, build_speechlet_response_crickets_end(card_title, speech_output, None, should_end_session))
		
		

# --------------- Events ------------------

def on_session_started(session_started_request, session):

    global score
    global currQues
    global askedQuesCount
    global askedQues
    global quesAnswered

    session_attributes = {}
    score = 0
    currQues = -1
    askedQuesCount = 0
    askedQues = []
    quesAnswered = True

def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent)
    
    if intent_name == "QuizIntent":
        return quiz(intent, session)
    elif intent_name == "AnswerIntent":
        return get_answer(intent, session)
    elif intent_name == "RepeatQuestionIntent":	
        return repeat_question(intent, session)
    elif intent_name == "RepeatOptionsIntent":
        return repeat_options(intent, session)
    elif intent_name == "ReplayIntent":
        return replay_quiz(intent, session)
    elif intent_name == "WhatsMyScoreIntent":
        return current_score(intent, session)
    elif intent_name == "NoIntent":
        return no_response(intent, session)
    elif intent_name == "YesIntent":
        return yes_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        
def on_session_ended(session_ended_request, session):
    session_attributes = {}

# --------------- Main handler ------------------

session_attributes = {}

def lambda_handler(event, context):
    
    if event['session']['new']:
	    on_session_started({'requestId': event['request']['requestId']},event['session'])
		
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

