import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import zscore
import os

# Create outputs directory if not exists
os.makedirs('outputs', exist_ok=True)

# Load data
df = pd.read_csv('data/climate_data.csv')
df['Date'] = pd.to_datetime(df['Date'])

print("Data loaded successfully. Shape:", df.shape)

# Data Cleaning
df.dropna(inplace=True)
print("After cleaning, shape:", df.shape)

# EDA
print("Summary Statistics:")
print(df.describe())

# Plot Temperature Trend
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Temperature_C'], label='Temperature')
plt.title('Temperature Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.savefig('outputs/temperature_trend.png')
plt.show()

# Rolling Average for Trend
df['Temp_Rolling'] = df['Temperature_C'].rolling(window=12).mean()
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Temperature_C'], alpha=0.5, label='Original')
plt.plot(df['Date'], df['Temp_Rolling'], color='red', label='Rolling Avg')
plt.title('Smoothed Temperature Trend')
plt.legend()
plt.savefig('outputs/smoothed_trend.png')
plt.show()

# Rainfall Distribution
plt.figure(figsize=(8, 6))
sns.histplot(df['Rainfall_mm'], bins=30)
plt.title('Rainfall Distribution')
plt.savefig('outputs/rainfall_distribution.png')
plt.show()

# Anomaly Detection
df['Temp_Z'] = zscore(df['Temperature_C'])
anomalies = df[df['Temp_Z'].abs() > 3]
print(f"Number of anomalies detected: {len(anomalies)}")
anomalies.to_csv('outputs/anomalies.csv', index=False)

# Plot Anomalies
plt.figure(figsize=(12, 6))
plt.scatter(df['Date'], df['Temperature_C'], alpha=0.5, label='Normal')
plt.scatter(anomalies['Date'], anomalies['Temperature_C'], color='red', label='Anomalies')
plt.title('Anomaly Detection in Temperature')
plt.legend()
plt.savefig('outputs/anomalies_plot.png')
plt.show()

# Forecasting with Linear Regression
df['Time_Index'] = np.arange(len(df))
X = df[['Time_Index']]
y = df['Temperature_C']

model = LinearRegression()
model.fit(X, y)
predictions = model.predict(X)
future_index = np.arange(len(df), len(df) + 12)
future_X = pd.DataFrame({'Time_Index': future_index})
future_pred = model.predict(future_X)

plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Temperature_C'], label='Actual')
plt.plot(df['Date'], predictions, label='Fitted', color='green')
future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=13, freq='ME')[1:]
plt.plot(future_dates, future_pred, label='Forecast', color='orange')
plt.title('Temperature Forecasting')
plt.legend()
plt.savefig('outputs/forecast.png')
plt.show()

print("Analysis complete. Outputs saved in outputs/ folder.")
print(f"MSE: {mean_squared_error(y, predictions):.2f}")