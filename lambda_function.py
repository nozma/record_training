import gsheet
import os
import datetime

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

sb = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "懸垂を記録するには、チンアップを3回やった、のように言ってください。"

        return (
            handler_input.response_builder
                .speak(speech_text)
                .ask(speech_text)
                .response
        )


class RecordChinUpHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("RecordChinUp")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        number = get_slot_value(
            handler_input = handler_input,
            slot_name = "number"
        )
        method = get_slot_value(
            handler_input = handler_input,
            slot_name = "method"
        )
 
        request = {
            "function": "appendRecords",
            "parameters": [{
                "query_result": {
                "number": number,
                "method": method
                }
            }],
            "devMode": True
        }

        gsheet.write_data(gsheet.get_auth(), request)
        
        speech_text = str(number) + "回" + method + "の記録をしました"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("懸垂記録", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        print(exception)

        speech = "すみません、わかりませんでした。もう一度言ってください。"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RecordChinUpHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()