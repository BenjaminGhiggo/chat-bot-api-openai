import openai
from dotenv import load_dotenv
model_info = openai.Model.retrieve("o1-mini")
print(model_info)
