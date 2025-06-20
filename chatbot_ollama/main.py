import os
import asyncio
from dotenv import load_dotenv

# Add flask
from flask import Flask, render_template, request, jsonify
import datetime

# logging and debugging
import logging

# Add ollama 
from ollama import AsyncClient

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


## flask app
app = Flask(__name__)

## get return content from Azure OpenAI model
async def get_completion(user_message):
   message = {"role": "user", "content": user_message}
   
   # Get response from AsyncClient.chat
   response = await AsyncClient().chat(model='deepseek-llm', messages=[message])

   # return content as json format
   return response.message.content


# Root Route: load index page
@app.route("/")
def chatbot():

   return render_template('chatbot.html')

# Chat Route: handle user input and return response
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('user_message', '').strip()
        
        ## call async chat
        response = asyncio.run(get_completion(user_message))
        
        return jsonify({
            'bot_reply': response
        })

    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        return jsonify({
            'bot_reply': "An error occurred. Please try again.",
            'error_details': str(e)
        }), 500

# launch webservice 
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True) #Defining IP and port. (Host IP on network)

