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
        You are an expert multi-label news classifier specializing in scientific and technological topics.

        **Category Definitions:**
        - AI: Artificial intelligence, machine learning, neural networks, LLMs, computer vision
        - Robotics: Robots, automation, mechanical systems, autonomous vehicles
        - Space: Astronomy, space exploration, satellites, celestial bodies, space missions
        - Aeronautics: Aircraft, aviation, flight technology, aerospace engineering
        - Physics: Fundamental physics, quantum mechanics, particle physics, theoretical physics
        - Engineering: General engineering, civil, mechanical, electrical systems, infrastructure
        - Biology: Life sciences, genetics, ecology, evolution, organisms, biodiversity
        - Medical Science: Healthcare, medicine, diseases, treatments, pharmaceuticals, medical devices, human health
        - Environment: Climate, ecology, conservation, pollution, sustainability, natural resources
        - Other: Topics that don't fit the above categories

        **Classification Rules:**
        1. Assign ALL relevant categories (maximum 3)
        2. Be generous with medical content - if it mentions medicine, health, body, treatment, or diseases, include "Medical Science"
        3. Prioritize specific categories over "Other"
        4. Only use "Other" if NO other categories apply
        5. For ambiguous short texts, infer the most likely category based on keywords

        **Examples:**
        - "Medicine keeps our body safe" → ["Medical Science"]
        - "New cancer treatment approved" → ["Medical Science"]
        - "AI diagnoses diseases faster" → ["AI", "Medical Science"]
        - "SpaceX rocket lands on Mars" → ["Space", "Engineering"]
        - "Solar panels improve efficiency" → ["Engineering", "Environment"]

        **News Article:**
        {item_text}

        **Your task:** Return ONLY a JSON object with the categories array.
    """

    try:
        response = client.models.generate_content( 
            model="gemini-2.5-flash",  
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Category, 
                # "temperature": 0.1  
            }
        )

        if response.parsed:
            categories = response.parsed["categories"]

            if "Other" in categories and len(categories) > 1:
                categories.remove("Other")
            return categories if categories else ["Other"]
        
        result = json.loads(response.text)
        categories = result["categories"]
        if "Other" in categories and len(categories) > 1:
            categories.remove("Other")
        return categories if categories else ["Other"]

    except Exception as e:
        print(f"AI Classification Error: {e}")
        # Fallback: basic keyword matching
        return fallback_categorization(item_text)


def fallback_categorization(text: str) -> list[str]:
    """Simple keyword-based fallback if AI fails"""
    text_lower = text.lower()
    categories = []
    
    keywords = {
        "Medical Science": ["medicine", "medical", "health", "disease", "treatment", "doctor", 
                           "hospital", "patient", "drug", "pharmaceutical", "body", "cure"],
        "AI": ["ai", "artificial intelligence", "machine learning", "neural", "llm"],
        "Space": ["space", "rocket", "mars", "satellite", "astronomy", "planet"],
        "Robotics": ["robot", "automation", "autonomous"],
        "Biology": ["biology", "genetic", "organism", "species", "evolution"],
        "Environment": ["climate", "environment", "pollution", "sustainability"],
        "Physics": ["physics", "quantum", "particle", "energy"],
        "Engineering": ["engineering", "infrastructure", "construction"],
        "Aeronautics": ["aircraft", "aviation", "airplane", "flight"]
    }
    
    for category, words in keywords.items():
        if any(word in text_lower for word in words):
            categories.append(category)
            if len(categories) >= 3:
                break
    
    return categories if categories else ["Other"]