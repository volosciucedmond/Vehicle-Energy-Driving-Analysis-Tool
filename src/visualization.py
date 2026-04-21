import matplotlib.pyplot as plt
import json

with open('data/car_data.json', 'r') as f:
    car_data = json.load(f)
# import numpy as np

def plot_results(df, vehicle_id):
    fig, ax = plt.subplots(3, 1, figsize=(10,12))
    ax[0].plot(df['time(s)'], df['speed(km/h)'], color='blue')
    ax[0].set_title(f"Vehicle Speed Profile {car_data[vehicle_id]['name']}")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Speed (km/h)")
    ax[0].grid(True)
    
    ax[1].plot(df['time(s)'], df['power'], color='red')
    ax[1].set_title(f"Power Output {car_data[vehicle_id]['name']}")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Power (W)")
    ax[1].grid(True)

    ax[2].plot(df['time(s)'], df['cumulative_energy_kwh'], color='green')
    ax[2].set_title(f"Cumulative Energy Consumption {car_data[vehicle_id]['name']}")
    ax[2].set_xlabel("Time (s)")
    ax[2].set_ylabel("Energy (kWh)")
    ax[2].grid(True)
    
    plt.tight_layout()
    plt.show()
    
def plot_efficiency_check(df, vehicle_name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot 1: The Power Tax
    ax1.plot(df['time(s)'], df['battery_power_w'] / 1000, label='Battery Power (kW)', alpha=0.7)
    ax1.plot(df['time(s)'], df['power'] / 1000, label='Mechanical Power (kW)', linestyle='--')
    ax1.set_ylabel('Power (kW)')
    ax1.set_title(f'Power Comparison & Efficiency Tax: {vehicle_name}')
    ax1.legend()
    ax1.grid(True)

    # Plot 2: Efficiency Changes
    ax2.plot(df['time(s)'], df['motor_efficiency'], color='green')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylim(0.6, 1.0) # Zoom in to see the changes
    ax2.set_title('Motor Efficiency Throughout Trip')
    ax2.grid(True)

    plt.tight_layout()
    plt.show()