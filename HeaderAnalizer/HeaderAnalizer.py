'''
Created on Mar 8, 2016
@author: grodriguez
'''
from email import message_from_string as m_string
from email.utils import parseaddr as address
from email.utils import parsedate as date
from TokenAnalizer.Identifiers import MessageID



class HeaderAnalizer(object):
    '''
    Receive a Mail message and analyze the Trace headers
    '''
    from_emails = []

    def __init__(self, message_string):
        try:
            self.message = m_string(message_string)
        except:
            pass
        else:
            #############################################
            # Headers that should appears at most once  #
            # and should have only one value            #
            #############################################
            
            #Odd header            
            self.orig_date = date(self.message.get('date'))
            
            #Address type headers
            self.sender = address(self.message.get('sender'))
            self.reply_to = address(self.message.get('reply-to'))
            
            #ID type headers
            self.message_id = MessageID(self.message.get('message-id'))
            
            #Subject
            self.subject = self.message.get('subject')
            
            
            #############################################
            # Headers that should appears once but could#
            # have multiple values on it                #
            #############################################
            
            #Address type fields
            self.from_list = []
            self.bcc_list = []
            self.cc_list = []
            self.reply_to_list = []
            
            for addr in self.message.get('from'):
                self.from_list.append(address(addr))
            
            for addr in self.message.get('bcc'):
                self.bcc_list.append(address(addr))
                
            for addr in self.message.get('cc'):
                self.cc_list.append(address(addr))
            
            for addr in self.message.get('reply-to'):
                self.reply_to_list.append(address(addr))
            
            #Message id type
            self.references_list = []
            self.inReplyTo_list = []
            
            message_ids = self.message.get('references')
            for mid in message_ids:
                self.references_list.append(mid)
            
            message_ids = self.message.get('in-reply-to')
            for mid in message_ids:
                self.inReplyTo_list.append(mid)
            
            #################################################
            # Headers that has unlimited appears restriction #
            #################################################
            
            self.comments = []
            self.keywords = []
            
            for comment in self.message.get('comments'):
                self.comments.append(comment)
                
            for keys in self.message.get_all('keywords'):
                for key in str.split(keys,","):
                    self.keywords.append(key)
            
            
            
            

            
            

       
       


    def getHeaders(self):
        pass
    
    def getBody(self):
        pass
    
    def getTraceHeaders(self):
        pass
    
    def getTraceIPList(self):
        pass
    
    def getTraceTimming(self):
        pass
    
    def getMailEditor(self):
        pass
    
