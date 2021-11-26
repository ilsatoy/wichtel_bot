# wichtel_bot
November 2021\
ilsa toy

This script will help you to organize your game of Secret Santa (which is called 'Wichteln' in Austria), without any physical contact of the participants and the opportunity to keep the 'Wichtel-assignment' top-secret for everybody. This small program allows you to assign each participant, who signed up via a spread sheet, to a random other participant and send each one of them an automated email, which contains the presentee's name, their likes, dislikes and postal address if given.


## Disclaimer
I am new to programming and this is my first project. so please be kind.
When writing comments and explanations, i tend to think of the readers as people like me, who have little to no knowledge about coding and stuff. So please excuse the detailed readme and comments.

## How to use this code

* step 1: Download this file and open the containing folder in your terminal (on windows press shift + right click anywhere in the folder, then select 'open powershell window here').

* step 2: Make sure that Python is installed (https://www.python.org/downloads/ - there are great online tutorials on how to install it, i recommend watching one).

* step 3: Create a new Gmail address, that is not linked to any of your other accounts (creating a new address is advised due to safety and privacy concerns). This code only runs with a Gmail address. If you want to use another provider, you will have to make sure TSL is supported and change the line 'server=smtplib.SMTP("smtp.gmail.com")' according to the the provider you are using.

* step 4: Sign in to your new Gmail account and set the option 'Allow less secure apps' to ON (https://myaccount.google.com/lesssecureapps)

* step 5: Create a spread sheet (or Google sheet) that contains the following colums:

	name; email address; likes; dislikes; street name and house number; postal code and location; country

	Please stick to this order! If you don't want to collect a certain information, just insert an empty colum (e.g. an empty colum for likes or dislikes) or 	leave the colum blank (e.g. last three colums stay blank, if you do not want to ask for postal addresses). 

* step 6: Export the final version of the spread sheet as a csv (save as CSV UTF-8 (comma delimited)).

Now it's time to add some more information. You can do so by changing the values of some variables* (look below for further information about variables and values).

* step 7: Change the value of the variable 'my_email' to the new address you created in step 3.

* step 8: Change the value of the variable 'my_csv_path' to the path of the csv file, that holds the participant's information (shift + right click on csv file - copy as path).

* step 9: Change the value of the variable 'subject' to the subject, you want every outgoing mail to have.

* step 10: Change the value of the variable 'number_of_gifts' to the amount of total gifts you want to exchange. This variable has to be a number >= 1.

* step 11: Change the value of the variable 'due_date' to the date on which the participants should hand over the gifts (e.g. 'on the 22nd of December', 'from the 05th to the 20th of December' or 'each week, starting on the 01st of December').

* step 12: Change the value of the variable 'max_cost' to the maximum amount of money, the present should cost.

* step 13: (optional) ONLY change the value of the variable 'max_cost_alt' if you want to exchange multiple gifts AND want to the maximum amount of money for the last gift to differ (e.g. be higher) than for the other ones.

* step 14: (optional) If you want to change the messages you can do so, by scrolling down to the message components, starting at line 153. Look below for further information about the different message components.** Make sure, your changes work with the following if-statements.

* step 15: Run the script (a test run with a test csv file is advised).***
	Note, that the requested password is the password you set for your new gmail account.


## Further information about instructions marked with one or multiple *

\* Values and variables

If you are new to this, some of the wording might be a little confusing. A variable is a symbolic name, that is a reference or pointer to an object (e.g. a = 5; a is our variable and 5 is our value).
In this code the variable 'number_of_gifts' is set to the value 1 by default. If you change it to another number, python will use this new number, every time we use the variable 'number_of_gifts'.
You might ask yourself why the values are between quotation marks. This is, because we want python to know, that we want the values to be a text (called string). So please stick with the quotation marks and use either "" or '' when setting the values.

\** The different message components

msg_1				is used in every message\
msg_2ld				is used, if the row of the csv included both likes and dislikes of the participant\
msg_2l				is used, if the row of the csv only included likes\
msg_2d			is used, if the row of the csv only included dislikes\
msg_2				is used, if the row of the csv included neither likes nor dislikes\
msg_3				is used, if number_of_gifts = 1\
msg_3_multiple_gifts		is used, if number_of_gifts > 2\
msg_multiple_gifts_dif_cost	is used, if number_of_gifts > 2 AND the value of the variable 'max_cost_alt' is not an empty string.\
msg_4				is only used, if the row of the csv contained information about the postal address in the last 3 colums\
msg_5				will be used in every message

\*** running the test csv 'test_wichtel_bot.csv'

Follow step 1
Open the csv file 'test_wichtel_bot.csv' in Excel or in your text editor. Change every entry under 'email address' to an address, you
have access to. Save the file. 
In step 2 set the value of the variable 'my_csv_path' to the path of 'test_wichtel_bot.csv' by shift+right clicking on the file and choose 'copy as path'. If a second set of quotation marks was copied, delete those.
Follow steps 3 to 13
Now you should receive 4 mails. The names may vary, since the program shuffels the participants differently every time, but should otherwise
look something like this, depending on the values you set for the variables in step 9 to 12:

	Hello Paul!

	Thank you for participating in this year's 'wichtel-game'. Each one of us will gift another, randomly assigned person 2 present(s) during christmas season.
	Your 'wichtel-present-receiver' has been chosen randomly and iiiiiiiiis (insert drumroll) Steven!
	According to our research, Steven dislikes candles. I wonder what Steven wishes for. I'm sure you will find out!
	The 2 gifts will be exchanged starting on the 01 st of December. Your wichtel-group agreed on a maximum cost of 10 € for the first present(s) and 15 € for the
	very last present.

	Happy Holidays and best regards

	wichtel_bot

	(this is an auto-generated message)

or

	Hello Claire!
	
	Thank you for participating in this year's 'wichtel-game'. Each one of us will gift another, randomly assigned person 2 present(s) during christmas season.
	Your 'wichtel-present-receiver' has been chosen randomly and iiiiiiiiis (insert drumroll) Maria!
	According to our research, Maria likes sweets and dislikes... nothing?! A great person to give gifts to!
	The 2 gifts will be exchanged starting on the 01 st of December. Your wichtel-group agreed on a maximum cost of 10 € for the first present(s) and 15 € for the
	very last present.
	I noticed, that Maria and you might not see each other in person. But do not worry, you can send your present by postal mail to:
       
	    Maria
	    examplestreet 2
	    1 example city
	    examplecountry

	Happy Holidays and best regards
	
	wichtel_bot
	
	(this is an auto-generated message)

Check each incoming mail and make sure, they include all the information you entered.

Have fun wichteling! :)
