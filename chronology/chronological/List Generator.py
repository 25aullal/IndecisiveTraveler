import os

import dotenv
from openai import OpenAI

# Tested Using Python 3.12 Interpreter

dotenv.load_dotenv()

# Gets API Key Access
api_key = os.getenv("OPENAI_API_KEY")

# Test Out API Key
try:
    client = OpenAI(api_key=api_key)
except Exception as error:
    raise SystemExit(f"Terminating: Failed to initialize OpenAI client. Error: {error}")


# Variables Being Asked of For Prompt
def ask_openai(place_of_interest: str, current_interests: list, budget: float, weather_preference: str,
               stay_duration: int, numOfPeople: float, food_preference: str):
    #No Destination Error
    if not place_of_interest:
        raise ValueError("Place of interest cannot be empty.")

    #No Current Interests Error
    if not isinstance(current_interests, list) or not all(isinstance(i, str) for i in current_interests):
        raise ValueError("Current interests must be a list of strings.")

    #No Budget or Negative Budget Error
    if not isinstance(budget, (int, float)) or budget <= 0:
        raise ValueError("Budget must be a positive number.")

    #No Weather Preference Error
    if not weather_preference:
        raise ValueError("Weather preference cannot be empty.")

    #No Stay Duration Error
    if not isinstance(stay_duration, int) or stay_duration <= 0:
        raise ValueError("Stay duration must be a positive integer.")

    #No Food Preference Error
    if not food_preference:
        raise ValueError("Food preference cannot be empty.")

    # No Number of People or Not 1 Person Error
    if not isinstance(numOfPeople, (int, float)) or numOfPeople <= 0:
        raise ValueError("Must have more than one person on trip")

    interests_str = ", ".join(current_interests)

    question = (f"I'm planning a {stay_duration}-day trip to {place_of_interest}. I enjoy {interests_str}, "
                f"prefer {weather_preference} weather, and have a budget of ${budget}. I also love {food_preference} cuisine. I will be going with {numOfPeople} people."
                " Before anything, think about the amount of people going on this trip and whats appropriate both location and cost wise by what our inputs are. "
                f"After factoring that, what are the best recommendations do you have for going to in this place? ""Provide only a list of places and their prices, making sure all of them add up to ${budget}. "
                "Do not use general places, give specific places near the others spots within each day. ""Try to keep these places nearby each other, assuming no more than an hour of public transit at one sitting. "
                "Try not to say anything before or after, assuring we recieve the list and prices only. ""Attempt to use about 75% of the budget, "
                "leaving more for any spending. Feel free to change this percentage given the budget the person has. ""Think about possibly optimizing the trips so if the location is in an area, they can go somewhere else nearby "
                "As previously mentioned, do not include any general places, ONLY provide specific places near the others spots within each day. "
                "Once you are done generating each day, under each of these days, provide a maps link with those places, making sure the link actually works "
                "and does not return an error. ""If the user writes gibberish, please just write them a sweet message on how the dolphins are unhappy with them. "
                "If the user puts in uncorrelated information for one of the inputs, ask them to please specify those inputs that are wrong. ""Do not allow the user to input unrelated information for any of those inputs. "
                "Analyze each response according to the input and question the correctness of the input, any suspicion of incorrectness can be denied. "
                "Once you are done, give the response in an .html format so it can be paster well in a website. ""With this .html response, get rid of the html and body sections since we already have one. "
                "Only implement the parts that do not say anything html related, only start with our heading title, assuring getting rid of html, doctype, etc... only formatting for the text. Start with our list heading and do not include ''' or '''html before and after. "
                "With the response, put a recommendation of three hotels in close budget and include approximate prices per person for that stay""Make sure to add the amount of people in the title for ___ day trip to ____ with ____ people. ""Finally, assure that the map link"
                "is functional and does not encounter any errors when pressed.""At the end, include a total estimated cost breaking down estimated costs of the trip.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
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

    food_preference = input ("What type of food do you prefer?").strip()

    try:
        numOfPeople = float(input("How many people are going?"))
    except ValueError:
        raise ValueError("Must have at least one person on trip.")

    current_interests = [interest.strip() for interest in raw_interests.split(",") if interest.strip()]

    travel_response = ask_openai(place_of_interest, current_interests, budget, weather_preference, stay_duration, numOfPeople, food_preference)
    print(travel_response)