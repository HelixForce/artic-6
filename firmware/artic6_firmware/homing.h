#ifndef HOMING_H
#define HOMING_H

#include "config.h"
#include "stepper.h"

// ============================================================
//  HOMING ROUTINES
//  Each axis moves toward its limit switch, backs off, then
//  re-approaches slowly for precision. Sets position to zero
//  plus offset.
//
//  Limit switches: NC wired, HIGH = normal, LOW = triggered
// ============================================================

// ---- Read limit switch (with debounce) ----
bool limitTriggered(uint8_t axis) {
  if (axis >= NUM_AXES) return true; // fail safe
  // NC wiring: LOW = triggered (switch opened or wire broken)
  if (digitalRead(LIMIT_PINS[axis]) == LOW) {
    delay(LIMIT_DEBOUNCE_MS);
    return (digitalRead(LIMIT_PINS[axis]) == LOW);
  }
  return false;
}

// ---- Home a single axis ----
// Returns true on success, false on failure/timeout
bool homeAxis(uint8_t axis) {
  if (axis >= NUM_AXES) return false;
  if (emergencyStop) return false;

  Serial.print(F("HOMING axis "));
  Serial.println(axis + 1);

  enableAxis(axis);
  delay(100); // Let driver stabilize

  int8_t dir = HOME_DIRS[axis];
  float stepsPerDeg = (STEPS_PER_REV * REDUCTIONS[axis]) / 360.0;

  // --- Phase 1: Fast approach toward limit switch ---
  steppers[axis].setMaxSpeed(HOMING_SPEED_FAST);
  steppers[axis].setAcceleration(MAX_ACCELS[axis]);

  // Move a large distance in the homing direction (will be interrupted by limit switch)
  long maxTravel = degreesToSteps(axis, 400.0); // 400° should be more than enough
  steppers[axis].move(dir * maxTravel);

  unsigned long timeout = millis() + 30000; // 30s timeout
  while (!limitTriggered(axis)) {
    if (emergencyStop) return false;
    if (millis() > timeout) {
      Serial.print(F("ERR homing timeout axis "));
      Serial.println(axis + 1);
      steppers[axis].stop();
      disableAxis(axis);
      return false;
    }
    steppers[axis].run();
  }

  // Hit the switch — stop
  steppers[axis].stop();
  steppers[axis].setCurrentPosition(steppers[axis].currentPosition());
  delay(200);

  // --- Phase 2: Back off from switch ---
  steppers[axis].setMaxSpeed(HOMING_SPEED_SLOW);
  long backoff = degreesToSteps(axis, 10.0); // Back off 10 degrees
  steppers[axis].move(-dir * backoff);

  while (steppers[axis].isRunning()) {
    if (emergencyStop) return false;
    steppers[axis].run();
  }
  delay(200);

  // --- Phase 3: Slow re-approach for precision ---
  steppers[axis].move(dir * backoff);  // Approach again slowly

  while (!limitTriggered(axis)) {
    if (emergencyStop) return false;
    steppers[axis].run();
  }

  steppers[axis].stop();
  delay(100);

  // --- Phase 4: Set home position ---
  steppers[axis].setCurrentPosition(0);

  // Move to home offset (away from the switch)
  long offsetSteps = degreesToSteps(axis, HOME_OFFSETS[axis]);
  steppers[axis].move(-dir * offsetSteps);

  while (steppers[axis].isRunning()) {
    if (emergencyStop) return false;
    steppers[axis].run();
  }

  // This position is now "home" (0 degrees)
  steppers[axis].setCurrentPosition(0);
  jointPositions[axis] = 0.0;
  axisHomed[axis] = true;

  // Restore normal speed
  steppers[axis].setMaxSpeed(MAX_SPEEDS[axis]);

  Serial.print(F("OK homed axis "));
  Serial.println(axis + 1);
  return true;
}

// ---- Home all axes in safe order ----
// Order matters: shoulder & elbow first (they could collide with base)
// then base, then wrist axes
bool homeAllAxes() {
  Serial.println(F("HOMING all axes..."));

  // Home order: 2 (shoulder), 3 (elbow), 1 (base), 4, 5, 6
  const uint8_t homeOrder[NUM_AXES] = {1, 2, 0, 3, 4, 5};

  for (uint8_t i = 0; i < NUM_AXES; i++) {
    if (!homeAxis(homeOrder[i])) {
      Serial.print(F("ERR homing failed at axis "));
      Serial.println(homeOrder[i] + 1);
      disableAllAxes();
      return false;
    }
  }

  Serial.println(F("OK all axes homed"));
  return true;
}

#endif // HOMING_H
