time_s = 0
speed_kmh = 0
accel_mps2 = 0
time = []
speed = []
acceleration = []
slope = []

for i in range (0, 61):
    current_time = i
    # speeds, acceleration and time
    if current_time < 10:
        time.append(current_time)
        accel_mps2 = 1.38
        acceleration.append(accel_mps2)
        speed_kmh = max(0, speed_kmh)
        speed_kmh += accel_mps2 * 3.6
        speed.append(speed_kmh)
    elif 10 <= current_time < 50:
        time.append(current_time)
        accel_mps2 = 0
        acceleration.append(accel_mps2)
        speed_kmh += accel_mps2 * 3.6
        speed_kmh = max(0, speed_kmh)
        speed.append(speed_kmh)      
    else:
        time.append(current_time)
        accel_mps2 = -1.38
        acceleration.append(accel_mps2)
        speed_kmh += accel_mps2 * 3.6
        speed_kmh = max(0, speed_kmh)
        speed.append(speed_kmh)
        
    # road slope
    if current_time < 20:
        slopeV = 0
        slope.append(slopeV)
    elif 20 <= current_time < 30:
        slopeV = 4
        slope.append(slopeV)
    elif 30 <= current_time < 40:
        slopeV = 0
        slope.append(slopeV)
    else:
        slopeV = -3
        slope.append(slopeV)
        

        
def create_csv(time, speed, acceleration):
    import pandas as pd
    data = {'time(s)': time, 'speed(km/h)': speed, 'acceleration(m/s²)': acceleration, 'slope(%)': slope}
    df = pd.DataFrame(data)
    df.to_csv('data/drive_cycle.csv', index=False)
    return df
# print(speed)

my_dataframe = create_csv(time, speed, acceleration)
print(my_dataframe)
