import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Setting the Seaborn style to dark
plt.style.use("dark_background")

# Generate dummy data for demand response
np.random.seed(42)

# Time series data
time_index = pd.date_range(start='2024-01-01', periods=24, freq='H')

# Dummy electricity prices (higher during peak hours)
prices = np.random.normal(loc=50, scale=10, size=24)
prices[8:20] += 50  # Simulating higher prices during peak hours (8 AM to 8 PM)

# Dummy energy consumption (higher during day)
consumption = np.random.normal(loc=100, scale=20, size=24)
consumption[8:20] += 50  # Simulating higher consumption during the day

# Creating a DataFrame
data = pd.DataFrame({'Price': prices, 'Consumption': consumption}, index=time_index)

# AI-based demand response algorithm to shift consumption to off-peak hours
def demand_response(consumption, prices):
    adjusted_consumption = consumption.copy()
    peak_hours = (prices > 70)
    off_peak_hours = ~peak_hours

    peak_consumption = consumption[peak_hours].sum()
    off_peak_slots = off_peak_hours.sum()

    shift_amount = peak_consumption / off_peak_slots * 0.1  # Shift 10% of peak consumption to off-peak

    adjusted_consumption[peak_hours] *= 0.9
    adjusted_consumption[off_peak_hours] += shift_amount

    return adjusted_consumption

# Streamlit app layout
st.title('Energy Demand Response AI Demo')

# Display initial graphs
st.header('Electricity Prices')
fig1, ax1 = plt.subplots()
sns.lineplot(x=data.index.hour, y=data['Price'], ax=ax1, color='cyan', marker='o', label='Electricity Price')
ax1.set_facecolor('#2E2E2E')
ax1.set_ylabel('Price ($)', color='white')
ax1.set_xlabel('Hour', color='white')
ax1.set_xticks(data.index.hour)
ax1.tick_params(axis='x', colors='white')
ax1.tick_params(axis='y', colors='white')
ax1.legend()
fig1.tight_layout()
st.pyplot(fig1)

st.header('Consumption on That Day')
fig2, ax2 = plt.subplots()
sns.lineplot(x=data.index.hour, y=data['Consumption'], ax=ax2, color='magenta', marker='o', label='Consumption')
ax2.set_facecolor('#2E2E2E')
ax2.set_ylabel('Consumption (kWh)', color='white')
ax2.set_xlabel('Hour', color='white')
ax2.set_xticks(data.index.hour)
ax2.tick_params(axis='x', colors='white')
ax2.tick_params(axis='y', colors='white')
ax2.legend()
fig2.tight_layout()
st.pyplot(fig2)

# Button to apply demand response AI
if st.button('Apply Demand Response AI'):
    data['Adjusted Consumption'] = demand_response(data['Consumption'], data['Price'])

    # Display adjusted consumption graph
    st.header('Adjusted Consumption After Demand Response')
    fig3, ax3 = plt.subplots()
    sns.lineplot(x=data.index.hour, y=data['Consumption'], ax=ax3, color='magenta', marker='o', label='Original Consumption')
    sns.lineplot(x=data.index.hour, y=data['Adjusted Consumption'], ax=ax3, color='lime', marker='o', linestyle='--', label='Adjusted Consumption')
    ax3.set_facecolor('#2E2E2E')
    ax3.set_ylabel('Consumption (kWh)', color='white')
    ax3.set_xlabel('Hour', color='white')
    ax3.set_xticks(data.index.hour)
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.legend()
    fig3.tight_layout()
    st.pyplot(fig3)

