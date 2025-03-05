from tavily import TavilyClient
from termcolor import colored, cprint
from dotenv import load_dotenv
import os

def write_result(result): 
    # Open the file in write mode ('w')
    with open("search.json", "w") as file:
        file.write(result)


load_dotenv()
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

result = tavily_client.search("current weather in Hildesheim, Germany ?")
write_result(result["results"][0]["content"])
cprint(result)