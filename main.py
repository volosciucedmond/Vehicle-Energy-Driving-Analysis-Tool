from src import analysis, visualization
import matplotlib.pyplot as plt

filePath = 'data/wltp_drive_cycle.csv'
print("Starting analysis of trip data...")

# data_tesla = analysis.analyze_trip_data(filePath, vehicle_name="tesla_model_3")
# data_dacia = analysis.analyze_trip_data(filePath, vehicle_name="dacia_spring")
# data_audi = analysis.analyze_trip_data(filePath, vehicle_name="audi_etron_gt")
# data_vw = analysis.analyze_trip_data(filePath, vehicle_name="vw_id3")

car_data_id = ["tesla_model_3", "dacia_spring", "audi_etron_gt", "vw_id3"]

plt.figure(figsize=(10,6))

for cid in car_data_id:
    
    result_df = analysis.analyze_trip_data(filePath, vehicle_name=cid)
    
    pretty_name = analysis.car_data[cid]['name']
    
    plt.plot(result_df['time(s)'], 
             result_df['cumulative_energy_kwh'], 
             label=f"car: {pretty_name} | Energy consumption: {result_df['kwh_per_100km'].max():.2f} kwh/100km") #

plt.title("WLTP Cycle: Multi-vehicle Energy Comparison")
plt.xlabel("Time (s)")
plt.ylabel("Cumulative Energy Consumption (kWh)")
plt.legend()
plt.grid(True)
plt.show()
