GRAVITY = 9.81 
AIR_DENSITY = 1.225

def convert_kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6

def calculate_drag(velocity, drag_coefficient, area):
    return 0.5 * AIR_DENSITY * area * drag_coefficient * (velocity ** 2)

def calculate_rolling_resistance(mass, rolling_resistance_coefficient):
    return mass * GRAVITY * rolling_resistance_coefficient

def calculate_acceleration_force(mass, acceleration):
    return mass * acceleration

def calculate_total_power(velocity, forces_sum):
    return forces_sum * velocity