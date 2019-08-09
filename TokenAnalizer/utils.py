'''
Created on 4/5/2016

@author: epzylon
'''
from ipaddress import IPv4Address as ip4
from ipaddress import IPv6Address as ip6

from pyparsing import OneOrMore, Optional, Suppress, Forward, alphanums, Word

class TextUtils(object):
    ''' Several string/text utils '''
    
    def __init__(self,raw):
        self.raw = raw
        self._NULL = ''
        self._PARENTHESES = [('[',']'),('<','>'),('{','}'),('(',')')]
    
    def remove_chars(self,char_list):
        '''Remove the chars given from the text'''
        for c in char_list:
            result = self.raw.replace(c,self._NULL)
    
        return result
    
           
    def get_enclosed(self,raw):
    
        #Word ::= Ascii - Tokens
        non_token = "!#$%&\'*+,-./:;=?@\\^_`|~"
        word = Word(alphanums+non_token)
        #word = Word(printables)
    
        #Tokens ::= {}[]()<>
        tokens = "{}[]()<>"  
    
        o_curly,c_curly,o_brack,c_brack,o_paren,c_paren,o_mayor,c_mayor = map(Suppress,tokens)

        enclosed_data = Forward()
        
        #Enclosed groups
        curly_enclosed = OneOrMore(o_curly + enclosed_data + c_curly)
        brack_enclosed = OneOrMore(o_brack + enclosed_data + c_brack)
        paren_enclosed = OneOrMore(o_paren + enclosed_data + c_paren)
        mayor_enclosed = OneOrMore(o_mayor + enclosed_data + c_mayor)
    
        enclosed = Optional(curly_enclosed) & Optional(brack_enclosed) & Optional(paren_enclosed) & Optional(mayor_enclosed) 
    
        enclosed_data << ((OneOrMore(word) & enclosed) ^ enclosed)
    
        return enclosed_data.parseString(raw)
        
    
    
class WhatIs(object):
    '''
    Try to determine what is the given value
    '''


    def __init__(self, value):
        self.value = value
    
    def this(self):
        if self.IsDomain():
            return ('domain')
        elif self.IsIP():
            if self.IsIPv4():
                return ('ip4')
            elif self.IsIPv6():
                return ('ip6')
        elif self.IsEmailAddr():
            return ('email')
        elif self.IsHeader():
            return ('header')
        else:
            return ('unknown')
    

    def IsDomain(self):
        pass
    
    def IsIP(self):
        '''
        If it is a ip (v4 or v6) it returns True
        '''
        if self.IsIPv4():
            return(True)
        elif self.IsIPv6():
            return(True)
        else:
            return(False)
    
    def IsIPv4(self):
        '''
        It retutns true only if it is a ipv4 (on a 4 octets form)
        '''
        #IPv4Addess allows one, two or tree decimal doted
        #digits as valid address, but we only want 4 octets
        if len(self.value.split('.')) == 4:
            try:
                ip4(self.value)
            except:
                return(False)
            else:
                return(True)        
    
    def IsIPv6(self):
        '''
        It returns true only if it is a ipv6
        '''
        try:
            ip6(self.value)
        except:
            return(False)
        else:
            return(True)
        
    
    def IsEmailAddr(self):
        pass
    
    def IsHeader(self):
        pass
    