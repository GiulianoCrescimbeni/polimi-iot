import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#values taken from the previous file
deep_sleep_power_mean= 3923.8090909090915
sensor_read_power_mean= 7898.059363957596
sensor_read_period= 3.5375
transmission_power_mean= 14483.779439252337
transmission_time_period= 1.5285714285714285


#personal_code= 1071(2403)
energy_budget= 2403 + 15000


#EXPLANATION-----
# In order to improve the energy consumption, the only possible variable capable to
# be manipulated is the sleep time. In order to find the best possible value, we try
# every value in a 8 -> 3600 s with a step of 0.5 sec each

# Creazione dell'array x e y
x = np.arange(8, 3600.5, 0.5)
y = np.zeros_like(x)

# Ciclo per ogni valore di x
for i, x_test in enumerate(x):
    # Cost per 1 transmission_cycle
    total_energy_consumption = ((deep_sleep_power_mean * x_test) + 
                                (sensor_read_power_mean * sensor_read_period) + 
                                (transmission_power_mean * transmission_time_period)) / 1000
    
    # Duration of 1 transmission_cycle
    total_duty_cycle_sec = x_test + sensor_read_period + transmission_time_period
    
    # Target values
    total_cycles = energy_budget / total_energy_consumption
    y[i] = total_cycles * total_duty_cycle_sec


    # Plot dei dati
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Total Cycles * Duty Cycle', color='b')
plt.xlabel('X (Sleep time in s)')
plt.ylabel('Y (Total Duration in s)')
plt.grid(True)
plt.legend()
plt.show()

x_eval= 500
print("Sleep time optimized: ", x_eval)
index_eval = np.where(x == x_eval)[0]
duration = total_cycles * total_duty_cycle_sec
print("Total duration of the system before:", y[0])
print("Total duration of the system after:", y[index_eval])
print("'%' improvement:",(y[index_eval] / y[0])*100 )