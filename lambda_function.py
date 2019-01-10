# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging
import boto3
import time
import datetime
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response



from decimal import Decimal

ml = boto3.client('machinelearning')


# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================
SKILL_NAME = "Workout Recommendation"
GET_FACT_MESSAGE = "... "
HELP_MESSAGE = "You can say tell me a space fact, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Space Facts skill can't help you with that.  It can help you discover facts about space if you say tell me a space fact. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Try this...open pathlon coach!" 

# =========================================================================================================================================
# Getting Latest Real-time Data from Google Sheets API and Feeding into AWS Machine Learning Model
# =========================================================================================================================================
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


# # use creds to create a client to interact with the Google Drive API
# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# client = gspread.authorize(creds)

# # Find a workbook by name and open the first sheet
# # Make sure you use the right name here.
# sheet = client.open("Fitbit Data - Daily Activity").sheet1

# #Sleep Minutes
# sleepdata= sheet.cell(5, 14).value
# #Previous Day Calories
# activitycalories= sheet.cell(6, 6).value
# #Very Active Minutes
# vactivemin= sheet.cell(6, 11).value

response = ml.predict(
    MLModelId='ml-QQgKl1iHzix',
    Record={
        'DayofWeek' : "Sunday",
        'PreviousDayCalories': str(2060),#str(activitycalories),
        'VeryActiveMin': str(50),#str(vactivemin),
        'SleepMins': str(600)#str(sleepdata)
    },
    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'


)
number = response["Prediction"]["predictedValue"]
# =========================================================================================================================================
# Retrieving latest prediction from AWS Machine Learning Model and translating it to user through VUI
# =========================================================================================================================================
  
  
data = "Your optimal time to workout today is at" + " " + str("%.2f" % number) + " o'clock"
  
  





#sending prediction value to Data base (DynamoDB) 
# title = "Prediction"
# number = response["Prediction"]["predictedValue"]
# value = Decimal(number)


# dynamodb = boto3.resource('dynamodb')
# dynamoTable = dynamodb.Table('test_table')
# dynamoTable.put_item(

#     Item={
#         'Name': title,
#         'Age' : value

#     }
# )

  


# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewSpaceFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        random_fact = data
        speech = GET_FACT_MESSAGE + random_fact

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
