from src import analysis, visualization
import matplotlib.pyplot as plt

filePath = 'data/wltp_drive_cycle.csv'
print("Starting analysis of trip data...")

car_data_id = ["tesla_model_3", "dacia_spring", "audi_etron_gt", "vw_id3", "ford_transit_electric"]
results = []

plt.figure(figsize=(10,6))

for cid in car_data_id:
    result_df = analysis.analyze_trip_data(filePath, vehicle_name=cid)
    pretty_name = analysis.car_data[cid]['name'] # get the name for each vehicle
    
    # calculate totals
    total_battery_kwh = result_df["cumulative_energy_kwh"].iloc[-1]
    
    # calculate what the energy would have been without the efficiency tax
    perfect_energy_kwh = (result_df["power"] * 1).sum() / 3.6e6
    
    # heat loss is the difference
    heat_loss_kwh = total_battery_kwh - perfect_energy_kwh
    loss_percentage = (heat_loss_kwh / total_battery_kwh) * 100
    
    results.append({
        "vehicle": pretty_name,
        "Consumption": f"{result_df['kwh_per_100km'].iloc[0]:.2f} kWh/100km",
        "Heat Loss": f"{loss_percentage:.1f}",
    })
    
    plt.plot(result_df['time(s)'],
             result_df['battery_power_w'],
            label=f"car: {pretty_name} | Battery Power: {result_df['battery_power_w'].max() / 1000:.2f} kW",
    ) 
    
plt.title("WLTP Cycle: Multi-vehicle Energy Comparison")
plt.xlabel("Time (s)")
plt.ylabel("Motor RPM")
plt.legend()
plt.grid(True)
plt.show()

import pandas as pd
summary_df = pd.DataFrame(results)
print("\n--- FINAL BENCHMARK SUMMARY ---")
print(summary_df.to_string(index=False))
