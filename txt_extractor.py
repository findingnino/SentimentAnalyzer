from os import listdir
import email, re, time


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

def main():
    eml_path = raw_input("Where is the eml directory to be tested?")
    save = raw_input("Where should I save the new, txt-only folder?")
    filename = 1
    for emails in listdir(eml_path):
        path = eml_path + '/' + emails
        msg = email.message_from_file(open(path))
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = remove_junk(str(part.get_payload(decode=True)))
                elif part.get_content_type() == 'text/html':
                    body = remove_junk(str(part.get_payload(decode=True)))
        else:
            body = remove_junk(str(msg.get_payload(decode=True)))

        new = save + '/' + str(filename)
        with open(new, 'w') as file:
            file.write(body)
            filename = eval('1 + filename')
        time.ctime()


if __name__ == '__main__':
    main()
