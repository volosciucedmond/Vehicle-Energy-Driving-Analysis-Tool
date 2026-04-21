from src.physics import convert_kmh_to_ms, calculate_drag, calculate_rolling_resistance, calculate_acceleration_force, calculate_total_power, calculate_gradient_force
import pandas as pd
import json

with open('data/car_data.json', 'r') as f:
    car_data = json.load(f)

def analyze_trip_data(file_path, vehicle_name):
    df = pd.read_csv(file_path)
    mass = car_data[vehicle_name]["mass_kg"]
    drag_coefficient = car_data[vehicle_name]["drag_coefficient"]
    frontal_area = car_data[vehicle_name]["frontal_area_m2"]
    crr = car_data[vehicle_name]["crr"]
    

    df["velocity"] = convert_kmh_to_ms(df["speed(km/h)"])
    df["drag_force"] = calculate_drag(df["velocity"], drag_coefficient=drag_coefficient, area=frontal_area)
    df["rolling_resistance"] = calculate_rolling_resistance(mass=mass, rolling_resistance_coefficient=crr, slope_percent=df["slope(%)"])
    df["gradient_force"] = calculate_gradient_force(mass=mass, slope_percent=df["slope(%)"])
    df["acceleration_force"] = calculate_acceleration_force(mass=mass, acceleration=df["acceleration(m/s²)"])
    df["total_force"] = df["drag_force"] + df["rolling_resistance"] + df["acceleration_force"] + df["gradient_force"]
    df["power"] = calculate_total_power(df["velocity"], df["total_force"])
    df["energy_j"] = df["power"] * 1
    df["cumulative_energy_kwh"] = df["energy_j"].cumsum() / 3.6e6

    total_joules = df["power"].sum()
    total_distance = df["velocity"].sum()
    # print(total_distance)
    # print(total_joules)

    kwh_per_100km = (total_joules / 3.6e6) / (total_distance / 100000)
    print(f"Energy consumption for {car_data[vehicle_name]['name']}: {kwh_per_100km:.2f} kWh/100km")
    # print(trip_data)
    return df
