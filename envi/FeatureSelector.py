import os
import shutil
from datetime import datetime
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from tabulate import tabulate
import requests

# Function to fetch stock data from Finviz API
def fetch_stock_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.content  # Return raw content for CSV
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

# Main function to run the script
def main():
    # API URL with your specific filters and API token
    api_url = "https://elite.finviz.com/export.ashx?[allYourFilters]&auth=66ab7f6e-727b-4a46-b3dd-13f2b3ef2c07"
    
    # Fetch stock data
    data = fetch_stock_data(api_url)
    
    if data:
        # Write data to a CSV file
        with open("export.csv", "wb") as f:
            f.write(data)
        print("CSV file created successfully: export.csv")
    else:
        print("No data fetched.")
        return

    # Path to the current directory
    current_dir = os.getcwd()

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Rename the file
    new_file_name = f"finviz_{current_datetime}.csv"
    new_file_path = os.path.join(current_dir, new_file_name)
    shutil.move("export.csv", new_file_path)
    print(f"File renamed to: {new_file_name}")

    # Load the renamed CSV file into a DataFrame
    df = pd.read_csv(new_file_path)
    print("\nRaw data loaded from CSV:")
    print(tabulate(df.head(), headers='keys', tablefmt='psql'))

    # Reprocess the data
    # Drop rows with any missing values
    df.dropna(inplace=True)

    # Separate features and target
    # Assuming 'Change' is the target column
    X = df.drop(columns=['Change', 'Ticker', 'Company', 'No.'])
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
    rf = RandomForestClassifier(random_state=42)  # Set the random_state for consistent outputs
    rf.fit(X_processed, y)
    importances = rf.feature_importances_

    # Aggregate importances for categorical features
    cat_feature_importances = {}
    for i, col in enumerate(categorical_cols):
        start_idx = len(numeric_cols) + i * len(preprocessor.named_transformers_['cat'].categories_[i])
        end_idx = start_idx + len(preprocessor.named_transformers_['cat'].categories_[i])
        cat_feature_importances[col] = sum(importances[start_idx:end_idx])

    # Combine with numeric feature importances
    feature_importances = {**dict(zip(num_features, importances[:len(numeric_cols)])), **cat_feature_importances}

    # Create a DataFrame for importances
    importance_df = pd.DataFrame(list(feature_importances.items()), columns=['Feature', 'Importance'])
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    # Print feature importances
    print("Feature Importances:")
    print(tabulate(importance_df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()