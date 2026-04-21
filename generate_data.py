time_s = 0
speed_kmh = 0
accel_mps2 = 0
time = []
speed = []
acceleration = []

for i in range (0, 61):
    current_time = i
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
        
def create_csv(time, speed, acceleration):
    import pandas as pd
    data = {'time(s)': time, 'speed(km/h)': speed, 'acceleration(m/s²)': acceleration}
    df = pd.DataFrame(data)
    df.to_csv('data/drive_cycle.csv', index=False)
    return df
# print(speed)

my_dataframe = create_csv(time, speed, acceleration)
print(my_dataframe)
