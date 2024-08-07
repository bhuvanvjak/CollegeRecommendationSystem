import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('usa100.csv')

# Preprocess the data
data['State'] = data['Location'].apply(lambda x: x.split()[-1])

# Define features and target
X = data[["Min. CGPA (4.0 scale)", "Min. TOEFL (iBT)", "Min. GRE (V+Q)", "State", "Min ILETS Score"]]
y = data["Rank"]  # Using Rank as the target variable for this example

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["Min. CGPA (4.0 scale)", "Min. TOEFL (iBT)", "Min. GRE (V+Q)", "Min ILETS Score"]),
        ("cat", OneHotEncoder(handle_unknown='ignore'), ["State"])
    ])

# Define algorithms
algorithms = {
    'KNN': KNeighborsClassifier(n_neighbors=5),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Logistic Regression': LogisticRegression(),
    'SVM': SVC(),
    'XGBoost': XGBClassifier()
}

# Function to calculate precision and recall at k
def precision_recall_at_k(y_true, y_pred, k=10):
    top_k_pred = np.argsort(y_pred)[:k]
    top_k_true = np.argsort(y_true)[:k]
    true_positives = len(set(top_k_pred) & set(top_k_true))
    precision = true_positives / k
    recall = true_positives / len(top_k_true)
    return precision, recall

# Evaluate algorithms
results = {}
for name, algorithm in algorithms.items():
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', algorithm)
    ])
    
    # Fit the pipeline
    pipeline.fit(X_train, y_train)
    
    # Make predictions
    y_pred = pipeline.predict(X_test)
    
    # Calculate metrics
    precision, recall = precision_recall_at_k(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Store results
    results[name] = {
        'Precision@10': precision,
        'Recall@10': recall,
        'F1-score': f1
    }

# Print results
for name, metrics in results.items():
    print(f"{name}:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    print()

# Plotting
metrics = ['Precision@10', 'Recall@10', 'F1-score']
x = np.arange(len(algorithms))
width = 0.25

fig, ax = plt.subplots(figsize=(12, 6))

for i, metric in enumerate(metrics):
    values = [results[alg][metric] for alg in algorithms]
    ax.bar(x + i*width, values, width, label=metric)

ax.set_ylabel('Scores')
ax.set_title('Algorithm Comparison')
ax.set_xticks(x + width)
ax.set_xticklabels(algorithms.keys(), rotation=45)
ax.legend()

plt.tight_layout()
plt.show()