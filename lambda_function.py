"""
This is a Python template for Alexa to get you building skills (conversations) quickly.
"""

from __future__ import print_function
import requests


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------
def get_test_response():
    """ An example of a custom intent. Same structure as welcome message, just make sure to add this intent
    in your alexa skill in order for it to work.
    """
    session_attributes = {}
    card_title = "Test"
    speech_output = "This is a test message"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Voice Recharge Service,you want to do reacharge or you want check the balance "
    reprompt_text = "Welcome to the Voice Recharge Service, Say Hello"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_Recharge_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Recharge"
    speech_output = "Provide your 10 digit mobile number"
    reprompt_text = "Provide your 10 digit mobile number please"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


MobileNum = ""
def get_MobileRecharge_response(intent):
    global MobileNum
    session_attributes = {}
    card_title = "MobileRecharge"
    
    MobileNum = intent['slots']['MobileNumbers']['value']
    if len(MobileNum) != 10:
        speech_output = "Provide your 10 digit mobile number"
        reprompt_text = "Provide your 10 digit mobile number please"
    else:
        speech_output = "provider name "
        reprompt_text = "provider name please..!"        

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

providerNme = ""
def get_ProviderDetail_response(intent):
    global providerNme
    session_attributes = {}
    card_title = "ProviderDetail"

    providerNme = intent['slots']['provider']['value']
            
    speech_output = "Amount to recharge in rupees"
    reprompt_text = "Amount to recharge in rupees please"
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_RechargeAmount_response(intent):
    session_attributes = {}
    card_title = "RechargeAmount"
    RechargeAmt = intent['slots']['Amount']['value']
    
    dicti = {'airtel': 1, 'vodafone': 2, 'idea': 3, 'bsnl': 8, 'aircel':29, 'jio':112}
    for key,value in dicti.items():
        if providerNme == key:
            provid = value
    
    api_token = "Token"
    url = 'https://www.pay2all.in/web-api/paynow?api_token={} &number={} &provider_id={}&amount={}&client_id=123456'.format(api_token, MobileNum, provid, RechargeAmt)
    resp = requests.get(url)
    data = resp.json()
            
    speech_output = data['message']
    reprompt_text = "Thank you for details"
    
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_BalanceDetails_response():
    session_attributes = {}
    card_title = "BalanceDetails"
    
    api = 'Token'
    resp = requests.get('https://www.pay2all.in/web-api/get-balance?api_token={}'.format(api))
    data = resp.json()
    
    speech_output = 'Balance is '+ str(data['balance']) + ' rupees'
    reprompt_text = 'Not working try again...!'

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

    

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "test":
        return get_test_response()
    
    elif intent_name == 'Recharge':
        return get_Recharge_response()
        
    elif intent_name == 'MobileRecharge':
        return get_MobileRecharge_response(intent)

    elif intent_name == 'ProviderDetail':
        return get_ProviderDetail_response(intent)

    elif intent_name == 'RechargeAmount':
        return get_RechargeAmount_response(intent)
    
    elif intent_name == 'BalanceDetails':
        return get_BalanceDetails_response()    
    
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
        
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
