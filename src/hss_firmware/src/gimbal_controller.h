#ifndef GIMBAL_CONTROLLER_H
#define GIMBAL_CONTROLLER_H

#include <Arduino.h>

// Gimbal Control Variables
extern float current_pan_angle;
extern float current_tilt_angle;
extern float target_pan_angle;
extern float target_tilt_angle;

// PID Controller (Placeholders)
extern float Kp_pan, Ki_pan, Kd_pan;
extern float Kp_tilt, Ki_tilt, Kd_tilt;

void update_gimbal_pid();
void move_stepper(int step_pin, int dir_pin, float current_angle, float target_angle);

#endif // GIMBAL_CONTROLLER_H
