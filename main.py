from src import analysis, visualization


filePath = 'data/wltp_drive_cycle.csv'
print("Starting analysis of trip data...")

data_tesla = analysis.analyze_trip_data(filePath, vehicle_name="tesla_model_3")
data_dacia = analysis.analyze_trip_data(filePath, vehicle_name="dacia_spring")
data_audi = analysis.analyze_trip_data(filePath, vehicle_name="audi_etron_gt")
data_vw = analysis.analyze_trip_data(filePath, vehicle_name="vw_id3")

print("Trip data analysis complete. Generating visualizations...")

visualization.plot_results(data_tesla, "tesla_model_3")
visualization.plot_results(data_dacia, "dacia_spring")
visualization.plot_results(data_audi, "audi_etron_gt")
visualization.plot_results(data_vw, "vw_id3")