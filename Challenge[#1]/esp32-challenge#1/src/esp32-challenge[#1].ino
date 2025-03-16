#include <WiFi.h>
#include <esp_now.h>

#define uS_TO_S 1000000
#define TRIG_PIN 2 // Trigger pin to start the sampling
#define ECHO_PIN 4 // Echo pin for the output


//Broadcast Address: 8C:AA:B5:84:FB:90 
uint8_t broadcast_addr[]  {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90} ;

esp_now_peer_info_t peerInfo;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status){
  Serial.println("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok\n" : "Error\n");
}

void setup() {

  // IDLE //
  unsigned long idle_start = micros();
  Serial.begin(115200);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.println("Starting...");
  
  // SENSOR READ //
  unsigned long sensor_start = micros();
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read the result
  int duration = pulseIn(ECHO_PIN, HIGH, 4000);
  unsigned long sensor_end = micros();
  // END OF SENSOR READ //

  // IDLE //
  // Distance conversion in centimeters
  int distance= duration / 58;

  // Create the message to send
  String snd_msg = (distance < 51 && distance != 0) ? "OCCUPIED\0" : "FREE\0";

  // WIFI START //
  unsigned long wifi_start = micros();
  WiFi.mode(WIFI_STA);
  
  esp_now_init();
  esp_now_register_send_cb(OnDataSent);

  memcpy(peerInfo.peer_addr,broadcast_addr, 6);
  peerInfo.channel= 0;
  peerInfo.encrypt= 0;

  esp_now_add_peer(&peerInfo);

  // TRANSMISSION START //
  unsigned long transmission_start = micros();
  esp_now_send(broadcast_addr, (uint8_t*) snd_msg.c_str(), snd_msg.length() + 1);
  unsigned long transmission_end = micros();
  // TRANSMISSION END //

  WiFi.mode(WIFI_OFF);
  unsigned long wifi_end = micros();
  // WIFI END//

  int personal_duty_cycle= 3+5; // Personal Code = 107124(03)
  esp_sleep_enable_timer_wakeup(personal_duty_cycle * uS_TO_S);

  // Debug info
  Serial.print("Distance in CM: ");
  Serial.print(distance);
  Serial.print("\n");
  Serial.println(snd_msg);

  Serial.print("Sensor duration: ");
  Serial.print(sensor_end - sensor_start);
  Serial.print("\n");
  Serial.print("Wifi duration: ");
  Serial.print(wifi_end - wifi_start );
  Serial.print("\n");
  Serial.print("Transmission duration: ");
  Serial.print(transmission_end - transmission_start);
  Serial.print("\n");
  Serial.print("Idle time: ");
  Serial.print((transmission_start - sensor_end) + (sensor_start - idle_start));
  Serial.print("\n");

  esp_deep_sleep_start();
}

void loop() {
  //not utilized
}