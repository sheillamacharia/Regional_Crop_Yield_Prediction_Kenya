from flask import Flask, render_template, request
import pandas as pd
import pickle
import os

app = Flask(__name__)

# ----------------------------
# Load the fitted pipeline
# ----------------------------
model_path = os.path.join("model", "random_forest_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# ----------------------------
# Dropdown Options
# ----------------------------
regions = [
    "Baringo","Bomet","Bungoma","Busia","Elgeyo-Marakwet","Embu","Garissa",
    "Homa Bay","Isiolo","Kajiado","Kakamega","Kericho","Kiambu","Kilifi",
    "Kirinyaga","Kisii","Kisumu","Kitui","Kwale","Laikipia","Lamu",
    "Machakos","Makueni","Mandera","Marsabit","Meru","Migori","Mombasa",
    "Murang'a","Nairobi","Nakuru","Nandi","Narok","Nyamira","Nyandarua",
    "Nyeri","Samburu","Siaya","Taita Taveta","Tana River","Tharaka Nithi",
    "Trans Nzoia","Turkana","Uasin Gishu","Vihiga","Wajir","West Pokot"
]

items = ["Maize","Sorghum","Wheat","Rice","Tea","Sugarcane"]
seasons = ["Annual","Long"]

# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        regions=regions,
        items=items,
        seasons=seasons,
        prediction_text=""
    )

# ----------------------------
# Prediction Route
# ----------------------------

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Collect form inputs
        Region = request.form["Region"]
        Item = request.form["Item"]
        Year = int(request.form["Year"])
        season_name = request.form["season_name"]
        area = float(request.form["area"])
        production = float(request.form["production"])
        temperature = float(request.form["Temperature"])
        rainfall = float(request.form["Rainfall"])
        pesticides = float(request.form["Pesticides"])

        # Build input dataframe matching training features
        input_df = pd.DataFrame([{
            "Region": Region,
            "Item": Item,
            "season_name": season_name,
            "Year": Year,
            "area": area,
            "production": production,  
            "Rainfall - (MM)": rainfall,
            "Temperature - (Celsius)": temperature,
            "pesticides_hg_per_ha": pesticides
        }])

        # Make prediction
        prediction = model.predict(input_df)
        output = round(float(prediction[0]), 4)

        return render_template(
            "index.html",
            regions=regions,
            items=items,
            seasons=seasons,
            prediction_text=f"Predicted Yield: {output} tons/ha"
        )

    except Exception as e:
        return render_template(
            "index.html",
            regions=regions,
            items=items,
            seasons=seasons,
            prediction_text=f"Error: {str(e)}"
        )

if __name__ == "__main__":
    app.run(debug=True)

    # app.py completed


