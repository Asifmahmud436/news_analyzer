from google import genai
import typing_extensions as typing
import os
import json
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))  

def get_news_category(item_text: str) -> list[str]: 
    class Category(typing.TypedDict):
        categories: list[typing.Literal[
        "AI", "Robotics", "Space", "Aeronautics", "Physics",
        "Engineering", "Biology", "Medical Science", "Environment", "Other"
        ]]

    prompt = f"""
        You are a strict multi-label classifier.

        Rules:
        - Pick ALL relevant categories
        - Maximum 3 categories
        - If unsure, include "Other"
        - Output JSON only

        News:
        {item_text}
    """


    try:
        response = client.models.generate_content( 
            model="gemini-2.0-flash", 
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Category, 
                "temperature": 0
            }
        )

        if response.parsed:
            return response.parsed["categories"]
        
        
        result = json.loads(response.text)
        return result["categories"]  


    except Exception as e:
        print(f"Error: {e}")
        return ["Other"]  

    
