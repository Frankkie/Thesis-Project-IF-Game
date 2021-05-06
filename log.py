"""

https://medium.com/swlh/add-log-decorators-to-your-python-project-84094f832181

Classes:


Functions:


"""


import logging
import os
import sys
import functools
from inspect import getframeinfo, stack


default_log_file = "log"
default_log_file_dir = ""


class CustomFormatter(logging.Formatter):
    """ Custom Formatter does these 2 things:
    1. Overrides 'funcName' with the value of 'func_name_override', if it exists.
    2. Overrides 'filename' with the value of 'file_name_override', if it exists.
    """

    def format(self, record):
        if hasattr(record, 'func_name_override'):
            record.funcName = record.func_name_override
        if hasattr(record, 'file_name_override'):
            record.filename = record.file_name_override
        return super(CustomFormatter, self).format(record)


def get_logger(log_file_name, log_dir=""):
    """ Creates a Log File and returns Logger object """

    # Build Log File Full Path
    logpath = log_file_name if os.path.exists(log_file_name) else os.path.join(log_dir, (str(log_file_name) + '.log'))

    # Create logger object and set the format for logging and other attributes
    logger = logging.Logger(log_file_name)

    handler = logging.FileHandler(logpath, 'a+')
    """ Set the formatter of 'CustomFormatter' type as we need to log base function name and base file name """
    handler.setFormatter(CustomFormatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s'))
    logger.addHandler(handler)

    # setting the level of logger
    logger.setLevel(logging.DEBUG)

    # Return logger object
    return logger


def log_decorator(_func=None):
    def log_decorator_info(func):
        @functools.wraps(func)
        def log_decorator_wrapper(self, *args, **kwargs):
            """Build logger object"""
            try:
                log_file_name = self.log_file_name
                log_dir = self.log_file_dir
            except AttributeError:
                log_file_name = default_log_file
                log_dir = default_log_file_dir
            logger_obj = get_logger(log_file_name=log_file_name, log_dir=log_dir)

            """ Create a list of the positional arguments passed to function"""
            args_passed_in_function = [repr(a) for a in args]
            """ Create a list of the keyword arguments"""
            kwargs_passed_in_function = [f"{k}={v!r}" for k, v in kwargs.items()]
            """ The lists of positional and keyword arguments is joined together to form final string """
            formatted_arguments = ", ".join(args_passed_in_function + kwargs_passed_in_function)

            """ log function argumments before execution"""
            logger_obj.info(f"Arguments: {formatted_arguments} - Begin function")

            py_file_caller = getframeinfo(stack()[1][0])
            extra_args = {'func_name_override': func.__name__,
                          'file_name_override': os.path.basename(py_file_caller.filename)}

            """ Before to the function execution, log function details."""
            logger_obj.info(f"Arguments: {formatted_arguments} - Begin function", extra=extra_args)
            try:
                """ log return value from the function """
                value = func(self, *args, **kwargs)
                logger_obj.info(f"Returned: - End function {value!r}", extra=extra_args)
            except:
                """log exception if occurs in function"""
                logger_obj.error(f"Exception: {str(sys.exc_info()[1])}", extra=extra_args)
                raise
            return value
        return log_decorator_wrapper
    if _func is None:
        return log_decorator_info
    else:
        return log_decorator_info(_func)


