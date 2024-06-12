  # import libraries
import pandas as pd
from finvizfinance.quote import finvizfinance
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif
import requests

# get financial data
# list of stocks of interest
stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META']
data = []

# Define the specific features we want to evaluate
features_to_evaluate = ['Avg Volume', 'Rel Volume', 'Float', 'Price', 'Gap', 'Volume']
time_period_minutes = 390


for stock in stocks:
    try:
        stock_data = finvizfinance(stock).ticker_fundament()
        if 'Float' in stock_data and 'Volume' in stock_data:
            stock_data['Float per min'] = stock_data['Float'] / time_period_minutes
            stock_data['Volume per min'] = stock_data['Volume'] / time_period_minutes
            filtered_data = {key: stock_data[key] for key in features_to_evaluate + ['Float per min', 'Volume per min'] if key in stock_data}
        stock_data['Ticker'] = stock
        data.append(stock_data)
    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve data for {stock}: {e}")
    except Exception as e:
        print(f"An error occurred for {stock}: {e}")
        filtered_data = {key: stock_data[key] for key in features_to_evaluate if key in stock_data}
        filtered_data['Ticker'] = stock  # Add the ticker back in
        data.append(filtered_data)
    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve data for {stock}: {e}")
    except Exception as e:
        print(f"An error occurred for {stock}: {e}")


# convert list of dictionary to DataFrame if data is not empty
if data:
    df = pd.DataFrame(data)
else:
    print("No data to process")
    exit()

# preprocess the data
# drop rows with any missing values
df.dropna(inplace=True)

# separate features and target
X = df.drop(columns=['Ticker'])
y = df['Ticker']

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

# feature selection
# using SelectKBest to select top features based on ANOVA F-value
selector = SelectKBest(score_func=f_classif, k='all')  # adjust 'k' as needed
X_new = selector.fit_transform(X_processed, y)

# get selected feature names
selected_features = [all_features[i] for i in selector.get_support(indices=True)]

print("Selected Features (using SelectKBest):")
print(selected_features)

# can also use feature importance from RandomForest
rf = RandomForestClassifier()
rf.fit(X_processed, y)
importances = rf.feature_importances_
importance_df = pd.DataFrame({'Feature': all_features, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Feature Importances:")
print(importance_df)