import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from flask import Blueprint, render_template, request, jsonify

app = Blueprint('uk', __name__)

# Load and preprocess data
data = pd.read_csv('Data/uk10.csv')

# Convert degree class to numerical values
degree_class_map = {'Third Class': 1, 'Lower Second (2:2)': 2, 'Upper Second (2:1)': 3}
data['Min. Degree Class'] = data['Min. Degree Class'].map(degree_class_map)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["Min. CGPA (4.0 scale)", "Min. IELTS", "Min. TOEFL (iBT)", "Min. PTE Academic", "Min. Degree Class"]),
        ("cat", OneHotEncoder(handle_unknown='ignore'), [])
    ])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("knn", NearestNeighbors(n_neighbors=50, metric="euclidean"))
])

model.fit(data[["Min. CGPA (4.0 scale)", "Min. IELTS", "Min. TOEFL (iBT)", "Min. PTE Academic", "Min. Degree Class"]])

def calculate_admission_probability(row, cgpa, ielts, toefl, pte):
    factors = [
        (cgpa - row["Min. CGPA (4.0 scale)"]) / 0.5,
        (ielts - row["Min. IELTS"]) / 0.5,
        (toefl - row["Min. TOEFL (iBT)"]) / 5,
        (pte - row["Min. PTE Academic"]) / 5
    ]
    avg_factor = np.mean([f for f in factors if f > 0])
    return min(max(avg_factor * 0.25, 0), 1)  # Limit probability between 0 and 1

def recommend_universities(cgpa, ielts, toefl, pte, degree_class, max_tuition):
    filtered_recommendations = data[
        (data["Min. CGPA (4.0 scale)"] <= cgpa) &
        (data["Min. IELTS"] <= ielts) &
        (data["Min. TOEFL (iBT)"] <= toefl) &
        (data["Min. PTE Academic"] <= pte) &
        (data["Min. Degree Class"] <= degree_class_map[degree_class]) &
        (data["Max Tuition Fee (INR)"] <= max_tuition)
    ]

    filtered_recommendations['Admission Probability'] = filtered_recommendations.apply(
        lambda row: calculate_admission_probability(row, cgpa, ielts, toefl, pte), axis=1
    )

    sorted_recommendations = filtered_recommendations.sort_values('Admission Probability', ascending=False)

    return sorted_recommendations[["Rank", "University", "Max Tuition Fee (INR)", "Admission Probability"]].head(10)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        cgpa = float(request.form['cgpa'])
        ielts = float(request.form['ielts'])
        toefl = int(request.form['toefl'])
        pte = int(request.form['pte'])
        degree_class = request.form['degree_class']
        max_tuition = int(request.form['max_tuition']) * 100000  # Convert lakhs to INR

        recommendations = recommend_universities(cgpa, ielts, toefl, pte, degree_class, max_tuition)
        
        if recommendations.empty:
            return jsonify([]), 200
        
        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        print(f"Error in recommend function: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500

@app.route('/')
def index():
    return render_template('uk.html')
