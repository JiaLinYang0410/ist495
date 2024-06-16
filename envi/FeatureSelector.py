# Import necessary libraries
import os
import shutil
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from tabulate import tabulate
import requests

# Define the specific features we want to evaluate
features_to_evaluate = ['Avg Volume', 'Rel Volume', 'Float', 'Price', 'Gap', 'Volume']
time_period_minutes = 390

# Path to the Downloads folder
downloads_folder = os.path.expanduser("~/Downloads")

# Get current date and time
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Search for files starting with "finviz" and ending with ".csv"
file_found = False
for file_name in os.listdir(downloads_folder):
    if file_name.startswith("finviz") and file_name.endswith(".csv"):
        file_found = True
        file_path = os.path.join(downloads_folder, file_name)
        # Generate new filename with current datetime appended
        new_file_name = f"finviz_{current_datetime}.csv"
        new_file_path = os.path.join(downloads_folder, new_file_name)
        # Rename the file
        shutil.move(file_path, new_file_path)
        print(f"File renamed: {file_name} -> {new_file_name}")

        # Load the renamed CSV file into a DataFrame
        df = pd.read_csv(new_file_path)
        print("\nRaw data loaded from CSV:")
        print(tabulate(df.head(), headers='keys', tablefmt='psql'))
        break

if not file_found:
    print("No 'finviz' CSV files found in the Downloads folder.")
    exit()

# Preprocess the data
# Drop rows with any missing values
df.dropna(inplace=True)

# Separate features and target
# Assuming 'Ticker' is the target column
X = df.drop(columns=['Ticker'])
y = df['Change']

# Identify categorical and numeric columns
categorical_cols = X.select_dtypes(include=['object']).columns
numeric_cols = X.select_dtypes(include=['number']).columns

# Create a preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ]
)

# Apply the transformations
X_processed = preprocessor.fit_transform(X)

# Get feature names after preprocessing
num_features = numeric_cols
cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
all_features = num_features.to_list() + cat_features.tolist()

# Feature importance using RandomForest
rf = RandomForestClassifier()
rf.fit(X_processed, y)
importances = rf.feature_importances_
importance_df = pd.DataFrame({'Feature': all_features, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# Calculate 'Float per minute' and 'Volume per minute'
df['Volume_per_min'] = df['Volume'] / time_period_minutes


print("Feature Importances:")
print(importance_df)