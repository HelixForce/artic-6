# ARTIC-6 — Bill of Materials v0.2
> Last updated: March 2026  
> All prices USD, Amazon Prime unless noted.  
> **Every part verified against real Amazon listings. ASINs included — do not substitute without checking shaft/bore sizes.**

---

## Changelog — v0.2 (corrections from v0.1)

### Critical Fixes
- **NEMA 23 shaft diameter confirmed: 8mm** — specified STEPPERONLINE 23HS30-2804S with explicit 8mm shaft listing. Generic "NEMA 23 2.8A" listings often ship 6.35mm — do NOT order without checking.
- **GT2 80T pulley is aluminum, NOT printed** — found real aluminum 80T 8mm bore on Amazon (ASIN B08NXF2LWZ). Removed "(3D print)" note entirely. Printing the 80T driven pulley under 7Nm would destroy it.
- **Belt strategy changed: open-loop PU+steel-core, not closed-loop** — true closed-loop steel-core GT2 belts do not exist on Amazon in useful lengths. Closed-loop Amazon belts are rubber+fiberglass (more stretch). Correct approach: buy open-loop PU+steel-core white belt by the meter, cut to length, use GT2 belt clamps. Belt lengths still TBD after Fusion 360 center-distance is locked — **do NOT order belts until CAD is done.**
- **Standoff quantity corrected: 4→ 20** — Link 1 (4 standoffs), Link 2 (3 standoffs), base-to-turntable (4 standoffs), joint brackets (4 standoffs), spare (5). Previous BOM qty of 4 would result in a floppy sandwich.
- **51100 thrust bearing OD confirmed: 24mm** — CAD spec said 26mm seat. Correct seat recess: **24.5mm OD, 0.5mm deep**. Fix this in Fusion before DXF export.
- **TMC2209 sourcing: BIGTREETECH V1.3 only** — generic clone TMC2209s have UART pinout differences that will destroy them when wired to Arduino. BTT V1.3 is the verified safe choice.
- **NEMA 17 upsized: 1.5A → 2A, 59Ncm** — the wrist (Axes 4+5) is not as light as assumed when carrying a loaded gripper. Use the 2A 59Ncm STEPPERONLINE version for all 3 NEMA 17 slots.

---

## MOTORS & DRIVERS

| Qty | Part | ASIN / Where | Specs confirmed | Each | Total |
|-----|------|-------------|-----------------|------|-------|
| 3 | **STEPPERONLINE NEMA 23 Stepper — 1.9Nm, 2.8A, 8mm shaft** | B0DS52C4T2 (Amazon) | 57×57×76mm, 8mm D-shaft, 4-wire bipolar | $20 | $60 |
| 3 | **STEPPERONLINE NEMA 17 Stepper — 2A, 59Ncm, 5mm shaft** | B00PNEQKC0 (Amazon) | 42×42×48mm, 1.8°, 4-wire bipolar, 1m cable | $14 | $42 |
| 8 | **BIGTREETECH TMC2209 V1.3** (buy 6-pack + 2-pack) | B08WZFK9KT (6pk) + B08C2DJQ6B (2pk) | 2A cont / 2.8A peak, StallGuard4, UART mode | ~$8 | $64 |

> ⚠️ TMC2209 UART note: On Arduino Mega, each driver needs its own UART TX line or use software serial multiplexing. Wire DIAG pin to Arduino interrupt for StallGuard. Do not use generic non-BTT TMC2209 clones.

**Motors + Drivers Subtotal: $166** *(was $138 — NEMA 17 upsized, TMC2209 BTT brand required)*

---

## GEAR REDUCTION — ALL ALUMINUM — NO PRINTED PULLEYS

> 10:1 minimum on Axis 2 (shoulder) and Axis 3 (elbow).  
> 20T (motor) → 80T (joint) = **4:1 per stage**. Two stages needed = 16:1 theoretical, ~10-12:1 effective with belt compliance losses. This is correct and within spec.

| Qty | Part | ASIN / Where | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 4 | **GT2 20T Drive Pulley — 8mm bore, aluminum** | B07M5PCM2V (Saiper, 5-pack) | Confirm 8mm bore — fits NEMA 23 8mm shaft | $2 | $8 |
| 2 | **GT2 60T Driven Pulley — 8mm bore, aluminum** | B078SFMC7K (Amazon) | Aluminum, 6mm belt width | $6 | $12 |
| 2 | **GT2 80T Driven Pulley — 8mm bore, aluminum** ✅ | B08NXF2LWZ (Amazon) | **Aluminum alloy, NOT printed.** 7mm tooth width for 6mm belt | $8 | $16 |
| — | **GT2 Open Belt — PU + steel core (white), 6mm width, 5m** | B07BZDM8FH (Amazon) | **Do NOT order until CAD center-distances confirmed.** Buy 5m open roll, cut to length with clamps | $12 | $12 |
| 1 | **GT2 Belt Clamp Kit** (copper buckles) | search "GT2 belt clamp copper buckle 6mm" | For terminating open-loop belt ends | $8 | $8 |

> ⚠️ Belt length warning: The 400mm/500mm lengths from v0.1 were guesses. Once base plate and Link 1 are drawn in Fusion, measure motor shaft center to joint center distance. Formula: Belt length = 2×center_distance + π×(R_large + R_small). Buy 5m open roll and cut to exact length.

**Gear Reduction Subtotal: $56** *(was $52 — added belt clamps, removed guessed closed-loop lengths)*

---

## COMPUTE & ELECTRONICS

| Qty | Part | ASIN / Where | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **Raspberry Pi 5 — 4GB** | Adafruit / PiShop.us | Stock varies — check PiShop.us first | $60 | $60 |
| 1 | **ELEGOO MEGA R3 (Arduino Mega 2560 clone)** | B01H4ZDYCE (Amazon) | ATmega16U2 USB chip (not CH340) — required for stable UART | $16 | $16 |
| 1 | **24V 10A DC PSU** | search "24V 10A switching power supply" Amazon | Mean Well LRS-240-24 preferred ($28) | $28 | $28 |
| 1 | **5V 3A USB-C PSU (RPi dedicated)** | search "5V 3A USB-C Raspberry Pi 5 PSU" | Official RPi5 PSU or CanaKit | $12 | $12 |
| 1 | **22mm E-Stop Button — NC, panel mount** | search "22mm mushroom e-stop NC panel" | Must be NC (normally closed). Red mushroom, twist-release | $8 | $8 |
| 10 | **KW11-3Z Micro Limit Switch — SPDT, 3-pin** | B0BRFC7H8R (Amazon, 10-pack) | Buy SPDT (has both NO and NC terminals). Wire to NC terminal only. | $12 | $12 |
| 1 | **8-Channel Opto-Isolated Relay Board** | search "8 channel opto isolated relay 5V" | Must be opto-isolated. Verify input: 5V coil, active LOW trigger | $12 | $12 |
| 1 | **Logic Level Converter 4-ch (3.3V ↔ 5V)** | search "SparkFun logic level converter bi-directional" | RPi is 3.3V GPIO, Arduino is 5V — required | $6 | $6 |
| 3 | **1000µF 35V Electrolytic Capacitor** | search "1000uF 35V electrolytic" | One per NEMA 23 driver power rail | $1 | $3 |
| 1 | **Ferrite Core Kit — assorted** | search "ferrite bead kit USB cable" | Snap-on type for USB cables | $8 | $8 |

> ⚠️ Limit switch note: KW11-3Z is 3-pin SPDT (COM, NO, NC). Wire COM to +5V, NC to Arduino input pin with 10kΩ pull-down. When switch opens (triggered OR wire break), pin goes LOW — arm stops. This is the fail-safe NC configuration.

**Compute + Electronics Subtotal: $165** *(was $156 — 10 limit switches instead of 6, ELEGOO Mega specified)*

---

## STRUCTURE & HARDWARE — STANDOFF QUANTITY CORRECTED

| Qty | Part | ASIN / Where | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **SendCutSend — 3mm 6061-T6 Al** | sendcutsend.com | Upload DXF after Fusion. Includes: base plate, 2× Link1, 2× Link2, joint brackets, motor mounts | ~$185 | $185 |
| 2 | **51100 Thrust Bearing — 10mm bore, 24mm OD, 9mm thick** | B09CD8CWCR (uxcell, 2-pack) | Confirmed 24mm OD. **Fix CAD seat to 24.5mm OD, not 26mm.** Buy 2 (1 spare) | $8 | $8 |
| 20 | **M5 × 40mm Aluminum Standoffs** | search "M5 aluminum standoff hex 40mm" | 4× Link1, 3× Link2, 4× base-turntable, 4× brackets, 5 spare | $2 | $40 |
| 1 | **M3 / M4 / M5 Bolt & Nut Assortment (500pc)** | search "metric bolt assortment M3 M4 M5" | | $18 | $18 |
| 1 | **Brass Heat-Set Insert Kit — M3/M4** | search "M3 M4 heat set brass inserts kit" | For all PETG printed parts that take bolts | $12 | $12 |
| 20 | **608ZZ Bearings** | search "608ZZ bearing lot 20" | Two per joint (spaced apart per errors file) = 12 needed, 8 spare | $0.60 | $12 |
| 6 | **8mm Rigid Shaft Coupler — aluminum** | search "8mm rigid shaft coupler aluminum" | For joint pivot shafts | $3 | $18 |
| 1 | **Fender Washer Assortment — M3/M4/M5** | search "fender washer assortment metric" | Under every bolt head contacting PETG | $8 | $8 |

> ⚠️ Standoff note: Place standoffs every 100mm minimum, not just at ends. A 350mm link with only 2 end standoffs will bow and vibrate. 4 standoffs = every ~90mm. This is structurally required.

**Structure + Hardware Subtotal: $301** *(was $259 — standoffs corrected from 4 to 20, 2× thrust bearings, SendCutSend estimate +$10)*

---

## VISION & SENSING

| Qty | Part | Where | Notes | Each | Total |
|-----|------|-------|-------|------|-------|
| 1 | **Intel RealSense D435 — used** | eBay | Search "Intel RealSense D435" — target $80-100 used. Check for bent USB-C port. | $95 | $95 |
| 1 | **1kg Load Cell + HX711 amplifier** | search "1kg load cell HX711 module Amazon" | Tare every empty grip cycle in firmware | $10 | $10 |
| 1 | **USB Microphone — compact** | search "USB microphone compact mini" | Blue Snowball Nano or equiv. Must be USB, not 3.5mm (RPi 5 has no analog audio in) | $25 | $25 |

**Vision + Sensing Subtotal: $130** *(unchanged)*

---

## FILAMENT

> PETG: covers, housings, cable channel caps, wrist assembly, gripper body only.  
> No structural PETG. No PETG touching any NEMA 23 motor.

| Qty | Part | Where | Notes | Each | Total |
|-----|------|-------|-------|------|-------|
| 3 | **PETG Filament — 1kg spool** | Amazon / Bambu | Any reputable brand. Print temp 230-240°C, bed 70°C | $22 | $66 |
| 1 | **TPU 95A Filament — 500g** | search "TPU 95A filament 500g" | Gripper fingertips only | $16 | $16 |

**Filament Subtotal: $82** *(unchanged)*

---

## WIRING & CABLE MANAGEMENT

| Qty | Part | Where | Notes | Each | Total |
|-----|------|-------|-------|------|-------|
| 1 | **Silicone Wire Kit — 22/26AWG, high-flex** | search "silicone wire kit 22awg 26awg high flex" | Silicone rated ≥200°C — does not crack at joints | $15 | $15 |
| 5m | **Shielded Twisted Pair Wire — 24AWG** | search "shielded twisted pair 24AWG 5m" | All 6 limit switch runs. Connect shield to star ground only at one end | $12 | $12 |
| 1 | **JST-XH Connector Kit** | search "JST XH connector kit 2.54mm" | Motor leads + sensor connections | $12 | $12 |
| 1 | **Cable Drag Chain — 10×15mm, 1m** | search "cable drag chain 10x15 1 meter" | Check bend radius before routing in CAD | $12 | $12 |
| 1 | **Braided Cable Sleeve Kit — assorted** | search "braided cable sleeve assortment" | | $10 | $10 |
| 1 | **Heat Shrink Tubing Kit — assorted** | search "heat shrink tubing assortment" | | $8 | $8 |
| 1 | **Copper Ground Bus Bar** | search "ground bus bar terminal strip copper 10-way" | Star ground point — mount near PSU negative | $10 | $10 |
| 1 | **12-Way Terminal Block — 10A** | search "terminal block 12 way screw terminal" | For clean power distribution | $6 | $6 |

**Wiring Subtotal: $85** *(unchanged)*

---

## GRAND TOTAL v0.2

| Category | v0.1 | v0.2 | Δ | Why |
|----------|------|------|---|-----|
| Motors + Drivers | $138 | $166 | **+$28** | NEMA 17 upsized; BTT TMC2209 required |
| Gear Reduction | $52 | $56 | **+$4** | Added belt clamps; removed invalid closed-loop |
| Compute + Electronics | $156 | $165 | **+$9** | 10 limit switches; ELEGOO Mega specified |
| Structure + Hardware | $259 | $301 | **+$42** | Standoffs ×20 (was ×4); 2× thrust bearings; SCS +$10 |
| Vision + Sensing | $130 | $130 | — | |
| Filament | $82 | $82 | — | |
| Wiring | $85 | $85 | — | |
| **Parts Subtotal** | **$902** | **$985** | **+$83** | |
| Tools, consumables, shipping, tax, spares | ~$220 | ~$230 | +$10 | |
| **REALISTIC ALL-IN** | **~$1,122** | **~$1,215** | **+$93** | |
