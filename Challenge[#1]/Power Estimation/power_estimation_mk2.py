import pandas as pd
import numpy as np

print("SECOND VERSION\n")

####------ DEEP SLEEP TIMES
personal_duty_cycle = 3+5; #personal_code= 107124(03)
sleep_mode_power_= 59.5 #value in [mW] extracted from the csv file "deep_sleep"

###------IDLE POWER
idle_power= 313  #value in [mW] extracted from the csv file "deep_sleep"
idle_period= 190432 / 1000000

###------WIFI-POWER
wifi_power= 776  #value in [mW] extracted from the csv file "deep_sleep"
wifi_period= 197867 /1000000 # value in [s] taken from the code simulation

###-----SENSOR POWER
sensor_read_power= 466 #value in [mW] extracted from the csv file "sensor_read"
sensor_read_period = 4053 / 1000000 #value in [s] taken from the code simulation

###---- TRANSMISSION POWER
transmission_power= 1239 #value in [mW] extracted from the csv file "transmission_power"
transmission_period=  64 / 1000000 # value in [s] taken from the code simulation


deep_sleep_energy_consumption   = sleep_mode_power_ * personal_duty_cycle
sensor_energy_consumption  = sensor_read_power * sensor_read_period
transmission_energy_consumption = transmission_power * transmission_period + wifi_power * wifi_period
idle_energy_consumption = idle_power * idle_period

print("• Deep sleep energy consumption [mJ]: ", deep_sleep_energy_consumption)
print("Deep sleep time [s]: 8")
print("• Sensor read energy consumption [mJ]: ", sensor_energy_consumption)
print("Sensor read time [s]: ", sensor_read_period)
print("• Transmission energy consumption [mJ]: ", transmission_energy_consumption)
print("Trasnsmission time [s]: ", transmission_period + wifi_period)
print("• Idle energy consumption [mJ]:", idle_energy_consumption)
print("Idle time [s]: ", idle_period)
print("\n")

#FINAL COSTS
energy_consumption_transition_cycle= (deep_sleep_energy_consumption + sensor_energy_consumption + transmission_energy_consumption + idle_energy_consumption)/1000
print("• Total energy consumption per cycle [J]:", energy_consumption_transition_cycle)

total_duty_cycle_sec= personal_duty_cycle + idle_period + wifi_period + sensor_read_period + transmission_period
print("Total duty cycle [s]: ", total_duty_cycle_sec)
print("\n")

# Alive time estimation
energy_budget= 2403 + 15000 # personal_code= 1071(2403)
total_cycles = energy_budget/energy_consumption_transition_cycle
print("Max number of cycles: ", total_cycles)
print("• Max period of activity [s]: ", total_cycles* total_duty_cycle_sec)

print("\n")