from src import analysis, visualization

filePath = 'data/drive_cycle.csv'
print("Starting analysis of trip data...")

trip_data = analysis.analyze_trip_data(filePath)
print("Trip data analysis complete. Generating visualizations...")

visualization.plot_results(trip_data)