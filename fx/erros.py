'''Xchanger exceptions module'''

from termcolor import colored

class XchangerException(Exception):
    '''Exception class with message as a required parameter'''
    def __init__(self, message):
        self.message = colored(message,"red",attrs=["bold"])
        super().__init__(self.message)