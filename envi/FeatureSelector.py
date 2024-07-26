import pandas as pd
import requests
from io import StringIO
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

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
    # API URL with your specific filters and API token
    api_url = "https://elite.finviz.com/export.ashx?v=152&p=i1&f=cap_0.01to,geo_usa|china|france|europe|australia|belgium|canada|chinahongkong|germany|hongkong|iceland|japan|newzealand|ireland|netherlands|norway|singapore|southkorea|sweden|taiwan|unitedarabemirates|unitedkingdom|switzerland|spain,sh_curvol_o1000,sh_price_u50,sh_relvol_o5,ta_change_u&ft=4&o=-change&ar=10&c=0,1,2,6,25,85,30,31,84,61,63,64,67,65,66&auth=66b77c09-ec07-46b7-8b88-aabcae044aef"
    
    try:
        # Fetch stock data
        csv_data = fetch_stock_data(api_url)
        
        if csv_data:
            # Load the CSV data into a DataFrame
            df = pd.read_csv(StringIO(csv_data))
            
            # Display the first few rows of the dataframe to understand its structure
            print("Data preview:")
            print(df.head(20))
            
            # Drop rows with missing target values
            df = df.dropna(subset=['Change'])
            
            # Encode categorical features if any
            label_encoders = {}
            for column in df.select_dtypes(include=['object']).columns:
                label_encoders[column] = LabelEncoder()
                df[column] = label_encoders[column].fit_transform(df[column])
            
            # Separate features and target
            X = df.drop(columns=['Change', 'No.', 'Company', 'Ticker'])
            y = df['Change'].astype(float)
            
            # Train a Random Forest model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            # Extract feature importances
            importances = model.feature_importances_
            feature_names = X.columns
            
            # Create a DataFrame for feature importances
            feature_importances = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
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