# Stock Data Analysis with Random Forest

This repository contains a Python script that fetches stock data from the Finviz API, processes it, and uses a Random Forest Regressor to determine feature importances.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Description](#description)
- [API URL](#api-url)
- [Feature Engineering](#feature-engineering)
- [Model Training](#model-training)
- [Output](#output)

## Requirements

- Python 3.x
- pandas
- requests
- scikit-learn

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/stock-data-analysis.git
    ```
2. Navigate to the project directory:
    ```sh
    cd stock-data-analysis
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```sh
    python FeatureSelector.py
    ```

## Description

The script performs the following tasks:
1. Fetches stock data from the Finviz API.
2. Loads the data into a pandas DataFrame.
3. Performs feature engineering by calculating `Float_per_minute`, `Volume_per_minute`, and `Volume_per_Float_ratio`.
4. Previews the first few rows of the DataFrame.
5. Encodes categorical features.
6. Trains a Random Forest Regressor model to predict the `Change` column.
7. Outputs feature importances.

## API URL

The script uses a specific API URL with filters to fetch the stock data. Make sure you have access to the Finviz Elite API and have the correct API token.

```python
api_url = "https://elite.finviz.com/export.ashx?v=152&p=i1&f=cap_0.001to,geo_usa|china|france|europe|australia|belgium|canada|chinahongkong|germany|hongkong|iceland|japan|newzealand|ireland|netherlands|norway|singapore|southkorea|sweden|taiwan|unitedarabemirates|unitedkingdom|switzerland|spain,sh_curvol_o100,sh_relvol_o2,ta_change_u&ft=4&o=-change&ar=10&c=1,6,24,25,85,26,27,28,29,30,31,84,50,51,83,61,63,64,67,65,66,71&auth=YOUR_API_TOKEN"
