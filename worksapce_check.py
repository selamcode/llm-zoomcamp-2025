import openai
from  dotenv import load_dotenv
import os # using for system

'''
we need this to help us load the .env file
pip install python-dotenv 

'''
# with out the openAI() function
'''
# Load variables from .env
load_dotenv()

# Get the key
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = api_key

'''

from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-3.5-turbo-1106",
    input="What is the capital city of France?"
)

print(response.output_text)
