from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from config.constant import *

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

def model_client():
    model_client = OpenAIChatCompletionClient(model=MODEL, api_key=api_key)
    return model_client