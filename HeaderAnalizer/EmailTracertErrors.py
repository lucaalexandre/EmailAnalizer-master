'''
Created on Mar 8, 2016

@author: grodriguez
'''

class NotMessageObject(Exception):
    '''
    EmailTracert handles email.Message objects to study the email headers
    when we expect a email.Message and receive other stuff, we raise
    this Exception
    '''
    def __init__(self):
        pass
    

class InvalidToken(Exception):
    '''
    TokeAnalizer Classes analize values of the message's headers,
    usually with a structured format, containing specific token.
    This exception MUST be raised when this token is not found or
    is not valid.
    '''
    def __init__(self,value,expected_token):
        self.value = value
        self.expected_token = expected_token
        
class InvalidValue(Exception):
    '''
    This class SHOULD be raise if we found some value that
    doesn't match with any expected possible value
    '''
    def __init__(self,value):
        pass