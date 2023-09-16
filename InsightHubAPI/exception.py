from rest_framework.views import exception_handler
from core.models import Exceptions
import traceback
import sys

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        message = str(sys.exc_info()[0]) + str(sys.exc_info()[1])
        Exceptions.objects.create(stackTrace=traceback.format_exc(), message=exc, errorType=sys.exc_info()[0].__name__,
                                  exceptionMethod=context['request'].method)
    return response
