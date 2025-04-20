from typing import List
from base64 import urlsafe_b64decode
from googleapiclient.discovery import build
from os import path
from datetime import datetime
from .credential import get_credentials

def connection():
    
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    
    return service
    
class Part():
    
    def __init__(self, part, ID):
        
        self.service = connection()
        self.ID = ID
        for key in part:
            
            setattr(self, key, part[key])
            
    def __repr__(self):
    
        return f'Part({self.filename})'
    
    def attachment(self, FOLDER_SAVE_FILE):
        
        if 'attachmentId' in self.body.keys():
            attachment = self.service.users().messages() \
            .attachments().get(id=self.body['attachmentId'], userId='me', messageId=self.ID).execute()
            data = attachment.get("data")
            filepath = path.join(FOLDER_SAVE_FILE, self.filename)
            if data:
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
                    
            print("DOWNLOAD:", filepath)
            return filepath
            
class Message():
    
    def __init__(self, msg):
        
        self.id = msg['id']
        self.labes = msg['labelIds']
        self.dates = datetime.fromtimestamp(int(msg['internalDate'])/1000)
        for header in msg['payload']['headers']:
            if header['name'] == "From":
                self.From = header['value']
            elif header['name'] == "Date":
                 self.date_send = header['value']       
        self.files = []
        if 'parts' in msg['payload'].keys():
            self.files = [Part(part,msg['id']) for part in msg['payload']['parts']]
        
    def __repr__(self):
        
        return 'Message(msg)'
    
class MailBox():
    
    def __init__(self):
        
        self.service = connection()
        self.__messages = None
    
    @property
    def messages(self) -> List[Message]:
        
        if self.__messages or isinstance(self.__messages,list) :
            
            return self.__messages
                
        raise RuntimeError('Search method needs to be executed!!')
    
    def search(self, subject:'str' = None) -> None:
        
        self.__messages = []
        mailbox = self.service.users().messages().list(userId='me')
        
        if subject:
            
            mailbox = self.service.users().messages().list(userId='me',q=subject)
        
        mailbox = mailbox.execute()
        
        if 'messages' in mailbox.keys():
            
            messages = mailbox['messages']
            
            IDs = [msg["id"] for msg in messages]
            

            for ID in IDs:

                msg = self.service.users().messages().get(userId='me', id=ID, format='full').execute()
                self.__messages.append(Message(msg))                       

class Gmail():
    
    def __init__(self):
        
        self.service = connection()
        self.mailbox = MailBox()
        
    def __repr__(self):
        
        return 'Gmail()'
      