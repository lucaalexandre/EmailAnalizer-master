'''
Created on Mar 8, 2016

@author: Gustavo Rodriguez
'''

#Email utils
from email.utils import parsedate as ParseDate
from email.utils import parseaddr as ParseAddr

#Customized raised errors
from HeaderAnalizer.EmailTracertErrors import InvalidValue, InvalidToken

#Ip object
from ipaddress import ip_address as ip

#Utils to parse some strings
from TokenAnalizer.utils import WhatIs, TextUtils

#Pyparsing objects
from pyparsing import OneOrMore, Group, Optional, Dict, Word, CaselessLiteral,\
    ParseException, printables

#TODO: Create a FOR class




class ExtendedDomain(object):
    '''
    The information related to the tokens FROM and BY is called an described
    on the RFC 5321, section 4.4 as Extended-Domain in Augmented BNF notation
    This object receive this strings and make the analisys/disection
    '''

    
    def __init__(self,value=None,ip=None,domain=None,port=None,extra=None):
        
        #Values dictionary
        self._values = {'ip':'',
              'domain':'',
              'port':'',
              'extra':[]
              }
        self.__r_chars = ['[',']','(',')']
        
        if value == None:
            if ip != None:
                self._values['ip'] = ip
            if domain != None:
                self._values['domain'] = domain
            if port != None:
                self._values['port'] = port
            if extra != None:
                self._values['extra'] = extra
        else:
            self.__fill_values(value)
            
        #TODO: Please fix this uggly uggly method!
        self.__generate_attributes()
        
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        r = "ExtendedDomain("
        r_attr = ""
        for key in self._values.keys():
            if self._values[key] == '' or self._values[key] == []:
                pass
            else:
                r_attr = r_attr + str(key) + "=\"" + str(self._values[key]) + "\","
        if r_attr == "":
            return ""
        else:
            #Strip the last ,
            r = r + r_attr[:-1]
            r = r + ")"
            return r
    
    def __fill_values(self,value_list):            
        for val in value_list:
            #TODO: Before remove brackets and parenthesis
            #we should agroup this info
            val = TextUtils(val).remove_chars(self.__r_chars)
            
            #Test if it is a domain
            if self.__is_domain(val):
                self._values['domain'] = val
            #Test if it is a ipv4
            elif WhatIs(val).IsIPv4():
                self._values['ip'] = ip(val)
            #Test if it is a ipv6
            #TODO:Check
            #BUG:Check if it really degtect IPv6
            elif WhatIs(val).IsIPv6():
                self._values['ip'] = ip(val)
            #Otherwise
            else:
                #It could be a tuple ip:port
                if val.find(':') != -1:
                    possible_ip,*port = val.split(':')
                    if WhatIs(possible_ip).IsIP():
                        self._values['ip'] = ip(possible_ip)
                        self._values['port'] = port
                #Or somenthing else
                else:
                    self._values['extra'].append(val)

           
    #TODO: Replace with utils function
    def __is_domain(self,value):
        #Domain should have at least on dot
        #TODO: Please improve this!!!!
        if value.find('.') != -1:
            v_list = value.split(".")
            if v_list[-1].isalpha():
                return True
            else:
                return False
        else:
            return False
    
    def __generate_attributes(self):
        # This function is to load the values in the dict
        # to an attributes of the ExtendedDomain Object
        
        #Create attributes with no values
        self.ip = ''
        self.domain = ''
        self.port = ''
        self.extra = ''
        self.address = ''
        
        #fill attributes
        #TODO: Fix that! type(val) != ip
        if True:
            self.ip = self._values['ip']   
        
        if len(self._values['domain']) != 0:
            self.domain = self._values['domain']
        
        if len(self._values['port']) != 0:
            self.domain = self.port = self._values['port']
            
        if len(self._values['extra']) != 0:
            for e in self._values['extra']:
                self.extra = self.extra + ' ' + e 
        
        #This attribute is a easy way to get the ip or the domain
        if self.ip != '':
            self.address = str(self.ip)
        elif self.domain != '':
            self.address = self.domain
            

class Received(object):
    '''
    Aanalize the Received values and return a dic object
    Please refer to RFC 5321, section 4.4
    https://tools.ietf.org/html/rfc5321#section-4.4
    '''
    
    _FROM = 'from'
    _BY = 'by'
    _VIA = 'via'
    _WITH = 'with'
    _ID = 'id'
    _FOR = 'for'
    
    
    def __init__(self,received_value,rec_dict={}):
        
        #Split the rec string and the date
        if received_value.find(';'):
            self._rec,self._date_string = received_value.split(';')
            
            #Strip new line strings
            self._date_string = self._date_string.replace('\n','')
        else:
            self._rec = received_value
        
        if rec_dict != {}:
            self.received = rec_dict
            self.Date = ParseDate(self.received['date'])
        else:
            self.received = self._parse_rec_string()   
            
            #Set the date property
            self.Date = ParseDate(self._date_string)
             
        self._fill_values()
   
            
    
    def _parse_rec_string(self):
        '''
        Pyparsing parser to the received string
        '''
        #any word
        word = Word(printables)
        
        #recognized tokens
        from_t = CaselessLiteral(self._FROM)    
        by_t = CaselessLiteral(self._BY)
        with_t = CaselessLiteral(self._WITH)
        id_t = CaselessLiteral(self._ID)
        via_t = CaselessLiteral(self._VIA)
        for_t = CaselessLiteral(self._FOR)
    
        #A group of non tokens
        phrase = OneOrMore(~from_t + ~by_t + ~with_t + ~id_t + ~for_t + ~via_t + word)
       
        #Group phrase with token
        from_g = Optional(Group(from_t+phrase))
        by_g = Optional(Group(by_t+phrase))
        with_g = Optional(Group(with_t+phrase))
        id_g = Optional(Group(id_t+phrase))
        via_g = Optional(Group(via_t+phrase))
        for_g = Optional(Group(for_t+phrase))
        
        grouped_data = from_g & by_g & with_g & id_g & via_g & for_g
        
        parse_to_dict = Dict(grouped_data)
        
        try:
            rec_dict = parse_to_dict.parseString(self._rec)
        except ParseException:
            rec_dict = {}
        
        return rec_dict
    
    def _fill_values(self):
        space = " "

        ########### From #############
        if self._FROM in self.received.keys():
            raw_from = self.received[self._FROM]
        else:
            raw_from = ""
        
        if type(raw_from) != str and len(raw_from) >1:
            self.From = space.join(raw_from)
        else:
            self.From = raw_from
            
        ########### By #############        
        if self._BY in self.received.keys():
            raw_by = self.received[self._BY]
        else:
            raw_by = ""
            
        if type(raw_by) != str and len(raw_by) > 1:
            self.By = space.join(raw_by)
        else:
            self.By = raw_by
        
        ########### With ############            
        if self._WITH in self.received.keys():
            raw_with = self.received[self._WITH]
        else:
            raw_with = ""
        
        if type(raw_with) != str and len(raw_by) > 1:
            self.With = space.join(raw_with)
        else:
            self.With = raw_with
            
        ########### Id #############
        if self._ID in self.received.keys():
            raw_id = self.received[self._ID]
        else:
            raw_id = ""
        
        if type(raw_id) != str and len(raw_id) > 1:
            self.Id = space.join(raw_id)
        else:
            self.Id = raw_id
    
        ########### Via ############
        if self._VIA in self.received.keys():
            raw_via = self.received[self._VIA]
        else:
            raw_via = ""
            
        if type(raw_via) != str and len(raw_via) > 1:
            self.Via = space.join(raw_via)
        else:
            self.Via = raw_via

        ########### For ############
        if self._FOR in self.received.keys():
            raw_for = self.received[self._FOR]
        else:
            raw_for = ""
        
        if type(raw_for) != str and len(raw_for) > 1:
            self.For = space.join(raw_for)
        else:
            self.For = raw_for
    
    
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        repr_str = "Received(rec_dict={"
        if self.From != "":
            repr_str += "\'from\':\'" + self.From + "\', "
        if self.By != "":
            repr_str += "\'by\':\'" + self.By + "\', "
        if self.Via != "":
            repr_str += "\'via\':\'" + self.Via + "\', "
        if self.With != "":
            repr_str += "\'with\':\'" + self.With + "\', "
        if self.For != "":
            repr_str += "\'for\':\'" + self.For + "\', "
        if self._date_string != "":
            repr_str += "\'date\':\'" + self._date_string + "\' "
        repr_str += "})"
        
        return repr_str
    