import dotenv
import os
from openai import OpenAI

# Tested Using Python 3.12 Interpreter

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

try:
    client = OpenAI(api_key=api_key)
except Exception as error:
    raise SystemExit(f"Terminating: Failed to initialize OpenAI client. Error: {error}")

def ask_openai(place_of_interest: str, current_interests: list, budget: float, weather_preference: str,
               stay_duration: int, food_preference: str):
    if not place_of_interest:
        raise ValueError("Place of interest cannot be empty.")
    if not isinstance(current_interests, list) or not all(isinstance(i, str) for i in current_interests):
        raise ValueError("Current interests must be a list of strings.")
    if not isinstance(budget, (int, float)) or budget <= 0:
        raise ValueError("Budget must be a positive number.")
    if not weather_preference:
        raise ValueError("Weather preference cannot be empty.")
    if not isinstance(stay_duration, int) or stay_duration <= 0:
        raise ValueError("Stay duration must be a positive integer.")
    if not food_preference:
        raise ValueError("Food preference cannot be empty.")

    interests_str = ", ".join(current_interests)

    question = (f"I'm planning a {stay_duration}-day trip to {place_of_interest}. I enjoy {interests_str}, "
                f"prefer {weather_preference} weather, and have a budget of ${budget}. I also love {food_preference} cuisine. "
                f"What are the best recommendations do you have?""Provide only a list of places and their prices, making sure all of them add up to ${budget}."
                "Do not use general places, give specific places near the others spots within each day."
                "Try not to say anything before or after, assuring we recieve the list and prices only.""Attempt to use about 75% of the budget,"
                "leaving more for any spending. Feel free to change this percentage given the budget the person has."
                "As previously mentioned, do not include any general places, ONLY provide specific places near the others spots within each day."
                "Once you are done generating each day, under each of these days, provide a maps link with those places, making sure the link actually works"
                "and does not return an error.""If the user writes gibberish, please just write them a sweet message on how the dolphins are unhappy with them."
                "If the user puts in uncorrelated information for one of the inputs, ask them to please specify those inputs that are wrong.""Do not allow the user to input unrelated information for any of those inputs."
                "Analyze each response according to the input and question the correctness of the input, any suspicion of incorrectness can be denied.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=5000,
            top_p=1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error while communicating with OpenAI: {e}"

if __name__ == "__main__":
    place_of_interest = input("Where do you want to go? ").strip()
    raw_interests = input("What are your current interests?").strip()
    weather_preference = input("What kind of weather do you prefer?").strip()
    try:
        stay_duration = int(input("How many days will you stay? ").strip())
        if stay_duration <= 0:
            raise ValueError("Stay duration must be a positive number.")
    except ValueError:
        raise ValueError("Stay duration must be an integer value.")
    try:
        budget = float(input("What is your budget? ").strip())
    except ValueError:
        raise ValueError("Budget must be a numeric value.")
    food_preference = input("What type of food do you prefer? (e.g., Italian, Japanese, vegan, local cuisine) ").strip()

    current_interests = [interest.strip() for interest in raw_interests.split(",") if interest.strip()]

    travel_response = ask_openai(place_of_interest, current_interests, budget, weather_preference, stay_duration,
                          food_preference)
    print(travel_response)