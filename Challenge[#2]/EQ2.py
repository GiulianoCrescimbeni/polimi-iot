# Parameters
ETX = 50 / 1000000  # mJ/bit
ERX = 58 / 1000000  # mJ/bit
Ec = 2.4            # mJ for computation

def to_bits(byte):
    return byte * 8

def tx_energy(byte):
    return to_bits(byte) * ETX

def rx_energy(byte):
    return to_bits(byte) * ERX

# Frequencies
sensor_tx_per_day = 288
valve_rx_per_day = 288
valve_avg_computations = 48

# --- EQ1(a): COAP ---
coap_notify_tx = tx_energy(55) # PUT request
coap_reg_tx = tx_energy(60) # GET for connection
coap_get_rx = rx_energy(55) # GET for observations

coap_sensor_energy = coap_reg_tx + sensor_tx_per_day * coap_notify_tx
                    #Registration# #----------Transmission----------#

coap_valve_energy = coap_reg_tx + valve_rx_per_day * coap_get_rx + valve_avg_computations * Ec
                   #Registration# #---Receiving of Readings----#   #-------Computation-------#
coap_total = coap_sensor_energy + coap_valve_energy

# --- EQ1(b): MQTT ---
mqtt_conn_tx = tx_energy(54)
mqtt_conn_ack_rx = rx_energy(47)

mqtt_subscribe_rx = rx_energy(68)
mqtt_subscribe_ack_tx = tx_energy(52)

mqtt_publish_tx = tx_energy(68)
mqtt_publish_rx = rx_energy(68)

mqtt_sensor_energy = mqtt_conn_tx + mqtt_conn_ack_rx + sensor_tx_per_day * mqtt_publish_tx
                     #----------Connection---------#   #----Transmission of readings-----#

mqtt_valve_energy = mqtt_conn_tx + mqtt_conn_ack_rx + mqtt_subscribe_rx + mqtt_subscribe_ack_tx + valve_rx_per_day * mqtt_publish_rx + valve_avg_computations * Ec
                    #----------Connection---------#   #-------------Subscription--------------#   #-----Receiving of Readings------#   #-------Computation-------#

mqtt_total = mqtt_sensor_energy + mqtt_valve_energy

print("== EQ1 Results ==")
print(f"COAP Total Energy:  {coap_total:.2f} mJ")
print(f"MQTT Total Energy:  {mqtt_total:.2f} mJ")

# Changing protocol to MTTQ-SN for EQ2
mqtt_conn_tx = tx_energy(6)
mqtt_conn_ack_rx = rx_energy(3)

mqtt_subscribe_rx = rx_energy(6)
mqtt_subscribe_ack_tx = tx_energy(5)

mqtt_publish_tx = tx_energy(15)
mqtt_publish_rx = rx_energy(15)

mqtt_sensor_energy = mqtt_conn_tx + mqtt_conn_ack_rx + sensor_tx_per_day * mqtt_publish_tx
                     #----------Connection---------#   #----Transmission of readings-----#

mqtt_valve_energy = mqtt_conn_tx + mqtt_conn_ack_rx + mqtt_subscribe_rx + mqtt_subscribe_ack_tx + valve_rx_per_day * mqtt_publish_rx + valve_avg_computations * Ec
                    #----------Connection---------#   #-------------Subscription--------------#   #-----Receiving of Readings------#   #-------Computation-------#
mqtt_total = mqtt_sensor_energy + mqtt_valve_energy

print("\n\n== EQ2 Results ==")
print(f"MQTT Total Energy:  {mqtt_total:.2f} mJ")


# Changing sampling frequencies for energy optimization in EQ2 
import matplotlib.pyplot as plt

# Parameters
ETX = 50 / 1e6  # mJ/bit
ERX = 58 / 1e6  # mJ/bit
Ec = 2.4        # mJ

def to_bits(byte): return byte * 8
def tx_energy(byte): return to_bits(byte) * ETX
def rx_energy(byte): return to_bits(byte) * ERX

# MQTT-SN message sizes
mqtt_conn_tx = tx_energy(6)
mqtt_conn_ack_rx = rx_energy(3)
mqtt_subscribe_rx = rx_energy(6)
mqtt_subscribe_ack_tx = tx_energy(5)
mqtt_publish_tx = tx_energy(15)
mqtt_publish_rx = rx_energy(15)

# Frequencies to test (in minutes)
sampling_intervals = [1, 5, 10, 15, 30, 60]
total_energies = []

for interval in sampling_intervals:
    tx_per_day = int(1440 / interval)  # 1440 minutes in a day
    comp_per_day = 48  # assume valve computes every 2x sampling interval

    sensor_energy = mqtt_conn_tx + mqtt_conn_ack_rx + tx_per_day * mqtt_publish_tx
    valve_energy = (
        mqtt_conn_tx + mqtt_conn_ack_rx +
        mqtt_subscribe_rx + mqtt_subscribe_ack_tx +
        tx_per_day * mqtt_publish_rx +
        comp_per_day * Ec
    )

    total_energy = sensor_energy + valve_energy
    total_energies.append(total_energy)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(sampling_intervals, total_energies, marker='o')
plt.xlabel('Sampling Interval (minutes)')
plt.ylabel('Total Energy Consumption (mJ)')
plt.title('Energy Consumption in a day vs Sampling Frequency (MQTT-SN)')
plt.grid(True)
plt.tight_layout()
plt.show()


# Changing valve computation frequencies for energy optimization in EQ2 
import matplotlib.pyplot as plt

# Parameters
ETX = 50 / 1e6  # mJ/bit
ERX = 58 / 1e6  # mJ/bit
Ec = 2.4        # mJ

def to_bits(byte): return byte * 8
def tx_energy(byte): return to_bits(byte) * ETX
def rx_energy(byte): return to_bits(byte) * ERX

# MQTT-SN message sizes
mqtt_conn_tx = tx_energy(6)
mqtt_conn_ack_rx = rx_energy(3)
mqtt_subscribe_rx = rx_energy(6)
mqtt_subscribe_ack_tx = tx_energy(5)
mqtt_publish_tx = tx_energy(15)
mqtt_publish_rx = rx_energy(15)

# Frequencies to test (in minutes)
sampling_intervals = [1, 5, 10, 15, 30, 60, 120, 240]
total_energies = []

for interval in sampling_intervals:
    tx_per_day = 288  # 1440 minutes in a day
    comp_per_day = int(1440 / interval)  # assume valve computes every 2x sampling interval

    sensor_energy = mqtt_conn_tx + mqtt_conn_ack_rx + tx_per_day * mqtt_publish_tx
    valve_energy = (
        mqtt_conn_tx + mqtt_conn_ack_rx +
        mqtt_subscribe_rx + mqtt_subscribe_ack_tx +
        tx_per_day * mqtt_publish_rx +
        comp_per_day * Ec
    )

    total_energy = sensor_energy + valve_energy
    total_energies.append(total_energy)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(sampling_intervals, total_energies, marker='o')
plt.xlabel('Sampling Interval (minutes)')
plt.ylabel('Total Energy Consumption (mJ)')
plt.title('Energy Consumption in a day vs Valve computation Frequency (MQTT-SN)')
plt.grid(True)
plt.tight_layout()
plt.show()