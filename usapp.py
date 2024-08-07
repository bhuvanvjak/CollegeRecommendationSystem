import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestNeighbors
from flask import Flask, render_template, request, jsonify
from flask import Blueprint
import logging

app = Blueprint('usa', __name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load and preprocess data
try:
    data = pd.read_csv('usa100.csv')
    data['State'] = data['Location'].apply(lambda x: x.split()[-1])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), ["Min. CGPA (4.0 scale)", "Min. TOEFL (iBT)", "Min. GRE (V+Q)", "Min ILETS Score"]),
            ("cat", OneHotEncoder(handle_unknown='ignore'), ["State"])
        ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("knn", NearestNeighbors(n_neighbors=50, metric="euclidean"))
    ])

    model.fit(data[["Min. CGPA (4.0 scale)", "Min. TOEFL (iBT)", "Min. GRE (V+Q)", "State", "Min ILETS Score"]])
except Exception as e:
    logger.error(f"Error during data loading and preprocessing: {str(e)}")
    raise

def calculate_selection_percentage(row, cgpa, toefl, gre, ielts):
    cgpa_diff = (cgpa - row["Min. CGPA (4.0 scale)"]) / 0.5
    toefl_diff = (toefl - row["Min. TOEFL (iBT)"]) / 30 if toefl is not None else 0
    gre_diff = (gre - row["Min. GRE (V+Q)"]) / 40 if gre is not None else 0
    ielts_diff = (ielts - row["Min ILETS Score"]) / 2 if ielts is not None else 0
    
    provided_scores = [cgpa_diff, toefl_diff, gre_diff, ielts_diff]
    valid_scores = [diff for diff in provided_scores if diff != 0]
    avg_diff = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    
    avg_diff = min(max(avg_diff * 100, 0), 100)
    return round(avg_diff, 2)

def recommend_universities(cgpa, toefl, gre, ielts, state, max_tuition):
    filtered_recommendations = data[
        (data["Min. CGPA (4.0 scale)"] <= cgpa) &
        ((data["Min. TOEFL (iBT)"].isnull()) | (toefl is None) | (data["Min. TOEFL (iBT)"] <= toefl)) &
        ((data["Min. GRE (V+Q)"].isnull()) | (gre is None) | (data["Min. GRE (V+Q)"] <= gre)) &
        ((data["Min ILETS Score"].isnull()) | (ielts is None) | (data["Min ILETS Score"] <= ielts)) &
        (data["State"].str.lower() == state.lower()) &
        (data["Est. Annual Tuition (INR)"] <= max_tuition)
    ]

    filtered_recommendations["Selection %"] = filtered_recommendations.apply(
        lambda row: calculate_selection_percentage(row, cgpa, toefl, gre, ielts), axis=1
    )

    return filtered_recommendations[["Rank", "University", "Location", "Est. Annual Tuition (INR)", "Selection %"]].sort_values(["Selection %", "Rank"], ascending=[False, True])

@app.route('/')
@app.route('/usa')
def index():
    states = {
        'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',
        'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
        'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana',
        'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
        'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
        'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina',
        'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
        'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio',
        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
        'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont', 'WA': 'Washington',
        'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
    }
    return render_template('usa.html', states=states)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        cgpa = float(request.form['cgpa'])
        toefl = int(request.form['toefl']) if request.form['toefl'] else None
        gre = int(request.form['gre']) if request.form['gre'] else None
        ielts = float(request.form['ielts']) if request.form['ielts'] else None
        state = request.form['state'].split()[-1].strip('()')  # Extract state abbreviation
        max_tuition = int(float(request.form['max_tuition']) * 100000)  # Convert lakhs to INR

        logger.info(f"Recommending for CGPA: {cgpa}, TOEFL: {toefl}, GRE: {gre}, IELTS: {ielts}, State: {state}, Max Tuition: {max_tuition}")

        recommendations = recommend_universities(cgpa, toefl, gre, ielts, state, max_tuition)

        logger.info(f"Final recommendations:\n{recommendations}")
        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        logger.error(f"Error in recommend function: {str(e)}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)