from src.physics import calculate_motor_efficiency, convert_kmh_to_ms, calculate_drag, calculate_rolling_resistance, calculate_acceleration_force, calculate_total_power, calculate_gradient_force
import pandas as pd
import numpy as np
import json

with open('data/car_data.json', 'r') as f:
    car_data = json.load(f)

def analyze_trip_data(file_path, vehicle_name, mass_override=None, speed_multiplier=1.0):
    df = pd.read_csv(file_path)
    
    # get base data from JSON
    car = car_data[vehicle_name]
    
    # apply overrides (use slider value if provided, otherwise use JSON value)
    mass = mass_override if mass_override is not None else car["mass_kg"]
    
    drag_coefficient = car["drag_coefficient"]
    frontal_area = car["frontal_area_m2"]
    crr = car["crr"]
    wheel_radius = car["wheel_radius_m"]

    # apply speed multiplier to the entire speed column
    df["speed(km/h)"] = df["speed(km/h)"] * speed_multiplier
    

    df["velocity"] = convert_kmh_to_ms(df["speed(km/h)"])
    df["drag_force"] = calculate_drag(df["velocity"], drag_coefficient=drag_coefficient, area=frontal_area)
    df["rolling_resistance"] = calculate_rolling_resistance(mass=mass, rolling_resistance_coefficient=crr, slope_percent=df["slope(%)"])
    df["gradient_force"] = calculate_gradient_force(mass=mass, slope_percent=df["slope(%)"])
    df["acceleration_force"] = calculate_acceleration_force(mass=mass, acceleration=df["acceleration(m/s²)"])
    df["total_force"] = df["drag_force"] + df["rolling_resistance"] + df["acceleration_force"] + df["gradient_force"]
    df["power"] = calculate_total_power(df["velocity"], df["total_force"])
    
    angular_velocity = df["velocity"] / wheel_radius
    
    df["motor_torque"] = (df["total_force"] * wheel_radius) / 9.0
    
    df["motor_rpm"] = angular_velocity * (60 / (2 * np.pi)) * 9 # considered 9 standard gear ratio for electric cars
    df["motor_efficiency"] = calculate_motor_efficiency(df["motor_rpm"], df["motor_torque"])
    
    df["battery_power_w"] = np.where(
        df["power"] > 0, 
        df["power"] / df["motor_efficiency"], 
        df["power"] * df["motor_efficiency"]
    )

    df["energy_j"] = df["battery_power_w"] * 1
    df["cumulative_energy_kwh"] = df["energy_j"].cumsum() / 3.6e6

    total_joules = df["battery_power_w"].sum()
    total_distance = df["velocity"].sum()
    kwh_per_100km = (total_joules / 3.6e6) / (total_distance / 100000)
    print(f"Energy consumption for {car_data[vehicle_name]['name']}: {kwh_per_100km:.2f} kWh/100km")
    df["kwh_per_100km"] = kwh_per_100km
    # print(trip_data)
    
    # range prediction
    battery_cap = car_data[vehicle_name]["battery_capacity_kwh"]
    
    # calculate estimated range (km) = (totabl batter / consumption) * 100
    estimated_range_km = (battery_cap / kwh_per_100km) * 100
    
    print(f"Predicted range for {car_data[vehicle_name]['name']}: {estimated_range_km:.1f} km")
    df["estimated_range_km"] = estimated_range_km
    
    return df
