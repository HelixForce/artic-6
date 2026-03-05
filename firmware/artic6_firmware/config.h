#ifndef CONFIG_H
#define CONFIG_H

// ============================================================
//  ARTIC-6 FIRMWARE CONFIGURATION
//  Arduino Mega 2560 + TMC2209 drivers
//  All pin assignments match wiring_diagram.md
// ============================================================

// --- Number of axes ---
#define NUM_AXES 6

// --- STEP pins (D2-D7) ---
// One pulse on STEP = one microstep movement
#define STEP_PIN_1  2   // Axis 1: Base rotation (NEMA 23)
#define STEP_PIN_2  3   // Axis 2: Shoulder      (NEMA 23)
#define STEP_PIN_3  4   // Axis 3: Elbow          (NEMA 23)
#define STEP_PIN_4  5   // Axis 4: Wrist pitch    (NEMA 17)
#define STEP_PIN_5  6   // Axis 5: Wrist roll     (NEMA 17)
#define STEP_PIN_6  7   // Axis 6: Gripper rot    (NEMA 17)

const uint8_t STEP_PINS[NUM_AXES] = {
  STEP_PIN_1, STEP_PIN_2, STEP_PIN_3,
  STEP_PIN_4, STEP_PIN_5, STEP_PIN_6
};

// --- DIR pins (D8-D13) ---
// HIGH/LOW sets rotation direction
#define DIR_PIN_1   8
#define DIR_PIN_2   9
#define DIR_PIN_3   10
#define DIR_PIN_4   11
#define DIR_PIN_5   12
#define DIR_PIN_6   13

const uint8_t DIR_PINS[NUM_AXES] = {
  DIR_PIN_1, DIR_PIN_2, DIR_PIN_3,
  DIR_PIN_4, DIR_PIN_5, DIR_PIN_6
};

// --- ENABLE pins (D22-D27) ---
// LOW = motor energized, HIGH = motor free (TMC2209 convention)
#define EN_PIN_1    22
#define EN_PIN_2    23
#define EN_PIN_3    24
#define EN_PIN_4    25
#define EN_PIN_5    26
#define EN_PIN_6    27

const uint8_t EN_PINS[NUM_AXES] = {
  EN_PIN_1, EN_PIN_2, EN_PIN_3,
  EN_PIN_4, EN_PIN_5, EN_PIN_6
};

// --- LIMIT SWITCH pins (D28-D33) ---
// Wired NC (normally closed) with 10k pull-down
// HIGH = normal (switch closed), LOW = triggered or wire broken = STOP
#define LIMIT_PIN_1  28
#define LIMIT_PIN_2  29
#define LIMIT_PIN_3  30
#define LIMIT_PIN_4  31
#define LIMIT_PIN_5  32
#define LIMIT_PIN_6  33

const uint8_t LIMIT_PINS[NUM_AXES] = {
  LIMIT_PIN_1, LIMIT_PIN_2, LIMIT_PIN_3,
  LIMIT_PIN_4, LIMIT_PIN_5, LIMIT_PIN_6
};

// --- MOTOR PARAMETERS ---

// Microstep setting on TMC2209 (set via MS1/MS2 pins or UART)
// 8 microsteps is a good balance of smoothness vs speed
#define MICROSTEPS 8

// Steps per revolution: 200 full steps × microsteps
#define STEPS_PER_REV (200L * MICROSTEPS)  // = 1600

// Belt reduction ratios (motor turns : joint turns)
// 20T motor pulley → 80T joint pulley = 4:1 per stage
// Axes 1-3: two-stage 4:1 = 16:1 (NEMA 23)
// Axes 4-6: single-stage or direct (NEMA 17) — TBD after wrist design
#define REDUCTION_1  16.0   // Base rotation
#define REDUCTION_2  16.0   // Shoulder
#define REDUCTION_3  16.0   // Elbow
#define REDUCTION_4   4.0   // Wrist pitch (single stage)
#define REDUCTION_5   4.0   // Wrist roll
#define REDUCTION_6   1.0   // Gripper (direct drive or low ratio)

const float REDUCTIONS[NUM_AXES] = {
  REDUCTION_1, REDUCTION_2, REDUCTION_3,
  REDUCTION_4, REDUCTION_5, REDUCTION_6
};

// Steps per degree of joint rotation
// = (STEPS_PER_REV * reduction) / 360
// Axis 1: (1600 * 16) / 360 = 71.11 steps/degree
// Axis 2: same
// Axis 4: (1600 * 4) / 360 = 17.78 steps/degree

// Max speeds (steps/sec) — conservative starting values
// NEMA 23 at 2.8A can typically do ~2000 steps/sec at 8 microsteps
// NEMA 17 at 2A can do ~3000 steps/sec
#define MAX_SPEED_1     1500   // Base (slow — heavy inertia)
#define MAX_SPEED_2     1200   // Shoulder (slowest — full arm load)
#define MAX_SPEED_3     1500   // Elbow
#define MAX_SPEED_4     2500   // Wrist pitch
#define MAX_SPEED_5     2500   // Wrist roll
#define MAX_SPEED_6     3000   // Gripper

const long MAX_SPEEDS[NUM_AXES] = {
  MAX_SPEED_1, MAX_SPEED_2, MAX_SPEED_3,
  MAX_SPEED_4, MAX_SPEED_5, MAX_SPEED_6
};

// Max acceleration (steps/sec²)
// Lower = smoother but slower. Higher = more responsive but can skip steps.
#define MAX_ACCEL_1     800
#define MAX_ACCEL_2     600   // Shoulder needs gentle accel (heavy load)
#define MAX_ACCEL_3     800
#define MAX_ACCEL_4     1500
#define MAX_ACCEL_5     1500
#define MAX_ACCEL_6     2000

const long MAX_ACCELS[NUM_AXES] = {
  MAX_ACCEL_1, MAX_ACCEL_2, MAX_ACCEL_3,
  MAX_ACCEL_4, MAX_ACCEL_5, MAX_ACCEL_6
};

// Joint limits (degrees from home position)
// Axis 1 has hard stops at ±170°
#define JOINT_MIN_1   -170.0
#define JOINT_MAX_1    170.0
#define JOINT_MIN_2    -30.0   // Shoulder can't go far behind
#define JOINT_MAX_2    120.0
#define JOINT_MIN_3   -120.0   // Elbow folds back
#define JOINT_MAX_3     30.0
#define JOINT_MIN_4    -90.0
#define JOINT_MAX_4     90.0
#define JOINT_MIN_5   -180.0
#define JOINT_MAX_5    180.0
#define JOINT_MIN_6    -90.0
#define JOINT_MAX_6     90.0

const float JOINT_MINS[NUM_AXES] = {
  JOINT_MIN_1, JOINT_MIN_2, JOINT_MIN_3,
  JOINT_MIN_4, JOINT_MIN_5, JOINT_MIN_6
};
const float JOINT_MAXS[NUM_AXES] = {
  JOINT_MAX_1, JOINT_MAX_2, JOINT_MAX_3,
  JOINT_MAX_4, JOINT_MAX_5, JOINT_MAX_6
};

// Homing direction: -1 = toward negative limit, +1 = toward positive
#define HOME_DIR_1  -1
#define HOME_DIR_2  -1
#define HOME_DIR_3   1
#define HOME_DIR_4  -1
#define HOME_DIR_5  -1
#define HOME_DIR_6  -1

const int8_t HOME_DIRS[NUM_AXES] = {
  HOME_DIR_1, HOME_DIR_2, HOME_DIR_3,
  HOME_DIR_4, HOME_DIR_5, HOME_DIR_6
};

// Homing speed (steps/sec) — slow for accuracy
#define HOMING_SPEED_FAST   800   // Initial approach
#define HOMING_SPEED_SLOW   200   // Back off and re-approach

// Home position offset (degrees from limit switch to "zero")
// After hitting the limit switch, move this many degrees to reach home
const float HOME_OFFSETS[NUM_AXES] = {
  5.0, 5.0, 5.0, 3.0, 3.0, 3.0
};

// --- SERIAL COMMUNICATION ---
#define SERIAL_BAUD  115200   // USB serial to Raspberry Pi

// --- SAFETY ---
#define ESTOP_DEBOUNCE_MS    50
#define LIMIT_DEBOUNCE_MS    20
#define WATCHDOG_TIMEOUT_MS  2000  // If no command in 2s, disable motors

#endif // CONFIG_H
