import pandas as pd
import numpy as np

print("\n")

# deep_sleep state values
df = pd.read_csv("deep_sleep.csv", usecols=[1])  

deep_sleep = df.iloc[:, 0].tolist() 
deep_sleep_mean = np.mean(deep_sleep)
deep_sleep_power_mean = deep_sleep_mean * 20 # the raw retrieved value has frequency of 20 (50 ms)

print("Power sleep consumption mean [mW]:", deep_sleep_power_mean)
personal_duty_cycle = 3+5; #personal_code= 107124(03)
print("Time in sleeping mode [s]: ", personal_duty_cycle)
print("\n")

# sensor_read values
df = pd.read_csv("sensor_read.csv", usecols=[1])

sensor_read = df.iloc[:, 0].tolist() 
sensor_read_power_mean = np.mean(sensor_read) * 20 # The raw retrieved value has frequency of 20 (50 ms)
sensor_read_period = len(sensor_read)/(4*20)

print("Sensor read consumption mean [mW]: ", sensor_read_power_mean)
print("Sensor read period [s]: " , sensor_read_period)
print("\n")

# transmission_power values
df = pd.read_csv("transmission_power.csv", usecols=[1])

transmission_power = df.iloc[:, 0].tolist() 
transmission_time_period = len(transmission_power)/ (7*20)
transmission_power_mean = np.mean(transmission_power) * 20  # The raw retrieved value has frequency of 20 (50 ms)

print("Transmission Power Consumption mean [mW]: ", transmission_power_mean )
print("Transmission period [s]: " , transmission_time_period)
print("\n")

deep_sleep_energy_consumption   = deep_sleep_power_mean * personal_duty_cycle
sensor_read_energy_consumption  = sensor_read_power_mean * sensor_read_period
transmission_energy_consumption = transmission_power_mean * transmission_time_period

print("• Deep sleep energy consumption [mJ]: ", deep_sleep_energy_consumption)
print("• Sensor read energy consumption [mJ]: ", sensor_read_energy_consumption)
print("• Transmission energy consumption [mJ]: ", transmission_energy_consumption)
print("\n")

total_energy_consumption = (deep_sleep_energy_consumption + sensor_read_energy_consumption + transmission_energy_consumption) / 1000
print("• Total energy consumption [J]: ", total_energy_consumption)
total_duty_cycle_sec= personal_duty_cycle + sensor_read_period + transmission_time_period
print("Total duty cycle [s]: ", total_duty_cycle_sec)
print("\n")

# Alive time estimation
energy_budget= 2403 + 15000 # personal_code= 1071(2403)
total_cycles = energy_budget/total_energy_consumption
print("Max number of cycles: ", total_cycles)
print("• Max period of activity [s]: ", total_cycles* total_duty_cycle_sec)

print("\n")

import matplotlib.pyplot as plt

def plot_data(filename, title):
    df = pd.read_csv(filename, usecols=[1])
    values = df.iloc[:, 0].tolist()
    
    plt.figure(figsize=(8, 4))
    plt.plot(values, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()

plot_data("deep_sleep.csv", "Deep Sleep Values")
plot_data("sensor_read.csv", "Sensor Read Values")
plot_data("transmission_power.csv", "Transmission Power Values")