"""
wichtel_bot
november 2021
ilsa toy

this script will help you to organize your game of secret santa (which is called 'wichteln' in austria),
without any physical contact of the participants and the opportunity to keep the 'wichtel-assignment' top-secret
for everybody.
this small program allows you to assign each participant, who signed up via a spread sheet, to a random other
participant and send each one of them an automated email, which contains the presentee's name, their likes, dislikes and
postal address if given.
"""

# do not change this code block start
import random
import csv
import smtplib
import ssl
import re
from email.message import EmailMessage
# do not change this code block end

# Please read the file 'readme.txt' before proceeding.

# Change the values of the seven following variables (if needed)

# your new gmail address
my_email = "my_new_gmail_address"
# the path of your csv file; make sure to stick with r"path" or r'path' and include no additional quotation marks
my_csv_path = r"my_path"
# the subject of the mails the wichtel_bot is going to send to the participants
subject = "wichteln 2021"
# the number of gifts that are being exchanged (maybe you want to gift a small present every week?)
number_of_gifts = "1"
# the time or the timeframe for gifting (e.g. 'on the 22. of December'; 'from the 05th to the 20th of December' or
# 'each week, starting on the 01st of December')
due_date = "on the 24th of December"
# the maximum amount of money the present should cost
max_cost = "10 €"
# if you want to do multiple presents and want the last present to be a special one (= higher maximum amount of money
# allowed), define an alternative max_cost for the last present here. Please leave this empty, if all presents should
# cost the same!
max_cost_alt = ""

# good job! now the wichtel_bot knows everything it needs to know, to do its magic. Please make a test run with the file
# 'wichtel_bot_test.csv', to assure the mails will contain the desired messages and will be sent properly.
# Please refer to the file 'readme.txt' on how to do a test run.

port = 587  # For TSL
password = input(f"Type the password of the mail-account you set as 'my_email' and press enter: ")

# create a connection to the mail servers
context = ssl.create_default_context()
try:
    server = smtplib.SMTP("smtp.gmail.com")
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(my_email, password)

    # import data from csv file
    with open(my_csv_path, newline='\n', encoding='utf-8') as csvfile:
        ureader = csv.reader(csvfile, delimiter=';')
        next(ureader)  # skips first line in csv

        # create a nested dictionary and check for irregularities in the submitted .csv file
        wichtel = {}
        counter = 1
        counter_2 = 0
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for row in ureader:
            if len(row) < 2:
                pass
            elif row[0] == "" and row[1] == "":
                pass
            elif row[0] == "" and re.fullmatch(regex_mail, row[1]):
                print(f"There seems to be something missing in your .csv file. For {row[1]}, no name has been entered.")
                counter_2 += 1
            elif row[0] != "" and not re.fullmatch(regex_mail, row[1]):
                print(
                    f"There seems to be something missing in your .csv file. For {row[0]}, no valid mail-address has been entered.")
                counter_2 += 1
            else:
                wichtel[counter] = {}
                wichtel[counter]['name'] = row[0]
                wichtel[counter]['mail'] = row[1]
                wichtel[counter]['likes'] = row[2]
                wichtel[counter]['dislikes'] = row[3]
                wichtel[counter]['address_1'] = row[4]
                wichtel[counter]['address_2'] = row[5]
                wichtel[counter]['address_3'] = row[6]
                counter += 1

        # if there are only 1 or 2 participants, there really is no point in "wichteln"
        if counter <= 3:
            print("It seems, that there are too little participants, to play wichteln properly. Please add at least three participants to your .csv file and try again.")
            quit()

        # if there's something fishy in your .csv file, the program will print the following message and terminate.
        if counter_2 > 0:
            print("No mails were sent. Please check your .csv file and try again!")
            quit()

    # crate a list with all the wichtels, then shuffle it and zip it
    list_gifter = []

    for elem in wichtel:
        list_gifter.append(elem)

    list_presentee = list_gifter.copy()

    list_shuffled = []

    # this makes sure, that none of the wichtels are assigned to themselves
    is_shuffled = False
    while not is_shuffled:
        random.shuffle(list_presentee)
        list_shuffled = list(zip(list_gifter, list_presentee))
        is_shuffled = True
        for elem in list_shuffled:
            if elem[0] == elem[1]:
                is_shuffled = False

    # the following lines set variables for the receiver's mail-address, the sender's and receiver's names and the
    # receiver's likes, dislikes and postal address.
    counter_3 = 0
    for item in list_shuffled:
        sender_mail = my_email
        receiver_mail = wichtel[item[1]]["mail"]

        sender = wichtel[item[0]]["name"]
        receiver = wichtel[item[1]]["name"]

        likes = wichtel[item[1]]["likes"]
        dislikes = wichtel[item[1]]["dislikes"]

        address_1 = wichtel[item[1]]['address_1']
        address_2 = wichtel[item[1]]['address_2']
        address_3 = wichtel[item[1]]['address_3']

        # this assures, no string is used as the number of gifts. and yes, testing showed we need this.
        number_of_gifts = int(number_of_gifts)

        # this generates an object of the class 'EmailMessage' and sets the values of the fields 'subject', 'from' and 'to'
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = sender_mail
        message['To'] = receiver_mail

        # the participants will receive different messages, depending on which values were set for the variables by
        # either you, or the participants. these are all the components, a message could consist of:

        msg_1 = f"""Hello {sender}!

Thank you for participating in this year's 'wichtel-game'. Each one of us will gift another, randomly assigned person {number_of_gifts} present(s) during christmas season.
Your 'wichtel-present-receiver' has been chosen randomly and iiiiiiiiis (insert drumroll) {receiver}!
"""

        msg_2ld = f"""According to our research, {receiver} likes {likes} and dislikes {dislikes}. What a sublime taste!"""
        msg_2l = f"""According to our research, {receiver} likes {likes} and dislikes... nothing?! A great person to give gifts to!"""
        msg_2d = f"""According to our research, {receiver} dislikes {dislikes}. I wonder what {receiver} wishes for. I'm sure you will find out!"""
        msg_2 = f"""Unfortunately, I was not able to find out what {receiver} likes and dislikes. You will have to be extra creative!"""
        msg_3 = f"""\nThe gifts will be exchanged {due_date}. Your wichtel-group agreed on a maximum cost of {max_cost} for the present."""
        msg_3_multiple_gifts = f"""\nThe {number_of_gifts} gifts will be exchanged {due_date}. Your wichtel-group agreed on a maximum cost of {max_cost} for each present."""
        msg_3_multiple_gifts_dif_cost = f"""\nThe {number_of_gifts} gifts will be exchanged {due_date}. Your wichtel-group agreed on a maximum cost of {max_cost} for the first present(s) and {max_cost_alt} for the very last present."""

        msg_4_postal = f"""\nI noticed, that {receiver} and you might not see each other in person. But do not worry, you can send your present by postal mail to:
        
    {receiver}
    {address_1}
    {address_2}
    {address_3}"""

        msg_5 = f"""\n\nHappy Holidays and best regards

wichtel_bot

(this is an auto-generated message)"""

        # now we need to build the message, depending on the values of our variables

        msg_complete = f""
        msg_complete += msg_1

        if len(likes) > 0 and len(dislikes) > 0:
            msg_complete += msg_2ld
        elif len(likes) > 0 and len(dislikes) <= 0:
            msg_complete += msg_2l
        elif len(likes) <= 0 and len(dislikes) > 0:
            msg_complete += msg_2d
        elif len(likes) <= 0 and len(dislikes) <= 0:
            msg_complete += msg_2

        if number_of_gifts > 1 and max_cost_alt == "":
            msg_complete += msg_3_multiple_gifts
        elif number_of_gifts > 1 and max_cost_alt != "":
            msg_complete += msg_3_multiple_gifts_dif_cost
        else:
            msg_complete += msg_3

        if len(address_1) > 0 and len(address_2) > 0:
            msg_complete += msg_4_postal
        else:
            pass

        msg_complete += msg_5
        message.set_content(msg_complete)

        # the mail is sent, using the method '.sendmail()'
        server.sendmail(my_email, receiver_mail, message.as_string())

        counter_3 += 1
        print(f"An email was successfully sent to {sender}.")
    print(f"A total of {counter_3} emails were sent successfully.")

# this is some further blabla in case either you or i fudged something up
except smtplib.SMTPAuthenticationError:
    print(f"""There seems to be a problem, logging into your mail-account. Please make sure, {my_email} is your correct 
email address and you entered the right password.""")
    quit()
except Exception as e:
    print(f"""An Error has occurred. {e}
Please try opening the original file, refer to the file 'readme.txt' and try again""")
    quit()
finally:
    server.quit()

# if you can read this in the end, everything should have gone just fine.
print("Ho ho ho, my job is done!")