import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_climate_data(start_year=1950, end_year=2023, freq='ME'):
    """
    Generate synthetic climate data for demonstration purposes.
    Includes temperature, rainfall, humidity, and CO2 levels with seasonal patterns and trends.
    """
    # Create date range
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='ME')
    
    n = len(dates)
    
    # Base temperature with seasonal variation and long-term trend
    seasonal_temp = 15 + 10 * np.sin(2 * np.pi * np.arange(n) / 12)  # Seasonal cycle
    trend_temp = 0.01 * np.arange(n)  # Warming trend
    noise_temp = np.random.normal(0, 2, n)  # Random noise
    temperature = seasonal_temp + trend_temp + noise_temp
    
    # Rainfall with seasonal pattern
    seasonal_rain = 50 + 40 * np.sin(2 * np.pi * (np.arange(n) + 6) / 12)  # Peak in summer
    noise_rain = np.random.exponential(20, n)  # Exponential noise for rainfall
    rainfall = np.maximum(0, seasonal_rain + noise_rain)
    
    # Humidity correlated with rainfall
    humidity = 60 + 20 * np.sin(2 * np.pi * np.arange(n) / 12) + np.random.normal(0, 5, n)
    humidity = np.clip(humidity, 0, 100)
    
    # CO2 levels with increasing trend
    co2_base = 315  # Starting CO2 in ppm
    co2_trend = 1.5 * np.arange(n) / 12  # Increase over time
    co2_noise = np.random.normal(0, 1, n)
    co2 = co2_base + co2_trend + co2_noise
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Temperature_C': temperature,
        'Rainfall_mm': rainfall,
        'Humidity_%': humidity,
        'CO2_ppm': co2
    })
    
    # Add some anomalies
    anomaly_indices = np.random.choice(n, size=int(0.05 * n), replace=False)
    df.loc[anomaly_indices, 'Temperature_C'] += np.random.choice([-10, 10], len(anomaly_indices))
    
    return df

if __name__ == "__main__":
    df = generate_climate_data()
    df.to_csv('data/climate_data.csv', index=False)
    print("Synthetic climate data generated and saved to data/climate_data.csv")