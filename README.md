Vehicle Energy % Driving Analysis Tool (V1.0)
---------------------------------------------

A python based tool to analyse vehicle energy consumption and driving efficiency using longitudinal dynamics.

Features:
---------

*   **Physics Engine**: Calculates aerodynamic drag, rolling resistance and acceleration forces.
    
*   **Regenerative Braking:** Simulates energy recovery during deceleration phases.
    
*   **Data visualization**: Generates a 3-panel analysis of Speed, Power and Cumulative Energy.
    

Example restult:
----------------

_Energy consumption: 9.21 kWh/100km_

How to run?
-----------

1.  **Install dependencies: 
```bash 
pip install -r requirements.txt
```
    
2.  **Generate data: 
```bash 
python src/generate_data.py
```
    
3.  **Run analysis:** 
```bash 
python main.py
 ```