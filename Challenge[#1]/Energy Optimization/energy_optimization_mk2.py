import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#values taken from the previous file

####------ DEEP SLEEP TIMES
personal_duty_cycle = 3+5; #personal_code= 107124(03)
sleep_mode_power_= 59.5  #value in [mW] extracted from the csv file "deep_sleep"

###------IDLE POWER
idle_power= 313 #value in [mW] extracted from the csv file "deep_sleep"
idle_period= 190432 / 1000000

###------WIFI-POWER
wifi_power= 776  #value in [mW] extracted from the csv file "deep_sleep"
wifi_period= 197867 /1000000 # value in [s] taken from the code simulation

###-----SENSOR POWER
sensor_read_power= 466  #value in [mW] extracted from the csv file "sensor_read"
sensor_read_period = 4053 / 1000000 #value in [s] taken from the code simulation

###---- TRANSMISSION POWER
transmission_power= 1239  #value in [mW] extracted from the csv file "transmission_power"
transmission_period=  64 / 1000000 # value in [s] taken from the code simulation


deep_sleep_energy_consumption   = sleep_mode_power_ * personal_duty_cycle
sensor_energy_consumption  = sensor_read_power * sensor_read_period
transmission_energy_consumption = transmission_power * transmission_period + wifi_power * wifi_period
idle_energy_consumption = idle_power * idle_period


#EXPLANATION-----
# In order to improve the energy consumption, the only possible variables capable to
# be manipulated are the sleep time, transmission power and wifi activation. In order to find the best possible value, we try
# every value in a 8 -> 3600 s with a step of 0.5 sec each

# Creazione dell'array x e y
x = np.arange(8, 3600, 0.5)
y = np.zeros_like(x)

# Ciclo per ogni valore di x
for i, x_test in enumerate(x):
    deep_sleep_energy_consumption= sleep_mode_power_ * x_test
    energy_consumption_transition_cycle= (deep_sleep_energy_consumption + sensor_energy_consumption +transmission_energy_consumption +idle_energy_consumption)/1000

    total_duty_cycle_sec= x_test + idle_period + sensor_read_period + transmission_period

    # Alive time estimation
    energy_budget= 2403 + 15000 # personal_code= 1071(2403)
    total_cycles = energy_budget/energy_consumption_transition_cycle
    y[i]= total_cycles * total_duty_cycle_sec

    # Plot dei dati
plt.figure(figsize=(10, 6))
plt.plot(x, y, color='b')
plt.xlabel('X (Sleep time in s)')
plt.ylabel('Y (Total lifetime of the system in s)')
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