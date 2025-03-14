import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#values taken from the previous file

####------ DEEP SLEEP TIMES
personal_duty_cycle = 3+5; #personal_code= 107124(03)
sleep_mode_power_= 59.5 * 20 #value in [mW] extracted from the csv file "deep_sleep"
print("Time in sleeping mode [s]: ", personal_duty_cycle)
print("Power cost of sleep mode per sec [mW]", sleep_mode_power_)
print("\n")

###------BOOT POWER
boot_up_power= 313 * 20 #value in [mW] extracted from the csv file "deep_sleep"
print("the power requested to boot is [mW]:", boot_up_power)


###------WIFI-POWER
wifi_power_= 776 * 20 - boot_up_power #value in [mW] extracted from the csv file "deep_sleep"
wifi_period= 195650 /1000000 # value in [s] taken from the code simulation

###-----SENSOR POWER
sensor_read_power= 466 *20 #value in [mW] extracted from the csv file "sensor_read"
sensor_read_period = 12000 / 1000000 #value in [s] taken from the code simulation
sensor_idle_power= 331* 20 #value in [mW] extracted from the csv file "sensor_read"
sensor_idle_period=  252 / 1000000 # value in [s] taken from the code simulation


###---- TRANSMISSION POWER
transmission_power= 1239 * 20 #value in [mW] extracted from the csv file "transmission_power"
transmission_period=  252 / 1000000 # value in [s] taken from the code simulation

total_working_time= wifi_period


#deep_sleep_energy_consumption   = sleep_mode_power_ * personal_duty_cycle
sensor_total_energy_consumption  = sensor_read_power * sensor_read_period + sensor_idle_period *sensor_idle_power
transmission_energy_consumption = transmission_power * transmission_period
boot_up_energy_consumption= boot_up_power * total_working_time



#EXPLANATION-----
# In order to improve the energy consumption, the only possible variables capable to
# be manipulated are the sleep time, transmission power and wifi activation. In order to find the best possible value, we try
# every value in a 8 -> 3600 s with a step of 0.5 sec each

# Creazione dell'array x e y
x = np.arange(8, 3600.5, 0.5)
y = np.zeros_like(x)

# Ciclo per ogni valore di x
for i, x_test in enumerate(x):
    deep_sleep_energy_consumption= sleep_mode_power_ * x_test
    energy_consumption_transition_cycle= (deep_sleep_energy_consumption + sensor_total_energy_consumption +transmission_energy_consumption +boot_up_energy_consumption)/1000

    total_duty_cycle_sec= x_test+ total_working_time

    # Alive time estimation
    energy_budget= 2403 + 15000 # personal_code= 1071(2403)
    total_cycles = energy_budget/energy_consumption_transition_cycle
    y[i]= total_cycles * total_duty_cycle_sec

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