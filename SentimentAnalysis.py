import email, json, re, email.utils
from os import listdir

class Email(object):
    def __init__(self, email_path):
        '''Initializes an instance of the Email class.'''
        self.path = email_path

    def get_body(self):
        '''Stores the body of the email as an attribute, removing any whitespace characters and escapes.'''
        fp = open(self.path)
        msg = email.message_from_file(fp)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    self.body = remove_junk(str(part.get_payload(decode=True)))
                    self.get_label()
                    return
        else:
            self.body = remove_junk(str(msg.get_payload(decode=True)))
            self.get_label()
            return

    def get_label(self):
        if "align" in self.path:
            self.label = "positive"
        elif "neutral" in self.path:
            self.label = "neutral"
        elif "bash" in self.path:
            self.label = "negative"

    def validate(self):
        """Validates emails before adding it to the dictionary of emails."""
        fp = open(self.path)
        msg = email.message_from_file(fp)
        for item in msg.items():
            if item[0] == 'From':
                address = email.utils.parseaddr(item[1])
                self.address = address[1]
                if "google.com" in self.address or "Google.com" in self.address or "pols.exp@gmail.com" in self.address:
                    self.valid = False
                    return
                else:
                    self.valid = True
            if len(self.body) <= 16:
                self.valid = False

    def construct_dict(self):
        """Constructs a dictionary of email text and sentiment."""
        self.get_body()
        self.validate()
        if self.valid == False:
            return False
        email_dict = {}
        email_dict['text'] = self.body
        email_dict['label'] = self.label
        return email_dict

class Directory(Email):
    def __init__(self,directory):
        '''Initializes an instance of the Directory class.'''
        self.directory = directory

    def dir_list(self, dir):
        '''Returns the list of all files in self.directory'''
        try:
            return listdir(dir)
        except WindowsError as winErr:
            print("Directory error: " + str((winErr)))

    def dir_dict(self):
        '''Constructs a list of email dictionaries
        from the three directories of .eml files.'''
        eml_list = []
        for folders in self.dir_list(self.directory):
            self.eml = self.directory + '/' + folders
            for email in self.dir_list(self.eml):
                self.path = self.eml + '/' + email
                eml_dict = self.construct_dict()
                if eml_dict:
                    eml_list.append(eml_dict)
        return eml_list

    def convert_json(self, json_path):
        '''Creates a json file of email information at the specified path.'''
        with open(json_path,'w') as json_file:
            json.dump(self.dir_dict(), json_file)

def remove_junk(string):
    '''Removes whitespace characters, escapes, and links from a string.'''
    string = re.sub(r'\s+', ' ', string)
    string = re.sub(r"[\x80-\xff]", '', string)
    link_regex=["<http.*?>","http.*? ","http.*?[^\s]\.gov","http.*?[^\s]\.com","http.*?[^\s]\.COM",
                "www.*?[^\s]\.com","www.*?[^\s]\.org","www.*?[^\s]\.net","www.*?[^\s]\.gov","/.*?[^\s]\.com",
                "/.*?[^\s]\.COM","/.*?[^\s]\.gov",",.*?[^\s]\.gov",",.*?[^\s]\.com",
                "<.*?>"]
    for curr in link_regex:
        string = re.sub(curr,'',string)
    return string

def remove_non_ascii(text):
    '''Removes any non-ascii characters from a string.'''
    return ''.join(i for i in text if ord(i)<128)

def main():
    path = raw_input("Please enter the path of the folder I should train from?")
    p = Directory(path)
    json_fp = raw_input("Where should I save the train json?")
    p.convert_json(json_fp)
 
if __name__ == '__main__':
    main()
