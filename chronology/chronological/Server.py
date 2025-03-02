from flask import Flask, request, jsonify

from List_Generator import ask_openai

app = Flask(__name__)

@app.route("/ask_openai", methods=["POST"])
def ask_openai_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        result = ask_openai(
            data['place_of_interest'],
            data['current_interests'],
            data['budget'],
            data['weather_preference'],
            data['stay_duration'],
            data['numOfPeople'],
            data['food_preference']
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)