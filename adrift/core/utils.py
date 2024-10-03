import copy
from graphql_relay import from_global_id
from django.conf import settings
from graphql import GraphQLResolveInfo
from django.utils.deprecation import MiddlewareMixin
import json
from datetime import datetime
from uuid import UUID
from enum import Enum
from decimal import Decimal
import html
import re
import bleach

import logging.config
logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger('general')

# this is a decorator function to provide a generic try-except error handling mechanism
# & it logs the full path to failed function in the case of a failure
# the default return value in any failure case is 'None', this value can be changed easily
# via the decorator argument
# credit: https://stackoverflow.com/questions/15572288/general-decorator-to-wrap-try-except-in-python
def handle_error(log_error=True, return_if_error=None, rerun=False, *args, **kwargs):
    def decorate(func):
        def applicator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # log where the exception is coming from
                if log_error:
                    logger.error(f"Error in {func.__qualname__}:", e)
                
                if rerun:
                    return func(*args, **kwargs)
            
                return return_if_error

        return applicator

    return decorate

# def handle_graphql_error(*args, **kwargs):
#     def decorate(func):
#         def applicator(*args, **kwargs):
#             graphql_resolve_info = [arg for arg in args if isinstance(arg, GraphQLResolveInfo)][0]
#             field_name = graphql_resolve_info.field_name
#             try:
#                 logger.info(f"Ran {graphql_resolve_info.parent_type}: {field_name}")
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 # log where the exception is coming from
#                 logger.error(f"Error in {func.__qualname__} at {graphql_resolve_info.parent_type} {field_name}: {e}")
#                 raise e

#         return applicator

#     return decorate

# helper function to decode a Relay global id back to django model object id
# with error handling
@handle_error(log_error=False)
def decode_global_id(id=None):
    return from_global_id(id)[1]


# for accessing deep nested json data in a safer way
def safe_get(obj, *keys):
    try:
        for key in keys:
            if isinstance(obj, dict):
                obj = obj[key]
            else:
                obj = getattr(obj, key)
    except (KeyError, IndexError, AttributeError):
        return None
    return obj

# a function that helps to remove all key-value pairs in the given dict using the given
# key names
def remove_from_dict(_dict, *keys):
    new_dict = copy.deepcopy(_dict)
    for key in keys:
        if key in new_dict:
            del new_dict[key]
    return new_dict


def remove_new_lines(text):
    return text.replace('\n', '').replace('\r', '')

def find_key(obj, key_value):
    if isinstance(obj, dict):
        if key_value in obj:
            return obj[key_value]
        for key, value in obj.items():
            result = find_key(value, key_value)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_key(item, key_value)
            if result is not None:
                return result
    return None

def serialize(data):
    """
    Serialize a dictionary, converting non-JSON serializable objects to strings.
    """
    serialized_data = {}
    for key, value in data.items():
        if key == '_state':
            continue  # Exclude Django internal attribute

        if isinstance(value, datetime):
            serialized_data[key] = value.isoformat()  # Convert datetime to ISO 8601 string
        elif isinstance(value, UUID):
            serialized_data[key] = str(value)  # Convert UUID to string
        elif isinstance(value, Enum):
            serialized_data[key] = value.value  # Convert Enum to its value
        elif isinstance(value, Decimal):
            serialized_data[key] = float(value)  # Convert Decimal to float
        else:
            try:
                json.dumps(value)  # Test if value is serializable
                serialized_data[key] = value
            except (TypeError, ValueError):
                serialized_data[key] = str(value)  # Fallback to string representation

    return serialized_data

def sanitize(input):
    
    # Step 0: Clean using library (do add in allowed tags and attributes when needed)
    sanitized = bleach.clean(input)

    # Step 1: Escape HTML special characters
    sanitized = html.escape(sanitized)
    
    # Step 2: Neutralize JavaScript event handlers
    # Pattern for typical event handlers
    event_handler_pattern = re.compile(r'\bon\w+=', re.IGNORECASE)
    sanitized = event_handler_pattern.sub(lambda match: 'safe_' + match.group(), sanitized)
    
    # Step 3: Remove dangerous JavaScript and CSS expressions
    # This pattern looks for "javascript:" schemes and similar dangerous expressions
    dangerous_js_pattern = re.compile(
        r'javascript:|vbscript:|data:|base64|expression\(|alert\(|prompt\(|confirm\(|eval\(|setTimeout\(', 
        re.IGNORECASE
    )
    sanitized = dangerous_js_pattern.sub(lambda match: '', sanitized)
    
    # Step 4: Neutralize dangerous URL schemes in href/src attributes
    url_scheme_pattern = re.compile(r'\b(href|src)=["\'](javascript:|data:|vbscript:)', re.IGNORECASE)
    sanitized = url_scheme_pattern.sub(lambda match: match.group(1) + '="safe_' + match.group(2), sanitized)
    
    return sanitized

