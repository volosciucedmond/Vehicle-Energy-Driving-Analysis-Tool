from src.physics import convert_kmh_to_ms, calculate_drag, calculate_rolling_resistance, calculate_acceleration_force, calculate_total_power

import pandas as pd



def analyze_trip_data(file_path):
    df = pd.read_csv(file_path)

    df["velocity"] = convert_kmh_to_ms(df["speed(km/h)"])
    df["drag_force"] = calculate_drag(df["velocity"], drag_coefficient=0.3, area=2.2)
    df["rolling_resistance"] = calculate_rolling_resistance(mass=1500, rolling_resistance_coefficient=0.015)
    df["acceleration_force"] = calculate_acceleration_force(mass=1500, acceleration=df["acceleration(m/s²)"])
    df["total_force"] = df["drag_force"] + df["rolling_resistance"] + df["acceleration_force"]
    df["power"] = calculate_total_power(df["velocity"], df["total_force"])
    df["energy_j"] = df["power"] * 1
    df["cumulative_energy_kwh"] = df["energy_j"].cumsum() / 3.6e6

    total_joules = sum(df["power"])
    total_distance = sum(df["velocity"])
    # print(total_distance)
    # print(total_joules)

    kwh_per_100km = (total_joules / 3.6e6) / (total_distance / 100000)
    print(f"Energy consumption: {kwh_per_100km:.2f} kWh/100km")
    # print(trip_data)
    return df
