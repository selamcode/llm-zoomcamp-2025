import openai # if we don't use OpenAI
from  dotenv import load_dotenv
import os # if we don't use OpenAI

from openai import OpenAI

'''
we need this to help us load the .env file
pip install python-dotenv 

'''
# Load variables from .env
load_dotenv()

# with out the openAI() function
'''
# Get the key
api_key = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = api_key

'''

client = OpenAI()

response = client.responses.create(
    model="gpt-3.5-turbo-1106",
    input="What is the capital city of France?"
)

print(response.output_text)
