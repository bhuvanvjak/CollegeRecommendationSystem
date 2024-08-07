import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from flask import Flask, render_template, request, jsonify, Blueprint

app = Blueprint('canada', __name__)

# Load and preprocess data
data = pd.read_csv('canada100.csv')

# Impute missing GRE values with -1
data['Min. GRE (V+Q)'] = data['Min. GRE (V+Q)'].fillna(-1)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["Min. CGPA", "Min. TOEFL (iBT)", "Min. IELTS", "Min. GRE (V+Q)"]),
        ("cat", OneHotEncoder(handle_unknown='ignore'), [])
    ])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("knn", NearestNeighbors(n_neighbors=50, metric="euclidean"))
])

model.fit(data[["Min. CGPA", "Min. TOEFL (iBT)", "Min. IELTS", "Min. GRE (V+Q)"]])

def calculate_selection_percentage(row, cgpa, toefl, ielts, gre):
    cgpa_diff = (cgpa - row["Min. CGPA"]) / 0.5
    toefl_diff = (toefl - row["Min. TOEFL (iBT)"]) / 30
    ielts_diff = (ielts - row["Min. IELTS"]) / 1.0
    gre_diff = (gre - row["Min. GRE (V+Q)"]) / 40 if row["Min. GRE (V+Q)"] != -1 else 0
    avg_diff = min(max((cgpa_diff + toefl_diff + ielts_diff + gre_diff) / (3 + (1 if row["Min. GRE (V+Q)"] != -1 else 0)) * 100, 0), 100)
    return round(avg_diff, 2)

def recommend_universities(cgpa, toefl, ielts, gre, max_tuition):
    filtered_recommendations = data[
        (data["Min. CGPA"] <= cgpa) &
        (data["Min. TOEFL (iBT)"] <= toefl) &
        (data["Min. IELTS"] <= ielts) &
        ((data["Min. GRE (V+Q)"] <= gre) | (data["Min. GRE (V+Q)"] == -1)) &
        (data["Max Tuition Fee (INR)"] <= max_tuition)
    ]

    filtered_recommendations["Selection %"] = filtered_recommendations.apply(
        lambda row: calculate_selection_percentage(row, cgpa, toefl, ielts, gre), axis=1
    )

    # Sort by Selection % in descending order and limit to top 10
    filtered_recommendations = filtered_recommendations.sort_values("Selection %", ascending=False).head(10)

    # Convert to dictionary and handle NaN values
    result = filtered_recommendations[["Rank", "University", "Location", "Max Tuition Fee (INR)", "Selection %"]].to_dict(orient='records')
    
    for uni in result:
        for key, value in uni.items():
            if pd.isna(value):
                uni[key] = None  # Replace NaN with None, which will be converted to null in JSON
    
    return result

@app.route('/canada')
def index():
    return render_template('canada.html')

@app.route('/canada/recommend', methods=['POST'])
def recommend():
    try:
        cgpa = float(request.form['cgpa'])
        toefl = int(request.form['toefl'])
        ielts = float(request.form['ielts'])
        gre = int(request.form['gre']) if request.form['gre'] else -1
        max_tuition = int(float(request.form['max_tuition']) * 100000)  # Convert lakhs to INR

        print(f"Received data: CGPA={cgpa}, TOEFL={toefl}, IELTS={ielts}, GRE={gre}, Max Tuition={max_tuition}")

        recommendations = recommend_universities(cgpa, toefl, ielts, gre, max_tuition)
        
        if not recommendations:
            return jsonify({"error": "No universities found matching your criteria"}), 404
        
        return jsonify(recommendations)
    except ValueError as ve:
        print(f"ValueError in recommend function: {str(ve)}")
        return jsonify({"error": f"Invalid input: {str(ve)}"}), 400
    except Exception as e:
        print(f"Error in recommend function: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500