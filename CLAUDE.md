# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

ESPHome firmware config for a 24 V lead-acid battery monitor: a Peacefair **PZEM-017** DC meter (Modbus RTU over RS485) read by an **ESP32 DOIT DevKit V1** through a 3.3 V MAX3485 module, with a 16x2 HD44780 LCD (Winstar WH1602A, parallel 4-bit), exposed to Home Assistant via the native ESPHome API. There is no application code — `battery-monitor.yaml` is the whole firmware; `README.md` is the user-facing hardware/setup guide.

## Commands

Windows host. ESPHome lives in a local venv (`.venv/`, created from the Microsoft Store Python).

**Run all ESPHome builds from PowerShell or cmd, never Git Bash** — ESP-IDF aborts with `MSys/Mingw is not supported` when `MSYSTEM` is set. In PowerShell also clear it defensively: `Remove-Item Env:MSYSTEM -ErrorAction SilentlyContinue`.

```powershell
.venv\Scripts\esphome config  battery-monitor.yaml          # validate only (fast)
.venv\Scripts\esphome compile battery-monitor.yaml          # build (first run downloads ESP-IDF, several minutes)
$ip = (Get-Content .env | Select-String '^ESP_IP=').Line.Split('=')[1]
.venv\Scripts\esphome run battery-monitor.yaml --device $ip # OTA flash + logs
.venv\Scripts\esphome logs battery-monitor.yaml --device $ip
```

USB flashing (board on COM13 with the Silicon Labs CP210x driver): the DOIT board does **not** auto-enter download mode, so `esphome upload` fails with `Wrong boot mode detected (0x13)`. Have the user hold BOOT, tap EN, release BOOT, then flash with esptool without auto-reset:

```powershell
.venv\Scripts\python -m esptool --chip esp32 --port COM13 --baud 460800 --before no-reset --after hard-reset write-flash -z --flash-size detect 0x0 .esphome\build\battery-monitor\build\firmware.factory.bin
```

Reading the serial boot log (IP, MAC, Modbus errors) works by opening `System.IO.Ports.SerialPort` at 115200 and pulsing RTS to reset; keep DTR low or the chip boots into download mode.

Wiring diagram: `docs/wiring.svg` is generated, not hand-edited.

```bash
python docs/gen_wiring.py docs/wiring.svg
```

Then re-render `docs/wiring.png` with headless Edge (`msedge --headless=new --window-size=1820,1060 --screenshot=docs\wiring.png file:///.../docs/wiring.svg`) and view the PNG to check for overlapping labels/wires.

## Things that must stay in sync

Pin assignments appear in three places — the header comment of `battery-monitor.yaml`, the wiring tables in `README.md`, and the coordinates/labels in `docs/gen_wiring.py`. Change all three together. Current map: UART2 TX=GPIO17/RX=GPIO16, RS485 DE+RE=GPIO4 (`flow_control_pin`), LCD RS=32 E=33 D4..D7=25/26/27/14.

## PZEM-017 Modbus specifics

- Serial is **9600 8N2** (two stop bits), slave address 0x01.
- Input registers (fn 0x04): 0x0000 V (×0.01), 0x0001 A (×0.01), 0x0002–3 W (×0.1, 32-bit **low word first** → `U_DWORD_R`), 0x0004–5 Wh (same order), 0x0006/0x0007 high/low voltage alarm (0xFFFF = alarm).
- Holding registers (fn 0x03/0x06): 0x0000/0x0001 alarm thresholds (×0.01 V), 0x0002 address, 0x0003 shunt range (0=100 A, 1=50 A, 2=200 A, 3=300 A). The shunt range must match the physical shunt or current/power are mis-scaled.
- Do not add `register_count` to modbus_controller sensors; current ESPHome derives it from `value_type` and warns.
- The meter is **unidirectional**: charging current reads 0 and energy only accumulates discharge, so it cannot provide state of charge.
- Modbus "Stop waiting for response" warnings are expected whenever the PZEM/RS485 side is not connected.

## Secrets and local files

`secrets.yaml` (real WiFi creds, API encryption key, OTA and fallback-AP passwords) and `.env` (`ESP_IP`, the fixed DHCP lease set in pfSense for the board's MAC; read the MAC from the serial boot log, `Local MAC:` line) are gitignored; `secrets.example.yaml` and `.env.example` must contain placeholders only. The HA integration authenticates with `api_encryption_key`; changing it requires re-entering the key in Home Assistant.
