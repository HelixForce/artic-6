#ifndef STEPPER_H
#define STEPPER_H

#include <AccelStepper.h>
#include "config.h"

// ============================================================
//  STEPPER MOTOR CONTROL
//  Uses AccelStepper library for smooth acceleration/decel
//  Install: Arduino IDE → Library Manager → "AccelStepper"
// ============================================================

// AccelStepper instances — one per axis
// Type 1 = driver mode (STEP + DIR pins only, driver handles coils)
AccelStepper steppers[NUM_AXES] = {
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_1, DIR_PIN_1),
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_2, DIR_PIN_2),
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_3, DIR_PIN_3),
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_4, DIR_PIN_4),
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_5, DIR_PIN_5),
  AccelStepper(AccelStepper::DRIVER, STEP_PIN_6, DIR_PIN_6),
};

// Current joint positions in degrees (updated after homing + moves)
float jointPositions[NUM_AXES] = {0, 0, 0, 0, 0, 0};

// Whether each axis has been homed
bool axisHomed[NUM_AXES] = {false, false, false, false, false, false};

// Emergency stop flag
volatile bool emergencyStop = false;

// ---- Convert degrees to steps for a given axis ----
long degreesToSteps(uint8_t axis, float degrees) {
  if (axis >= NUM_AXES) return 0;
  float stepsPerDeg = (STEPS_PER_REV * REDUCTIONS[axis]) / 360.0;
  return (long)(degrees * stepsPerDeg);
}

// ---- Convert steps to degrees for a given axis ----
float stepsToDegrees(uint8_t axis, long steps) {
  if (axis >= NUM_AXES) return 0;
  float stepsPerDeg = (STEPS_PER_REV * REDUCTIONS[axis]) / 360.0;
  return (float)steps / stepsPerDeg;
}

// ---- Initialize all steppers ----
void steppersInit() {
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    // Set enable pins
    pinMode(EN_PINS[i], OUTPUT);
    digitalWrite(EN_PINS[i], HIGH);  // HIGH = disabled (motors free)

    // Configure AccelStepper
    steppers[i].setMaxSpeed(MAX_SPEEDS[i]);
    steppers[i].setAcceleration(MAX_ACCELS[i]);
    steppers[i].setEnablePin(EN_PINS[i]);
    steppers[i].setPinsInverted(false, false, true); // EN is active LOW
    steppers[i].setCurrentPosition(0);
  }
}

// ---- Enable/disable individual axis ----
void enableAxis(uint8_t axis) {
  if (axis < NUM_AXES) {
    digitalWrite(EN_PINS[axis], LOW);  // LOW = motor energized
  }
}

void disableAxis(uint8_t axis) {
  if (axis < NUM_AXES) {
    digitalWrite(EN_PINS[axis], HIGH); // HIGH = motor free
  }
}

// ---- Enable/disable ALL axes ----
void enableAllAxes() {
  for (uint8_t i = 0; i < NUM_AXES; i++) enableAxis(i);
}

void disableAllAxes() {
  for (uint8_t i = 0; i < NUM_AXES; i++) disableAxis(i);
}

// ---- Check if target angle is within joint limits ----
bool withinLimits(uint8_t axis, float degrees) {
  if (axis >= NUM_AXES) return false;
  return (degrees >= JOINT_MINS[axis] && degrees <= JOINT_MAXS[axis]);
}

// ---- Move single axis to absolute angle (degrees) ----
// Returns false if out of limits or axis not homed
bool moveAxisTo(uint8_t axis, float degrees) {
  if (axis >= NUM_AXES) return false;
  if (!axisHomed[axis]) return false;
  if (!withinLimits(axis, degrees)) return false;
  if (emergencyStop) return false;

  long targetSteps = degreesToSteps(axis, degrees);
  steppers[axis].moveTo(targetSteps);
  return true;
}

// ---- Move single axis by relative degrees ----
bool moveAxisBy(uint8_t axis, float deltaDegrees) {
  if (axis >= NUM_AXES) return false;
  float newPos = jointPositions[axis] + deltaDegrees;
  return moveAxisTo(axis, newPos);
}

// ---- Check if any axis is still moving ----
bool anyAxisMoving() {
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    if (steppers[i].isRunning()) return true;
  }
  return false;
}

// ---- Run all steppers (call this in loop() as fast as possible) ----
// Returns true if any axis is still moving
bool steppersRun() {
  if (emergencyStop) return false;

  bool moving = false;
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    if (steppers[i].run()) {
      moving = true;
    }
  }

  // Update joint positions from step counters
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    jointPositions[i] = stepsToDegrees(i, steppers[i].currentPosition());
  }

  return moving;
}

// ---- Stop all axes immediately ----
void stopAllAxes() {
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    steppers[i].stop();                   // Decelerate to stop
    steppers[i].setCurrentPosition(        // Keep current position
      steppers[i].currentPosition()
    );
  }
}

// ---- Emergency stop — kill everything ----
void triggerEstop() {
  emergencyStop = true;
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    steppers[i].setSpeed(0);
    steppers[i].moveTo(steppers[i].currentPosition());
  }
  disableAllAxes();
}

// ---- Reset from e-stop (requires re-homing) ----
void resetEstop() {
  emergencyStop = false;
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    axisHomed[i] = false;
  }
}

#endif // STEPPER_H
