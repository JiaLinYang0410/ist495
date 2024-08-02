import pandas as pd
import requests
from io import StringIO
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.inspection import permutation_importance
from datetime import datetime

# Function to fetch stock data from Finviz API
def fetch_stock_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.content.decode('utf-8')  # Decode content for CSV
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None

# Main function to run the script
def main():
    # API URL with specific filters and API token
    api_url = "https://elite.finviz.com/export.ashx?v=152&p=i1&f=cap_0.001to,geo_usa|china|france|europe|australia|belgium|canada|chinahongkong|germany|hongkong|iceland|japan|newzealand|ireland|netherlands|norway|singapore|southkorea|sweden|taiwan|unitedarabemirates|unitedkingdom|switzerland|spain,sh_curvol_o100,sh_relvol_o2,ta_change_u&ft=4&o=-change&ar=10&c=1,6,24,25,85,26,27,28,29,30,31,84,50,51,83,61,63,64,67,65,66,71&auth=5055b82c-04c9-4a4a-84b5-4db7da1a5091"
    
    try:
        # Fetch stock data
        csv_data = fetch_stock_data(api_url)
        
        if csv_data:
            # Load the CSV data into DataFrame
            df = pd.read_csv(StringIO(csv_data))
            
            # Dynamic observation time
            observation_time = datetime.now()
            start_time = datetime.strptime('4:00 AM', '%I:%M %p').replace(year=observation_time.year, month=observation_time.month, day=observation_time.day)
            time_difference = (observation_time - start_time).total_seconds() / 60  # Total minutes
            
            # Calculate float per minute & volume per minute based on the dynamic observation time
            if 'Shares Float' in df.columns and 'Volume' in df.columns:
                df['Float_per_minute'] = df['Shares Float'] / 12 / 60
                df['Float_at_observation'] = df['Float_per_minute'] * time_difference
                df['Volume_per_minute'] = df['Volume'] / time_difference
                df['Volume_per_Float_ratio'] = df['Volume'] / df['Float_at_observation']
                df['Exceed_Supply'] = df['Volume_per_Float_ratio'] > 1
            else:
                print("Warning: 'Shares Float' or 'Volume' column(s) not found in the data.")
            
            # Display the first few rows of the dataframe to understand its structure
            preview_columns = ['Ticker', 'Change', 'Market Cap', 'Short Ratio', 'Short Interest', 'Volume', 'Float %', 'Shares Float', 'Gap', 'Average Volume', 'Relative Volume', 'Price', 'Float_per_minute', 'Volume_per_minute', 'Volume_per_Float_ratio', 'Exceed_Supply']
            # Ensure the preview columns exist in the DataFrame
            preview_columns = [col for col in preview_columns if col in df.columns]
            print("Data preview:")
            print(df[preview_columns].head(20))
            
            # Drop rows with missing target values
            df = df.dropna(subset=['Change'])
            
            # Encode categorical features if any
            label_encoders = {}
            for column in df.select_dtypes(include=['object']).columns:
                label_encoders[column] = LabelEncoder()
                df[column] = label_encoders[column].fit_transform(df[column])
            
            # Separate features and target
            X = df.drop(columns=['Change', 'Exceed_Supply', 'Ticker'])
            y = df['Change'].astype(float)
            
            # Train a Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Extract feature importances using permutation importance
            result = permutation_importance(model, X, y, n_repeats=10, random_state=42, n_jobs=2)
            sorted_idx = result.importances_mean.argsort()
            
            # Create a DataFrame for feature importances
            feature_importances = pd.DataFrame({'Feature': X.columns[sorted_idx], 'Importance': result.importances_mean[sorted_idx]})
            feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
            
            # Display the feature importances
            print("\nFeature importances:")
            print(feature_importances)
        else:
            print("No data fetched.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()