#ifndef SERIAL_PROTOCOL_H
#define SERIAL_PROTOCOL_H

#include "config.h"
#include "stepper.h"
#include "homing.h"

// ============================================================
//  SERIAL PROTOCOL — RPi ↔ Arduino communication
//
//  Commands are plain text lines ending with \n
//  Arduino responds with "OK ..." or "ERR ..." lines
//
//  COMMAND FORMAT:
//    MOVE <axis> <degrees>     Move axis to absolute angle
//    MOVR <axis> <degrees>     Move axis by relative angle
//    MOVA <a1> <a2> <a3> <a4> <a5> <a6>   Move all axes at once
//    HOME                      Home all axes
//    HOMEA <axis>              Home single axis
//    STOP                      Stop all axes (decelerate)
//    ESTOP                     Emergency stop (instant)
//    RESET                     Reset from e-stop
//    ENABLE                    Enable all motors
//    DISABLE                   Disable all motors
//    POS                       Report current joint positions
//    STATUS                    Report full status
//    PING                      Heartbeat — responds "OK PONG"
// ============================================================

#define CMD_BUF_SIZE 128
char cmdBuffer[CMD_BUF_SIZE];
uint8_t cmdIndex = 0;

// Last command time (for watchdog)
unsigned long lastCmdTime = 0;

// ---- Parse and execute a complete command line ----
void executeCommand(const char* cmd) {
  lastCmdTime = millis();

  // --- PING ---
  if (strncmp(cmd, "PING", 4) == 0) {
    Serial.println(F("OK PONG"));
    return;
  }

  // --- ESTOP ---
  if (strncmp(cmd, "ESTOP", 5) == 0) {
    triggerEstop();
    Serial.println(F("OK ESTOP activated"));
    return;
  }

  // --- RESET ---
  if (strncmp(cmd, "RESET", 5) == 0) {
    resetEstop();
    Serial.println(F("OK RESET — re-home required"));
    return;
  }

  // --- STOP ---
  if (strncmp(cmd, "STOP", 4) == 0) {
    stopAllAxes();
    Serial.println(F("OK STOPPED"));
    return;
  }

  // --- ENABLE ---
  if (strncmp(cmd, "ENABLE", 6) == 0) {
    enableAllAxes();
    Serial.println(F("OK motors enabled"));
    return;
  }

  // --- DISABLE ---
  if (strncmp(cmd, "DISABLE", 7) == 0) {
    disableAllAxes();
    Serial.println(F("OK motors disabled"));
    return;
  }

  // --- HOME (all) ---
  if (strcmp(cmd, "HOME") == 0) {
    if (emergencyStop) {
      Serial.println(F("ERR e-stop active, send RESET first"));
      return;
    }
    if (homeAllAxes()) {
      Serial.println(F("OK HOME complete"));
    } else {
      Serial.println(F("ERR HOME failed"));
    }
    return;
  }

  // --- HOMEA <axis> (home single axis, 1-indexed) ---
  if (strncmp(cmd, "HOMEA ", 6) == 0) {
    int axis = atoi(cmd + 6) - 1;  // Convert to 0-indexed
    if (axis < 0 || axis >= NUM_AXES) {
      Serial.println(F("ERR invalid axis (1-6)"));
      return;
    }
    if (emergencyStop) {
      Serial.println(F("ERR e-stop active"));
      return;
    }
    if (homeAxis(axis)) {
      Serial.print(F("OK HOMEA "));
      Serial.println(axis + 1);
    } else {
      Serial.print(F("ERR HOMEA failed axis "));
      Serial.println(axis + 1);
    }
    return;
  }

  // --- MOVA <a1> <a2> <a3> <a4> <a5> <a6> (move all axes) ---
  if (strncmp(cmd, "MOVA ", 5) == 0) {
    float angles[NUM_AXES];
    int parsed = sscanf(cmd + 5, "%f %f %f %f %f %f",
      &angles[0], &angles[1], &angles[2],
      &angles[3], &angles[4], &angles[5]);
    if (parsed != NUM_AXES) {
      Serial.println(F("ERR MOVA needs 6 angles"));
      return;
    }
    // Validate all before moving any
    for (uint8_t i = 0; i < NUM_AXES; i++) {
      if (!axisHomed[i]) {
        Serial.print(F("ERR axis "));
        Serial.print(i + 1);
        Serial.println(F(" not homed"));
        return;
      }
      if (!withinLimits(i, angles[i])) {
        Serial.print(F("ERR axis "));
        Serial.print(i + 1);
        Serial.println(F(" out of limits"));
        return;
      }
    }
    // All valid — command all axes
    for (uint8_t i = 0; i < NUM_AXES; i++) {
      moveAxisTo(i, angles[i]);
    }
    Serial.println(F("OK MOVA"));
    return;
  }

  // --- MOVE <axis> <degrees> (absolute) ---
  if (strncmp(cmd, "MOVE ", 5) == 0) {
    int axis;
    float degrees;
    if (sscanf(cmd + 5, "%d %f", &axis, &degrees) != 2) {
      Serial.println(F("ERR usage: MOVE <axis 1-6> <degrees>"));
      return;
    }
    axis -= 1; // Convert to 0-indexed
    if (axis < 0 || axis >= NUM_AXES) {
      Serial.println(F("ERR invalid axis (1-6)"));
      return;
    }
    if (moveAxisTo(axis, degrees)) {
      Serial.print(F("OK MOVE "));
      Serial.print(axis + 1);
      Serial.print(F(" → "));
      Serial.println(degrees);
    } else {
      if (!axisHomed[axis]) Serial.println(F("ERR axis not homed"));
      else if (!withinLimits(axis, degrees)) Serial.println(F("ERR out of limits"));
      else Serial.println(F("ERR move failed"));
    }
    return;
  }

  // --- MOVR <axis> <degrees> (relative) ---
  if (strncmp(cmd, "MOVR ", 5) == 0) {
    int axis;
    float degrees;
    if (sscanf(cmd + 5, "%d %f", &axis, &degrees) != 2) {
      Serial.println(F("ERR usage: MOVR <axis 1-6> <degrees>"));
      return;
    }
    axis -= 1;
    if (axis < 0 || axis >= NUM_AXES) {
      Serial.println(F("ERR invalid axis (1-6)"));
      return;
    }
    if (moveAxisBy(axis, degrees)) {
      Serial.print(F("OK MOVR "));
      Serial.println(axis + 1);
    } else {
      Serial.println(F("ERR relative move failed"));
    }
    return;
  }

  // --- POS (report positions) ---
  if (strncmp(cmd, "POS", 3) == 0) {
    Serial.print(F("POS"));
    for (uint8_t i = 0; i < NUM_AXES; i++) {
      Serial.print(F(" "));
      Serial.print(jointPositions[i], 2);
    }
    Serial.println();
    return;
  }

  // --- STATUS ---
  if (strncmp(cmd, "STATUS", 6) == 0) {
    Serial.print(F("STATUS estop="));
    Serial.print(emergencyStop ? F("YES") : F("NO"));
    Serial.print(F(" moving="));
    Serial.print(anyAxisMoving() ? F("YES") : F("NO"));
    Serial.print(F(" homed="));
    for (uint8_t i = 0; i < NUM_AXES; i++) {
      Serial.print(axisHomed[i] ? '1' : '0');
    }
    Serial.print(F(" pos="));
    for (uint8_t i = 0; i < NUM_AXES; i++) {
      Serial.print(jointPositions[i], 1);
      if (i < NUM_AXES - 1) Serial.print(',');
    }
    Serial.println();
    return;
  }

  // --- Unknown command ---
  Serial.print(F("ERR unknown: "));
  Serial.println(cmd);
}

// ---- Read serial data, execute when newline received ----
void serialPoll() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (cmdIndex > 0) {
        cmdBuffer[cmdIndex] = '\0';
        executeCommand(cmdBuffer);
        cmdIndex = 0;
      }
    } else if (cmdIndex < CMD_BUF_SIZE - 1) {
      cmdBuffer[cmdIndex++] = c;
    }
  }
}

// ---- Watchdog: disable motors if no commands received ----
void watchdogCheck() {
  if (lastCmdTime > 0 && (millis() - lastCmdTime > WATCHDOG_TIMEOUT_MS)) {
    if (anyAxisMoving()) {
      // Don't disable mid-move, but do stop accepting new targets
      return;
    }
    // Only disable if idle and no commands for a while
    // (Don't actually disable here — just available for future use)
  }
}

#endif // SERIAL_PROTOCOL_H
