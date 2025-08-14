## Flask Monitoring Web App

A lightweight monitoring platform for industrial cabinets that provides real‑time telemetry, alerting, and event evidence. It visualizes temperature data from multiple sensors, tracks motion, and captures images when a cabinet door is opened.

### Key capabilities
- **Real‑time charts**: Live line charts for IR object/ambient temperatures and DS18B20 readings, rendered with Chart.js and streamed via Turbo‑Flask.
- **Alarm thresholds**: Configure per‑sensor thresholds and see instant OK/NOK state on the interactive cabinet map.
- **Event logging**: Temperature reads, alarm detections, motion, door open, and camera captures logged to SQLite.
- **Photo evidence**: Raspberry Pi Camera captures images on door‑open events with a gallery view.
- **Responsive UI**: Simple Flask/Jinja templates with an interactive map and gallery.

### High‑level architecture
- **Web application** (`load/app.py`): Flask server with Turbo‑Flask server‑sent updates, Jinja templates, and static assets.
- **Data collector** (`load/collectData.py`): Runs on Raspberry Pi. Reads sensor data from STM32 over UART (`/dev/ttyS0`), samples light (I2C) and motion (ADXL345), and triggers PiCamera captures.
- **Database**: SQLite file `load/sensors.db` with tables:
  - `sensors(timestamp, SensorIR1Ob..8Ob, SensorIR1Am..8Am, SensorDS1..8)`
  - `alertsValues(SetValue, SensorIR1Ob..8Ob, SensorIR1Am..8Am, SensorDS1..8)`
  - `photos(timestamp, photoName)`
  - `logs(timestamp, Log)`

### UI routes
- **GET /**: Dashboard with interactive sensor map, live charts, and a live log stream.
- **GET /alert**: Configure alarm thresholds and review recent log entries.
- **GET /gallery**: View captured images with timestamps.
- **GET/POST /login**: Simple placeholder login view.
- **POST /processSensorInfo/<json>**: Switch chart source (IR vs DS sensors).
- **POST /processAlertInfo/<json>**: Update threshold for a selected sensor.

## Getting started

### Prerequisites
- Python 3.9+ on the host running the web app
- SQLite (included with Python stdlib)
- For the data collector (Raspberry Pi):
  - `smbus` (I2C), `board`, `busio`, `adafruit-adxl34x`
  - `picamera`
  - `pyserial`
  - Access to `/dev/ttyS0` and I2C enabled

### Install (web application)
```bash
cd load
python3 -m venv .venv
source .venv/bin/activate
pip install flask turbo-flask pyserial adafruit-circuitpython-adxl34x smbus2 picamera2  # install only what you need for your environment
```

If you are only running the web UI on a non‑Pi machine, you typically need just:
```bash
pip install flask turbo-flask
```

### Database initialization
Tables are created automatically by `load/sql.py` or `load/collectData.py` on first run. To pre‑create them:
```bash
python load/sql.py
```

Optionally seed default alert thresholds (example shown for a single preset named "Set1"):
```sql
INSERT INTO alertsValues (
  SetValue,
  SensorIR1Ob, SensorIR2Ob, SensorIR3Ob, SensorIR4Ob, SensorIR5Ob, SensorIR6Ob, SensorIR7Ob, SensorIR8Ob,
  SensorIR1Am, SensorIR2Am, SensorIR3Am, SensorIR4Am, SensorIR5Am, SensorIR6Am, SensorIR7Am, SensorIR8Am,
  SensorDS1, SensorDS2, SensorDS3, SensorDS4, SensorDS5, SensorDS6, SensorDS7, SensorDS8
) VALUES (
  'Set1', 100,100,100,100,100,100,100,100, 100,100,100,100,100,100,100,100, 100,100,100,100,100,100,100,100
);
```

### Configure
- Review `load/app.py` static folder declaration. For portability, set it to Flask’s default by removing the custom path or updating it to your environment:
  - `app = Flask(__name__)`
- Ensure images are stored under `load/static/css/images/` to appear in the gallery.
- The login form uses placeholder credentials; replace them in `load/app.py` as needed.

### Run the web application
```bash
python load/app.py
# App runs on http://0.0.0.0:5000 by default
```

### Run the data collector (on Raspberry Pi)
```bash
python load/collectData.py
```
This process will:
- Read JSON telemetry over UART from the STM32
- Store samples in `sensors` table
- Watch light level and motion events to log door opens/moves
- Capture images with PiCamera into `load/static/css/images/`

## Technology stack
- **Backend**: Flask, Turbo‑Flask (server‑sent updates), SQLite
- **Frontend**: Jinja2 templates, Chart.js
- **Hardware integration**: UART (STM32 → Pi), I2C (BH1750 light, ADXL345 accelerometer), Raspberry Pi Camera

## Screens
You can find assets in `load/static/css` and example images under `load/static/css/images/`.

## Notes and considerations
- Absolute paths in code may require adjustment for your deployment environment.
- Long‑running background tasks are scheduled via `threading.Timer` in `load/app.py` and `load/collectData.py`.
- The repository includes a sample `sensors.db`; you can start with it or build one from live data.

