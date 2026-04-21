import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

time = []
speed = []
acceleration = []
slope = []

def generate_detailed_wltp(duration_sec=1800):
    """
    Generates a detailed WLTP-style DataFrame with physics calculations.
    """
    # 1. Generate Time Axis (1 Hz)
    time = np.arange(0, duration_sec + 1)
    
    # 2. Generate/Load Speed Profile (km/h)
    # Note: For production, replace this with: speed_kmh = pd.read_csv('wltp.csv')
    # Here we create a synthetic 4-phase profile for demonstration
    speed_kmh_raw = simulate_wltp_phases(time)
    speed_series = pd.Series(speed_kmh_raw)
    
    speed_kmh = speed_series.rolling(window=20, min_periods=1, center=True).mean().to_numpy()
    
    # 3. Calculate Acceleration (m/s^2)
    # Conversion: 1 km/h = 1/3.6 m/s
    speed_ms = speed_kmh / 3.6
    # acceleration = dv/dt. Since dt = 1s, it's just the difference.
    acceleration = np.diff(speed_ms, prepend=0)
    
    # 4. Generate Realistic Slope (-4 to 4)
    # Instead of pure random, we use a 'Random Walk' to simulate hills
    slope = generate_realistic_slope(len(time))
    
    # 5. Build DataFrame
    df = pd.DataFrame({
        'time(s)': time,
        'speed(km/h)': np.round(speed_kmh, 2),
        'acceleration(m/s²)': np.round(acceleration, 4),
        'slope(%)': slope
    })
    
    df.to_csv('data/wltp_drive_cycle.csv', index=False)
    
    return df

def simulate_wltp_phases(time):
    """Simulates the 4 speed phases of a WLTP Class 3 cycle."""
    # This is a simplified mathematical representation of the WLTP curve
    low = 20 * np.sin(time[:400] * 0.02) + 15
    med = 30 * np.sin(time[400:800] * 0.015) + 40
    high = 40 * np.sin(time[800:1300] * 0.01) + 70
    ex_high = 20 * np.sin(time[1300:] * 0.008) + 100
    
    profile = np.concatenate([low, med, high, ex_high])
    # Ensure no negative speeds and start/end at 0
    profile = np.clip(profile, 0, 131.3)
    profile[0:10] = 0
    profile[-10:] = 0
    return profile[:len(time)]

def generate_realistic_slope(length):
    """Generates a slope that changes gradually between -4 and 4."""
    slope = [0]
    for _ in range(length - 1):
        # 10% chance to change slope by 1 unit
        change = np.random.choice([-1, 0, 1], p=[0.05, 0.90, 0.05])
        new_slope = np.clip(slope[-1] + change, -4, 4)
        slope.append(new_slope)
    return slope

# --- Execution and Visualization ---
df_wltp = generate_detailed_wltp()

# Displaying first few rows
print("WLTP Data Preview:")
print(df_wltp.head(10))

# Visualizing the Result
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Speed (km/h)', color='tab:blue')
ax1.plot(df_wltp['time(s)'], df_wltp['speed(km/h)'], color='tab:blue', label='Speed')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Slope', color='tab:red')
ax2.step(df_wltp['time(s)'], df_wltp['slope(%)'], color='tab:red', alpha=0.3, label='Slope')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title('Detailed WLTP Test Cycle Profile with Slope')
plt.show()