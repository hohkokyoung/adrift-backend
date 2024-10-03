from django.utils.deprecation import MiddlewareMixin
from core.utils import remove_new_lines, safe_get, find_key
from django.conf import settings
import json
from threading import current_thread
from core.utils import logger

class GraphQLLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(request, 'body') and request.content_type == 'application/json':
            try:
                body = json.loads(request.body)
                
                logger.info(f"Request Body: {remove_new_lines(safe_get(body, 'query'))}")
            except (ValueError, KeyError) as exception:
                logger.error(f"Error processing GraphQL request: {exception}")
        return None

    def process_response(self, request, response):
        if hasattr(response, 'content'):
            byte_result = response.content
            decoded_result = byte_result.decode('utf-8')

            # this will extract error happened in run-time like import error
            index = decoded_result.find('Request Method:')

            if index != -1:
                # Extract the text before the line containing "Request Method:"
                error_messages = decoded_result[:index].strip()
                logger.error(error_messages)

            # bypass error on initial load
            try:
                data = json.loads(decoded_result)
            except Exception:
                return response
            
            logger.info(f"GraphQL Data: {data}")
            errors_data = find_key(data, "errors")
            errors = {'errors': errors_data}
    
            if errors_data:
                logger.error(f"GraphQL Error: {errors}")
        return response
    
# # https://stackoverflow.com/a/66316959
# _requests = {}

# def current_request():
#     return _requests.get(current_thread().ident, None)

# class CurrentUserMiddleware(MiddlewareMixin):

#     def process_request(self, request):
#         _requests[current_thread().ident] = request

#     def process_response(self, request, response):
#         # when response is ready, request should be flushed
#         _requests.pop(current_thread().ident, None)
#         return response


#     def process_exception(self, request, exception):
#         # if an exception has happened, request should be flushed too
#          _requests.pop(current_thread().ident, None)

import threading

thread_local = threading.local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_local.request = request
        thread_local.request.ip_address = request.META.get('REMOTE_ADDR')
        response = self.get_response(request)
        return response

def get_current_request():
    return getattr(thread_local, 'request', None)
