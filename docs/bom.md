# ARTIC-6 — Bill of Materials v0.3
> Last updated: March 2026  
> **Prioritizing AliExpress for cost efficiency.** Shipping takes 2-4 weeks.  
> Amazon alternatives listed where faster shipping is critical.

---

## Changelog — v0.3
- Switched to AliExpress links where possible (30-50% cheaper)
- Added direct AliExpress search links
- Reduced parts cost from $985 → $622 (core parts only)
- Added realistic all-in cost section ($988-$1,424 including tools, shipping, tax, spares)

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

| Qty | Part | Where to Buy | Specs | Each | Total |
|-----|------|-------------|-------|------|-------|
| 3 | **NEMA 23 Stepper — 1.9Nm, 2.8A, 8mm shaft** | [AliExpress](https://www.aliexpress.com/w/wholesale-nema-23-stepper-2.8a-8mm-shaft.html) | 57×57×76mm, 8mm D-shaft, 4-wire bipolar. **VERIFY 8mm shaft before buying** | $12 | $36 |
| 3 | **NEMA 17 Stepper — 2A, 59Ncm, 5mm shaft** | [AliExpress](https://www.aliexpress.com/w/wholesale-nema-17-stepper-59ncm.html) | 42×42×48mm, 1.8°, 4-wire bipolar | $8 | $24 |
| 8 | **TMC2209 V1.3 Driver** | [AliExpress](https://www.aliexpress.com/w/wholesale-tmc2209-v1.3-bigtreetech.html) | BTT or Fysetc brand. 2A cont, StallGuard4, UART. **Avoid generic clones** | $3 | $24 |

> ⚠️ **CRITICAL:** Verify NEMA 23 has 8mm shaft (not 6.35mm). Check listing photos for shaft diameter. BTT/Fysetc TMC2209 only — generic clones have wrong UART pinout.

**Motors + Drivers Subtotal: $84** *(was $166 on Amazon)*

---

## GEAR REDUCTION — ALL ALUMINUM — NO PRINTED PULLEYS

> 10:1 minimum on Axis 2 (shoulder) and Axis 3 (elbow).  
> 20T (motor) → 80T (joint) = **4:1 per stage**. Two stages = 16:1 theoretical, ~10-12:1 effective.

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 4 | **GT2 20T Pulley — 8mm bore, aluminum** | [AliExpress](https://www.aliexpress.com/w/wholesale-gt2-20t-pulley-8mm-bore-aluminum.html) | Fits NEMA 23 8mm shaft | $1.50 | $6 |
| 2 | **GT2 60T Pulley — 8mm bore, aluminum** | [AliExpress](https://www.aliexpress.com/w/wholesale-gt2-60t-pulley-8mm-bore.html) | 6mm belt width | $3 | $6 |
| 2 | **GT2 80T Pulley — 8mm bore, aluminum** | [AliExpress](https://www.aliexpress.com/w/wholesale-gt2-80t-pulley-8mm-bore-aluminum.html) | **Must be aluminum, NOT 3D printed** | $4 | $8 |
| 5m | **GT2 Open Belt — PU + steel core, 6mm** | [AliExpress](https://www.aliexpress.com/w/wholesale-gt2-belt-steel-core-6mm-open.html) | White PU, cut to length. **Order after CAD done** | $6 | $6 |
| 1 | **GT2 Belt Clamp Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-gt2-belt-clamp-6mm.html) | Copper buckles for open-loop ends | $3 | $3 |

> ⚠️ **Belt length:** Order after CAD is complete. Formula: Belt = 2×center_distance + π×(R_large + R_small)

**Gear Reduction Subtotal: $29** *(was $56 on Amazon)*

---

## COMPUTE & ELECTRONICS

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **Raspberry Pi 5 — 4GB** | [PiShop.us](https://www.pishop.us/) | Stock varies. Check PiShop first | $60 | $60 |
| 1 | **Arduino Mega 2560 Clone** | [AliExpress](https://www.aliexpress.com/w/wholesale-arduino-mega-2560-atmega16u2.html) | Get ATmega16U2 USB chip (not CH340) | $8 | $8 |
| 1 | **24V 10A DC PSU** | [AliExpress](https://www.aliexpress.com/w/wholesale-24v-10a-switching-power-supply.html) | 240W minimum | $12 | $12 |
| 1 | **5V 3A USB-C PSU (RPi)** | [AliExpress](https://www.aliexpress.com/w/wholesale-5v-3a-usb-c-power-supply.html) | Dedicated for RPi5 only | $6 | $6 |
| 1 | **22mm E-Stop Button — NC** | [AliExpress](https://www.aliexpress.com/w/wholesale-22mm-emergency-stop-button-NC.html) | Red mushroom, twist-release, **must be NC** | $3 | $3 |
| 10 | **KW11-3Z Limit Switch — SPDT** | [AliExpress](https://www.aliexpress.com/w/wholesale-kw11-3z-limit-switch.html) | Wire to NC terminal only | $0.30 | $3 |
| 1 | **8-Ch Opto-Isolated Relay** | [AliExpress](https://www.aliexpress.com/w/wholesale-8-channel-relay-opto-isolated-5v.html) | Must be opto-isolated | $4 | $4 |
| 1 | **Logic Level Converter 4-ch** | [AliExpress](https://www.aliexpress.com/w/wholesale-logic-level-converter-3.3v-5v-bidirectional.html) | 3.3V ↔ 5V bidirectional | $1 | $1 |
| 5 | **1000µF 35V Capacitor** | [AliExpress](https://www.aliexpress.com/w/wholesale-1000uf-35v-electrolytic-capacitor.html) | One per NEMA 23 driver + spares | $0.20 | $1 |
| 1 | **Ferrite Core Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-ferrite-bead-kit-usb-cable.html) | Snap-on type | $2 | $2 |

> ⚠️ **Limit switch wiring:** KW11-3Z has COM, NO, NC pins. Wire COM→+5V, NC→Arduino pin with 10kΩ pulldown. Wire break = pin goes LOW = arm stops (fail-safe).

**Compute + Electronics Subtotal: $100** *(was $165 on Amazon)*

---

## STRUCTURE & HARDWARE

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **SendCutSend — 3mm 6061-T6 Al** | [sendcutsend.com](https://sendcutsend.com/) | Base plate, 2× Link1, 2× Link2, brackets, mounts | — | $185 |
| 2 | **51100 Thrust Bearing (10×24×9mm)** | [AliExpress](https://www.aliexpress.com/w/wholesale-51100-thrust-bearing.html) | 10mm bore, 24mm OD. 1 spare | $2 | $4 |
| 20 | **M5 × 40mm Aluminum Standoffs** | [AliExpress](https://www.aliexpress.com/w/wholesale-m5-aluminum-standoff-40mm-hex.html) | Hex, male-female | $0.80 | $16 |
| 1 | **M3/M4/M5 Bolt & Nut Kit (500pc)** | [AliExpress](https://www.aliexpress.com/w/wholesale-metric-bolt-assortment-m3-m4-m5.html) | Socket head cap screws | $8 | $8 |
| 1 | **Brass Heat-Set Insert Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-heat-set-insert-m3-m4-brass.html) | M3/M4 for PETG parts | $5 | $5 |
| 20 | **608ZZ Bearings** | [AliExpress](https://www.aliexpress.com/w/wholesale-608zz-bearing.html) | 8×22×7mm. Buy 20, need 12 | $0.25 | $5 |
| 6 | **8mm Rigid Shaft Coupler** | [AliExpress](https://www.aliexpress.com/w/wholesale-8mm-rigid-shaft-coupler-aluminum.html) | Aluminum | $1.50 | $9 |
| 1 | **Fender Washer Kit — M3/M4/M5** | [AliExpress](https://www.aliexpress.com/w/wholesale-fender-washer-assortment-metric.html) | Under bolts touching PETG | $4 | $4 |

> ⚠️ **Standoff placement:** Every 100mm minimum. A 350mm link with only end standoffs will bow.

**Structure + Hardware Subtotal: $236** *(was $301 on Amazon — SendCutSend same price)*

---

## VISION & SENSING

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **Intel RealSense D435 — used** | [eBay](https://www.ebay.com/sch/i.html?_nkw=intel+realsense+d435) | Target $80-100 used. Check USB-C port | $90 | $90 |
| 1 | **1kg Load Cell + HX711** | [AliExpress](https://www.aliexpress.com/w/wholesale-1kg-load-cell-hx711.html) | Tare every grip cycle | $3 | $3 |
| 1 | **USB Microphone** | [AliExpress](https://www.aliexpress.com/w/wholesale-usb-microphone-mini.html) | Must be USB (RPi5 has no analog audio) | $8 | $8 |

**Vision + Sensing Subtotal: $101** *(was $130)*

---

## FILAMENT

> PETG: covers, housings, wrist assembly, gripper body only. No structural PETG near motors.

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 3 | **PETG Filament — 1kg** | [AliExpress](https://www.aliexpress.com/w/wholesale-petg-filament-1kg.html) | 230-240°C print temp | $12 | $36 |
| 1 | **TPU 95A Filament — 500g** | [AliExpress](https://www.aliexpress.com/w/wholesale-tpu-95a-filament-500g.html) | Gripper fingertips only | $8 | $8 |

**Filament Subtotal: $44** *(was $82)*

---

## WIRING & CABLE MANAGEMENT

| Qty | Part | Where to Buy | Notes | Each | Total |
|-----|------|-------------|-------|------|-------|
| 1 | **Silicone Wire Kit — 22/26AWG** | [AliExpress](https://www.aliexpress.com/w/wholesale-silicone-wire-kit-22awg-26awg.html) | High-flex, ≥200°C rated | $6 | $6 |
| 5m | **Shielded Twisted Pair — 24AWG** | [AliExpress](https://www.aliexpress.com/w/wholesale-shielded-twisted-pair-24awg.html) | For limit switches | $4 | $4 |
| 1 | **JST-XH Connector Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-jst-xh-connector-kit.html) | 2.54mm pitch | $4 | $4 |
| 1 | **Cable Drag Chain — 10×15mm, 1m** | [AliExpress](https://www.aliexpress.com/w/wholesale-cable-drag-chain-10x15.html) | Check bend radius | $4 | $4 |
| 1 | **Braided Cable Sleeve Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-braided-cable-sleeve-assortment.html) | | $3 | $3 |
| 1 | **Heat Shrink Tubing Kit** | [AliExpress](https://www.aliexpress.com/w/wholesale-heat-shrink-tubing-assortment.html) | | $2 | $2 |
| 1 | **Copper Ground Bus Bar** | [AliExpress](https://www.aliexpress.com/w/wholesale-ground-bus-bar-copper-10-way.html) | Star ground point | $3 | $3 |
| 1 | **12-Way Terminal Block** | [AliExpress](https://www.aliexpress.com/w/wholesale-terminal-block-12-way-10a.html) | Power distribution | $2 | $2 |

**Wiring Subtotal: $28** *(was $85)*

---

## REALISTIC ALL-IN COST

> **This is the honest total** — including tools, shipping, tax, consumables, and contingency.
> Most BOMs hide these. I'm not hiding anything.

### Parts List (Core Components)

| Category | Low Est. | High Est. |
|----------|----------|-----------|
| Core Parts (Motors, Electronics, Structure) | $580 | $640 |
| 3D Printing Filament (PETG + TPU) | $60 | $82 |
| SendCutSend Aluminum Cutting | $110 | $150 |
| **Parts Subtotal** | **$750** | **$872** |

### Hidden & Missed Costs (What Most BOMs Don't Show)

| Category | Low Est. | High Est. |
|----------|----------|-----------|
| Shipping — AliExpress | $18 | $35 |
| Shipping — Amazon | $0 | $20 |
| Sales Tax (~8%) | $45 | $70 |
| Tools (soldering iron, multimeter, crimpers) | $0 | $132 |
| Consumables (solder, flux, threadlocker, grease) | $33 | $58 |
| RPi Essentials (SD card, cooler, USB hub) | $30 | $48 |
| Prototyping (breadboard, jumpers, caps) | $17 | $28 |
| Installation (desk mount, velcro) | $14 | $25 |
| **Hidden Costs Subtotal** | **$157** | **$416** |

### Spares & Contingency

| Item | Low Est. | High Est. |
|------|----------|-----------|
| Spare NEMA 17 Motor (1x) | $12 | $12 |
| Spare TMC2209 Driver (2x) | $14 | $14 |
| DOA / Wrong Parts | $20 | $40 |
| Failed Prints / Wasted Filament | $15 | $30 |
| Oops Fund | $20 | $40 |
| **Spares & Contingency Subtotal** | **$81** | **$136** |

---

## 💰 GRAND TOTAL — REALISTIC

| | Low | High |
|--|-----|------|
| Parts List (accounted) | $750 | $872 |
| Hidden / Missed Costs | $157 | $416 |
| Spares & Contingency | $81 | $136 |
| **GRAND TOTAL** | **$988** | **$1,424** |

> If you own tools already (soldering iron, multimeter, wire strippers): subtract ~$100.
> Realistic midpoint estimate: **~$1,100-$1,200**.

---

## Phased Buying Plan

| Phase | What | Cost | When |
|-------|------|------|------|
| **1** | Fusion 360 Design | FREE | Month 1 |
| **2** | Structure & Motors | $434 | Month 1-2 |
| **3** | Electronics & Power | $147 | Month 2 |
| **4** | Brain & Senses | $268 | Month 2-3 |
| **5** | Tools, Consumables, Spares | $223 | Ongoing |
| | **TOTAL** | **$1,072** | |

---

## Blueprint Grant Request: $350

**I'm not asking for the full $1,100. I'm asking for $350 to cover Phase 2 motion components.**

| What Grant Covers | Cost |
|-------------------|------|
| 3× NEMA 23 Steppers | $36 |
| 3× NEMA 17 Steppers | $24 |
| 6× TMC2209 Drivers | $24 |
| GT2 Pulleys + Belt | $42 |
| Bolts, bearings, standoffs | $42 |
| Wiring supplies | $28 |
| Shipping (AliExpress) | $35 |
| Buffer for price changes | $119 |
| **Grant Request** | **$350** |

### What I'm Self-Funding

| What I Pay For | Cost |
|----------------|------|
| SendCutSend aluminum | $130 |
| Raspberry Pi 5 (4GB) | $60 |
| Intel RealSense D435 (used) | $95 |
| RPi essentials (SD, cooler, hub) | $46 |
| 24V PSU + Arduino + E-stop | $57 |
| Filament (PETG + TPU) | $82 |
| All tools (soldering, etc.) | $55 |
| All consumables | $58 |
| Spares & contingency | $136 |
| **My Contribution** | **~$719** |

> **Total project: ~$1,100 | Grant: $350 | Self-funded: ~$750**
> I'm covering 68% of the project myself.
