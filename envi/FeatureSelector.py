def main():
    import os
    import shutil
    from datetime import datetime
    import pandas as pd
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from tabulate import tabulate

    # path to the downloads folder
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")

    # get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # search for files starting with "finviz" and ending with ".csv"
    file_found = False
    for file_name in os.listdir(downloads_folder):
        if file_name.startswith("finviz") and file_name.endswith(".csv"):
            file_found = True
            file_path = os.path.join(downloads_folder, file_name)

            # generate new filename with current datetime appended
            new_file_name = f"finviz_{current_datetime}.csv"
            new_file_path = os.path.join(downloads_folder, new_file_name)

            # rename the file
            shutil.move(file_path, new_file_path)
            print(f"File renamed: {file_name} -> {new_file_name}")

            # load the renamed CSV file into a DataFrame
            df = pd.read_csv(new_file_path)
            print("\nRaw data loaded from CSV:")
            print(tabulate(df.head(), headers='keys', tablefmt='psql'))
            break

    if not file_found:
        print("No 'finviz' CSV files found in the Downloads folder.")
        return

    # reprocess the data
    # drop rows with any missing values
    df.dropna(inplace=True)

    # exclude 'Company', 'No.', and 'Change' columns from features
    X = df.drop(columns=['Ticker', 'Company', 'No.', 'Change'])
    y = df['Change']

    # identify categorical and numeric columns
    categorical_cols = X.select_dtypes(include=['object']).columns
    numeric_cols = X.select_dtypes(include=['number']).columns

    # create a preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ]
    )

    # apply the transformations
    X_processed = preprocessor.fit_transform(X)

    # get feature names after preprocessing
    num_features = numeric_cols
    cat_features = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_cols)
    all_features = num_features.to_list() + cat_features.tolist()

    # feature importance using RandomForest
    rf = RandomForestClassifier(random_state=42)  # set the random_state for consistent outputs
    rf.fit(X_processed, y)
    importances = rf.feature_importances_

    # aggregate importances for categorical features
    cat_feature_importances = {}
    for i, col in enumerate(categorical_cols):
        start_idx = len(numeric_cols) + i * len(preprocessor.named_transformers_['cat'].categories_[i])
        end_idx = start_idx + len(preprocessor.named_transformers_['cat'].categories_[i])
        cat_feature_importances[col] = sum(importances[start_idx:end_idx])

    # combine with numeric feature importances
    feature_importances = {**dict(zip(num_features, importances[:len(numeric_cols)])), **cat_feature_importances}

    # create a DataFrame for importances
    importance_df = pd.DataFrame(list(feature_importances.items()), columns=['Feature', 'Importance'])
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    # print feature importances
    print("Feature Importances:")
    print(tabulate(importance_df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()
