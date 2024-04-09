# discord-scraper
Get a .har file including discord messages (it's a list of http requests, access from your browser console)  
Note you will have to load all the messages you want to store during your browser session, oops  
python organize.py <.har file> generates the text of the messages, in order  
Doesn't keep embeds or attachments  
Recommended to only pull from one channel; they're not separate  
