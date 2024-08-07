import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask import Blueprint

app= Blueprint('japan', __name__)



# Load and preprocess data
try:
    data = pd.read_csv('japan100.csv')
    locations = data['Location'].unique().tolist()
except Exception as e:
    print(f"Error loading CSV file: {e}")
    data = pd.DataFrame()
    locations = []

def calculate_selection_percentage(row, cgpa, jlpt, eju, toefl):
    cgpa_diff = (cgpa - row["Min. CGPA"]) / 0.5
    jlpt_diff = row["Min. JLPT"] == "N1"
    eju_diff = (eju - row["Min. EJU (Japan & World)"]) / 50
    toefl_diff = (toefl - row["Min. TOEFL (iBT)"]) / 30
    avg_diff = min(max((cgpa_diff + jlpt_diff + eju_diff + toefl_diff) / 4 * 100, 0), 100)
    return round(avg_diff, 2)

def recommend_universities(cgpa, jlpt, eju, toefl, max_tuition, location):
    print(f"Recommending for CGPA: {cgpa}, JLPT: {jlpt}, EJU: {eju}, TOEFL: {toefl}, Max Tuition: {max_tuition}, Location: {location}")

    filtered_recommendations = data[
        (data["Min. CGPA"] <= cgpa) &
        (data["Min. JLPT"].isin(["N1", "N2", "N3", "N4", "N5"]) & (data["Min. JLPT"].str.contains(jlpt.upper()))) &
        (data["Min. EJU (Japan & World)"] <= eju) &
        (data["Min. TOEFL (iBT)"] <= toefl) &
        (data["Min. Annual Fee (INR)"] <= max_tuition) &
        (data["Location"] == location)
    ]

    print(f"Filtered recommendations:\n{filtered_recommendations}")

    if filtered_recommendations.empty:
        return pd.DataFrame()

    filtered_recommendations["Selection %"] = filtered_recommendations.apply(
        lambda row: calculate_selection_percentage(row, cgpa, jlpt, eju, toefl), axis=1
    )

    return filtered_recommendations[["Rank", "University", "Location", "Min. Annual Fee (INR)", "Selection %"]].sort_values(["Selection %", "Rank"], ascending=[False, True])

@app.route('/')
def home():
    return render_template('japan.html', locations=locations)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        cgpa = float(request.form['cgpa'])
        jlpt = request.form['jlpt']
        eju = int(request.form['eju'])
        toefl = int(request.form['toefl'])
        max_tuition = int(request.form['max_tuition'])
        location = request.form['location']

        recommendations = recommend_universities(cgpa, jlpt, eju, toefl, max_tuition, location)

        if recommendations.empty:
            return jsonify({"error": "No universities found matching your criteria"}), 404

        print(f"Final recommendations:\n{recommendations}")
        return jsonify(recommendations.to_dict(orient='records'))
    except Exception as e:
        print(f"Error in recommend route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)