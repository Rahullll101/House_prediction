"""
Flask server for Bengaluru House Price Prediction API
with OpenAI GPT description generation.
"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# === OpenAI API Setup ===

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# === Flask App ===
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def index():
    """Health check endpoint."""
    return "🏠 Bengaluru House Price Prediction API is running with OpenAI!"


@app.route("/get_location_names", methods=["GET"])
def get_location_names():
    """Get available location names from the trained model."""
    try:
        locations = util.get_location_names()
        return jsonify({"locations": locations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    """Predict house price and generate a property description."""
    try:
        data = request.get_json()
        print("Incoming request:", data)

        # Extract input values with defaults
        total_sqft = float(data.get("total_sqft", 1000))
        bath = int(data.get("bath", 2))
        bhk = int(data.get("bhk", 2))
        built_year = int(data.get("built_year", 2015))
        property_age = int(data.get("property_age", 5))
        area_type = data.get("area_type", "Built-up Area")
        availability = data.get("availability", "Ready To Move")
        location = data.get("location", "1st Phase JP Nagar")
        nearby_metro = data.get("nearby_metro", "Yes")
        age_segment = data.get("age_segment")

        # Auto-calculate age segment
        if not age_segment:
            if property_age <= 5:
                age_segment = "New"
            elif property_age <= 15:
                age_segment = "Mid"
            else:
                age_segment = "Old"

        # Predict price using util
        price = util.get_estimated_price(
            total_sqft, bath, bhk, built_year, property_age,
            area_type, availability, location, nearby_metro, age_segment
        )

        # Prepare payload for GPT description
        payload = {
            "location": location,
            "total_sqft": total_sqft,
            "bhk": bhk,
            "bath": bath,
            "area_type": area_type,
            "age_segment": age_segment,
            "availability": availability,
            "nearby_metro": nearby_metro,
            "built_year": built_year,
            "property_age_years": property_age,
            "estimated_price_lakhs": price
        }

        description = "Description unavailable"
        try:
            prompt = (
                "You are a professional real estate agent in Bengaluru.\n"
                "Write a short, engaging description for this property using these details:\n"
                f"{json.dumps(payload, indent=2)}\n"
                "Rules:\n"
                "- Mention the estimated price in Lakhs.\n"
                "- Keep it under 50 words.\n"
                "- Be professional and clear."
            )

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for real estate descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=100
            )

            description = response.choices[0].message["content"].strip()

        except Exception as e:
            print(f"OpenAI Error: {e}")

        return jsonify({
            "estimated_price_lakhs": price,
            "description": description
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("Starting Flask server for Bengaluru House Price Prediction...")
    util.load_saved_artifacts()
    app.run(host="0.0.0.0", port=5000, debug=True)
