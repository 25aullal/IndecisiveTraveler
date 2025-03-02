from flask import Flask, request, jsonify

from List_Generator import ask_openai

app = Flask(__name__)


@app.route("/ask_openai", methods=["GET"])
def ask_openai():
    data = request.json
    """
    data = {
    "place_of_interest}: xxx,
    curren_interest: xxx
    }
    """
    result = ask_openai(data.place_of_interest, data.current_interests, data.budget, data.weather_preference,
                        data.stay_duration, data.numOfPeople, data.food_preference)
    # (place_of_interest, current_interests, budget, weather_preference, stay_duration, numOfPeople, food_preference)
    return jsonify((result))


app.run()
