#ifndef SENSOR_READER_H
#define SENSOR_READER_H

#include <Arduino.h>

// IMU Data (Placeholders)
extern float imu_roll, imu_pitch, imu_yaw;

void read_imu_data();
void read_buttons_and_switches();

#endif // SENSOR_READER_H
