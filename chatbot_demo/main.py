import os
import asyncio
from dotenv import load_dotenv

# Add Azure OpenAI package
from openai import AsyncAzureOpenAI

# Add flask
from flask import Flask, render_template, request, jsonify
import datetime

# logging and debugging
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get chatgpt configuration settings 
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

# Configure the Azure OpenAI client
client = AsyncAzureOpenAI(
   azure_endpoint = azure_oai_endpoint, 
   api_key=azure_oai_key,  
   api_version="2025-01-01-preview"
)

## flask app
app = Flask(__name__)

## get return content from Azure OpenAI model
async def get_completion(user_message):
   # local systen text
   system_text = open(file="system.txt", encoding="utf8").read().strip()

   # Get response from Azure OpenAI
   messages =[
   {"role": "system", "content": system_text},
   {"role": "user", "content": user_message},
   ]

   # call completion to get response
   response = await client.chat.completions.create(
      model=azure_oai_deployment,
      messages=messages,
      temperature=0.7,
      max_tokens=800
   )

   # return content as json format
   return response.choices[0].message.content


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
        
        ## call 
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
   # asyncio.run(cli_main())

