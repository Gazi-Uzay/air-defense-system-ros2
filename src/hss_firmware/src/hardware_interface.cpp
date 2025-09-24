#include "hardware_interface.h"

void initialize_hardware_pins() {
  pinMode(PAN_STEP_PIN, OUTPUT);
  pinMode(PAN_DIR_PIN, OUTPUT);
  pinMode(TILT_STEP_PIN, OUTPUT);
  pinMode(TILT_DIR_PIN, OUTPUT);

  pinMode(PAN_LIMIT_MIN_PIN, INPUT_PULLUP);
  pinMode(PAN_LIMIT_MAX_PIN, INPUT_PULLUP);
  pinMode(TILT_LIMIT_MIN_PIN, INPUT_PULLUP);
  pinMode(TILT_LIMIT_MAX_PIN, INPUT_PULLUP);

  pinMode(MODE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(KILL_SWITCH_PIN, INPUT_PULLUP);

  pinMode(LASER_PIN, OUTPUT);
  digitalWrite(LASER_PIN, LOW); // Ensure laser is off initially
}

void set_laser_state(bool on) {
  digitalWrite(LASER_PIN, on ? HIGH : LOW);
}
