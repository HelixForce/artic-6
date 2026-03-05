// ============================================================
//  ARTIC-6 FIRMWARE — Main Sketch
//  Arduino Mega 2560 + 6× TMC2209 stepper drivers
//
//  REQUIRED LIBRARY:
//    AccelStepper by Mike McCauley
//    Install: Arduino IDE → Sketch → Include Library →
//             Manage Libraries → search "AccelStepper" → Install
//
//  UPLOAD:
//    Board: "Arduino Mega or Mega 2560"
//    Processor: "ATmega2560"
//    Port: (whatever COM port shows up)
//
//  SERIAL MONITOR:
//    115200 baud, Newline line ending
//    Type "PING" and hit enter — should respond "OK PONG"
// ============================================================

#include "config.h"
#include "stepper.h"
#include "homing.h"
#include "serial_protocol.h"

// Status LED — blinks to show firmware is running
#define LED_PIN 13  // Built-in LED on Mega (shared with DIR_PIN_6)
// Note: LED_PIN conflicts with DIR_PIN_6. The LED blink is disabled
// once motors are enabled. This is fine — you'll know it's alive
// from serial responses.

unsigned long lastStatusTime = 0;
#define STATUS_INTERVAL_MS 100  // Check limit switches every 100ms

void setup() {
  // Start serial to RPi
  Serial.begin(SERIAL_BAUD);
  while (!Serial) { ; } // Wait for USB serial (only needed on some boards)

  Serial.println(F(""));
  Serial.println(F("============================="));
  Serial.println(F("  ARTIC-6 Firmware v0.1"));
  Serial.println(F("  6-DOF Robot Arm Controller"));
  Serial.println(F("============================="));
  Serial.println(F(""));

  // Initialize limit switch pins (INPUT — external pull-down resistors)
  for (uint8_t i = 0; i < NUM_AXES; i++) {
    pinMode(LIMIT_PINS[i], INPUT);
  }

  // Initialize stepper motors (all disabled/free on startup)
  steppersInit();

  Serial.println(F("Motors initialized (disabled)"));
  Serial.println(F("Commands: PING, ENABLE, HOME, MOVE, POS, STATUS, STOP, ESTOP"));
  Serial.println(F("Type ENABLE then HOME before moving."));
  Serial.println(F(""));
  Serial.println(F("OK READY"));

  lastCmdTime = millis();
}

void loop() {
  // 1. Check for serial commands from RPi
  serialPoll();

  // 2. Run stepper motors (generates step pulses)
  //    This MUST be called as fast as possible for smooth motion
  steppersRun();

  // 3. Periodic safety checks
  if (millis() - lastStatusTime > STATUS_INTERVAL_MS) {
    lastStatusTime = millis();

    // Check limit switches during motion — stop axis if triggered
    if (!emergencyStop) {
      for (uint8_t i = 0; i < NUM_AXES; i++) {
        if (steppers[i].isRunning() && limitTriggered(i)) {
          steppers[i].stop();
          steppers[i].setCurrentPosition(steppers[i].currentPosition());
          Serial.print(F("WARN limit hit axis "));
          Serial.println(i + 1);
        }
      }
    }

    // Watchdog
    watchdogCheck();
  }
}
