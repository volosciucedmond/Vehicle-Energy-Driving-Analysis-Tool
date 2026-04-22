import streamlit as st
import pandas as pd
from src import analysis

# page configuration
st.set_page_config(page_title="Vehicle Energy Analysis", layout="wide")
st.markdown("""
            <style>
    /* The main background */
    .stApp { background-color: #262730; }

    /* The Metric Card */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #e1e4e8;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* Force Label and Value to be dark */
    [data-testid="stMetricLabel"] p {
        color: #555555 !important;
    }
    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
    }
    </style>
            """, unsafe_allow_html=True)
st.title("EV Energy Consumption & Range Analysis Tool")
st.markdown("Adjust parameters to see how phsics impact EV range in real time")
st.divider()

# sidebar for vehicle selection
st.sidebar.header("Vehicle configuration")
vehicle_list = list(analysis.car_data.keys())
selected_car = st.sidebar.selectbox("Select a vehicle", vehicle_list, format_func=lambda x: analysis.car_data[x]['name'])

# sidebar for "What if?" scenarios
st.sidebar.divider()
st.sidebar.subheader("Adjust Scenarios")

# get the base mass from JSON so the slider starts at the right spot
base_car_data = analysis.car_data[selected_car]
total_mass = st.sidebar.slider("Total Mass (kg)", 500, 3000, int(base_car_data["mass_kg"]), help="Includes vehicle, passengers, and cargo.")
speed_mult = st.sidebar.slider("Driving Aggressiveness (Speed %)", 0.5, 1.5, 1.0, help="1.0 is standard WLTP cycle. 1.2 is 20% faster.")

# data processing
base_df = analysis.analyze_trip_data('data/wltp_drive_cycle.csv', selected_car)

current_df = analysis.analyze_trip_data(
    'data/wltp_drive_cycle.csv', 
    selected_car,
    mass_override=total_mass,
    speed_multiplier=speed_mult
)

# metrics dashboard
base_cons = base_df["kwh_per_100km"].iloc[0]
base_range = base_df["estimated_range_km"].iloc[0]

curr_cons = current_df["kwh_per_100km"].iloc[0]
curr_range = current_df["estimated_range_km"].iloc[0]
avg_eff = current_df["motor_torque"].abs().max()

st.subheader(f"Live performance: {base_car_data['name']}")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        label = "Net Consumption",
        value = f"{curr_range:.1f} km",
        delta = f"{curr_range - base_range:.1f} km vs Base"
    )
with m2:
    st.metric(
        label="Predicted Range", 
        value=f"{curr_range:.1f} km",
        delta=f"{curr_range - base_range:.1f} km vs Base"
    )
with m3:
    st.metric(
        label="Avg. Powertrain Efficiency", 
        value=f"{avg_eff:.1f}%",
        help="Mechanical Energy at Wheels / Battery Energy Consumed"
    )
    st.divider()
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Cumulative energy usage")
    # Using area_chart for a modern look
    chart_data = current_df[['time(s)', 'cumulative_energy_kwh']].set_index('time(s)')
    st.area_chart(chart_data, color="#29b5e8", use_container_width=True)

with col_right:
    st.subheader("Powertrain stats")
    max_rpm = current_df['motor_rpm'].max()
    max_torque = current_df['motor_torque'].abs().max()
    
    st.write(f"**Peak Motor Speed:** `{max_rpm:.0f} RPM`")
    st.write(f"**Peak Motor Torque:** `{max_torque:.1f} Nm`")
    
    # Progress bar for heat loss
    heat_loss_total = (current_df["battery_power_w"] - current_df["power"]).abs().sum() / 3.6e6
    st.write(f"**Total Heat Loss:** `{heat_loss_total:.3f} kWh`")
    
    # Final data peek
    with st.expander("View Raw Simulation Data"):
        st.dataframe(current_df.head(100))

st.caption("Developed as a Professional Vehicle Dynamics Benchmarking Tool | Powered by NumPy & Matplotlib")