import matplotlib.pyplot as plt
# import numpy as np

def plot_results(df):
    fig, ax = plt.subplots(3, 1, figsize=(10,12))
    ax[0].plot(df['time(s)'], df['speed(km/h)'], color='blue')
    ax[0].set_title("Vehicle Speed Profile")
    ax[0].set_xlabel("Time (s)")
    ax[0].set_ylabel("Speed (km/h)")
    ax[0].grid(True)
    
    ax[1].plot(df['time(s)'], df['power'], color='red')
    ax[1].set_title("Power Output")
    ax[1].set_xlabel("Time (s)")
    ax[1].set_ylabel("Power (W)")
    ax[1].grid(True)

    ax[2].plot(df['time(s)'], df['cumulative_energy_kwh'], color='green')
    ax[2].set_title("Cumulative Energy Consumption")
    ax[2].set_xlabel("Time (s)")
    ax[2].set_ylabel("Energy (kWh)")
    ax[2].grid(True)
    
    plt.tight_layout()
    plt.show()