'''
Created on 2/5/2016

@author: epzylon
'''
from HeaderAnalizer.EmailTracertErrors import InvalidValue
from email.utils import parsedate as date


class MessageID(object):
    '''
    Analize the Message-ID header
    '''

    def __init__(self, value):
        self.raw = value
        try:
            left,right = self.raw.split('@')
        except ValueError:
            raise InvalidValue
        
        self.id_left = left.strip('<')
        self.id_right = right.strip('>')
        
    
    def __str__(self):
        return (self.id_left + '@' + self.id_right)
    
    def __repr__(self):
        return ('MessageID(\'' + self.raw + '\'')
    

class ReceivedString(object):     
    '''
    Parse the Received field
    '''
    
    def __init__(self, value):
        self.raw = value
        try:
            self._rec,self._date_string = self.raw.split(';')
            self.date = date(self.date_string)
        except ValueError:
            raise InvalidValue
        
    
    def _parse_received(self):
        pass
    
    
        
        
    
    
        
        