# Step 1: Install and Import Libraries
# This line installs the 'yfinance' library, which is used to download stock data.
# The '!' tells the notebook to run this as a shell command.
!pip install yfinance

# These lines import the necessary Python libraries for our project.
# 'pandas' is for data manipulation (like working with tables).
# 'numpy' is for numerical operations, especially with arrays.
# 'yfinance' is our tool for getting financial data from Yahoo Finance.
# 'matplotlib.pyplot' is for creating plots and visualizations.
# 'scipy.stats' provides statistical functions, like the normal distribution.
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import norm

# ---

# Step 2: Get and Prepare the Stock Data

# We define the stock ticker, in this case, Apple (AAPL).
ticker = 'AAPL'

# We set the end date to today and calculate the start date to be exactly 5 years ago.
# 'DateOffset' is a smart tool that handles calendar rules (like leap years).
end_date = pd.to_datetime('today')
start_date = end_date - pd.DateOffset(years=5)

# This line downloads the historical stock data from Yahoo Finance.
# 'auto_adjust=True' is a key parameter that automatically adjusts the prices
# for corporate actions like stock splits and dividends, ensuring our data is accurate.
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

# This line calculates the daily percentage return for each day.
# It's like applying the formula (Today's Price - Yesterday's Price) / Yesterday's Price
# for every single row, which is much faster than using a loop.
data['Daily_Returns'] = data['Close'].pct_change()

# This line removes any rows with missing data (like the first day's return),
# which are created by the pct_change() function.
data.dropna(inplace=True)

# ---

# Step 3: Calculate VaR using the Historical Method

# The historical method assumes that past returns are a good indicator of future risk.
# We set our confidence level at 99%, meaning we want to find the worst loss
# that we would not expect to exceed 99% of the time.
confidence_level = 0.99

# This line finds the return value at the 1st percentile of our historical data.
# For a 99% confidence level, the tail of the distribution we care about is the worst 1%.
# This value represents our worst-case return with 99% confidence.
historical_var_return = np.percentile(data['Daily_Returns'], (1 - confidence_level) * 100)

# We assume a hypothetical portfolio value of $1 million.
portfolio_value = 1000000

# This converts the percentage return into a dollar amount.
historical_var_dollar = historical_var_return * portfolio_value

print("--- Historical VaR ---")
print(f"99% Historical VaR for {ticker}: {historical_var_dollar:,.2f} USD")

# ---

# Step 4: Calculate VaR using the Parametric Method

# The parametric method assumes that our returns follow a normal distribution.
# We calculate the mean and standard deviation from our historical data.
mean_return = data['Daily_Returns'].mean()
std_dev_return = data['Daily_Returns'].std()

# We find the Z-score that corresponds to our 99% confidence level.
# For a normal distribution, this is approximately -2.33 standard deviations from the mean.
# 'norm.ppf' gives us this exact value.
z_score = norm.ppf(1 - confidence_level)

# This is the core formula for Parametric VaR.
# It calculates the return at the point on the normal distribution curve that
# corresponds to the worst 1% of outcomes.
parametric_var_return = mean_return + z_score * std_dev_return

# We convert this VaR return into a dollar amount.
parametric_var_dollar = parametric_var_return * portfolio_value

print("\n--- Parametric VaR ---")
print(f"99% Parametric VaR for {ticker}: {parametric_var_dollar:,.2f} USD")

# ---

# Step 5: Visualize the Results

# We create a plot to visualize the distribution of our stock's returns.
plt.figure(figsize=(12, 8))
plt.hist(data['Daily_Returns'], bins=100, edgecolor='black', alpha=0.7)

# We add vertical dashed lines to the plot to show where our calculated VaR levels are.
# This makes it easy to see how both VaR methods fit the data.
plt.axvline(historical_var_return, color='red', linestyle='dashed', linewidth=2, label=f'Historical VaR ({confidence_level*100}%)')
plt.axvline(parametric_var_return, color='green', linestyle='dashed', linewidth=2, label=f'Parametric VaR ({confidence_level*100}%)')

# We add a title, labels, and a legend to make the plot professional and easy to understand.
plt.title(f'Daily Returns Distribution and VaR for {ticker}')
plt.xlabel('Daily Return')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.show()
