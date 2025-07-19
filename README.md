# College Recommendation System

A Python-based web application that helps students find suitable colleges based on their academic profiles and preferences using data-driven recommendation techniques.

## 🎯 Overview

The College Recommendation System assists students in navigating the complex college selection process by providing personalized recommendations. The system analyzes user inputs such as academic scores, location preferences, and program interests to suggest colleges that best match their requirements.

## ✨ Features

- **Personalized Recommendations**: Get college suggestions based on GRE/TOEFL scores, GPA, location preferences, and program interests
- **Data-Driven Approach**: Utilizes machine learning techniques to analyze and rank colleges
- **User-Friendly Web Interface**: Built with Flask for easy interaction and recommendation viewing
- **Comprehensive Data Analysis**: Includes Jupyter notebooks for exploring college datasets and deriving insights
- **Real-time Processing**: Instant recommendations based on user input

## 🏗️ Project Structure

```
CollegeRecommendationSystem/
│
├── mainapp.py             # Main Flask application file
├── canadaapp.py           # canada Flask application file
├── japanapp.py            # japan Flask application file
├── uk.app.py              # uk Flask application file
├── usapp.py               # usa Flask application file
├
├── README.md              # Project documentation
├
│
├── eval.py                # used to evaluate the model 
│   
│
├── data/                  # College datasets
│   ├── Canada100.csv           # College information
│   ├── Japan100.csv 
│   ├── Uk10.csv
│   └── usa100.csv
│
├── templates/             # HTML templates
│   ├── home.html                # landing page
│   ├── canada.html              # individual pages
│   ├── japan.html
│   ├── Uk.html
│   └── usa.html
│    
└── static/                # Static files
    ├── css/                    # Stylesheets
    ├── js/                     # JavaScript files
    └── images/                 # Images and icons
```
After the recent update all the css related to files is in html files not in static.

## 🚀 How It Works

1. **Data Collection**: Uses comprehensive college datasets with information on location, tuition, acceptance rates, and programs
2. **User Input**: Students provide academic details (GRE/TOEFL scores, GPA) and preferences (state, major) via web form
3. **Recommendation Engine**: Machine learning algorithm processes inputs and matches against college database using sophisticated filtering techniques
4. **Results Display**: Web interface shows ranked college recommendations with relevance scores and detailed information

### Detailed Model Architecture

The system employs a **content-based filtering** approach with machine learning algorithms to generate personalized recommendations:

#### **Algorithm Types:**

**1. K-Nearest Neighbors (KNN)**
- Treats user inputs and college attributes as feature vectors
- Calculates similarity using Euclidean or cosine distance
- Returns top-k colleges with closest profile matches
- Parameters: `n_neighbors`, distance metrics, and weighting schemes

**2. Custom Scoring Algorithm**
- Rule-based weighted scoring system
- Assigns points based on feature matches (GRE scores, location, major)
- Configurable weights reflecting user priorities
- Threshold-based filtering for minimum requirements

**3. Clustering-Based Approach**
- Groups colleges using k-means clustering
- Maps user profiles to nearest cluster
- Recommends colleges within matched clusters

#### **Feature Processing:**
- **Normalization**: Scales numerical features (GRE scores, tuition) to 0-1 range
- **Encoding**: One-hot encoding for categorical features (majors, locations)
- **Weighting**: Prioritizes features based on importance (academic fit: 40%, location: 30%, program: 30%)
- **Missing Data Handling**: Intelligent imputation and exclusion strategies

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Data Analysis**: Jupyter Notebooks
- **Frontend**: HTML, CSS, JavaScript
- **Database**: CSV datasets

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## ⚡ Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bhuvanvjak/CollegeRecommendationSystem.git
   cd CollegeRecommendationSystem
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Usage

1. Launch the web application
2. Enter your academic information:
   - GRE/TOEFL scores
   - GPA
   - Preferred state/location
   - Intended major/program
3. Submit the form to receive personalized college recommendations with match scores
4. Explore recommended colleges with detailed information and relevance rankings

## 📊 Dataset Information

The system uses comprehensive college datasets containing:

### **Core Features:**
- **College Name**: Unique identifier for each institution
- **Location**: State/city information for geographic preferences
- **Tuition Fees**: Cost of attendance for budget considerations
- **Acceptance Rate**: Selectivity indicators
- **Average GRE/TOEFL Scores**: Academic admission requirements
- **GPA Requirements**: Minimum/average GPA for admitted students
- **Programs/Majors**: Available academic programs (Computer Science, Engineering, etc.)
- **Additional Metrics**: Campus size, rankings, student-to-faculty ratios

### **Data Processing Pipeline:**
1. **Exploratory Data Analysis (EDA)** - Performed in Jupyter notebooks
2. **Data Cleaning** - Handle missing values and duplicates
3. **Feature Engineering** - Normalize numerical features and encode categories
4. **Model Training** - Parameter tuning and cross-validation

## 📓 Model Training & Evaluation

Explore the Jupyter notebooks in the `notebooks/` directory to understand:

### **Model Development Process:**
- **Exploratory Data Analysis (EDA)** - Statistical summaries and data visualization
- **Feature Engineering** - Data preprocessing and transformation techniques
- **Model Selection** - Comparison of KNN, scoring algorithms, and clustering approaches
- **Hyperparameter Tuning** - Grid search and cross-validation for optimal parameters
- **Performance Evaluation** - Using metrics like Precision@k and Mean Squared Error

### **Key Model Parameters:**
- **n_neighbors**: Number of similar colleges to recommend (typically 5-10)
- **Distance Metrics**: Euclidean, Manhattan, or cosine similarity
- **Feature Weights**: Adjustable importance scores for different attributes
- **Clustering Parameters**: Number of college groups for clustering-based recommendations

### **Model Assumptions & Limitations:**
- **Assumptions**: Comprehensive dataset, well-defined user inputs, prioritization of academic fit
- **Limitations**: Dataset currency, unique preferences handling, cold-start problem for new colleges

## 🔮 Future Enhancements

- [ ] **Advanced ML Models**: Implement collaborative filtering and neural networks
- [ ] **Expanded Dataset**: Include more colleges and detailed attributes
- [ ] **Mobile Optimization**: Responsive design for mobile devices
- [ ] **User Profiles**: Save user preferences for future recommendations
- [ ] **Real-time Data**: Integration with live college admission data
- [ ] **Social Features**: User reviews and ratings

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and commit (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



## 👥 Authors

- **@bhuvanvjak** - *Initial work* - [GitHub Profile](https://github.com/bhuvanvjak)
- **@AbhijeetRachuri** - *Assistance in Building* -[GitHub Profile](https://github.com/RachuriAbhijeeth)



---

⭐ **Star this repository if you found it helpful!**