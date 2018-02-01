## Chatbot ( Artificial Intelligence Assignment )
Group details 
Afroz Ahamad : 2015A7PS0119H
Keval Morabia: 2015A7PS0143H
Nikhil Joshi : 2015A7PS0179H


Chat bot responding to five endpoints:      
	- index => welcome    
	- / => atomic patters    
	- weather    
	- computers    
	- eateries (knowledge-base yet to be added)    

Weather data collected from forecast.io    

Secret key is inside the code itself.
> Remove secret key before making repo public

Also added is a sample response from forecast.io inside `templates/*.weather` file. Use that to parse sensible data to be returned by the chat bot.

### Running

```$ python3 chatbot.py```

This will spin up the flask server. Make requests to the endpoints to get response.

Making requests: [Postman](https://www.getpostman.com/)


