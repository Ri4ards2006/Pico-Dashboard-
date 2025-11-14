
Hier eine professionelle, lockere und detaillierte **README.md** für dein Pico-Dashboard-Projekt auf Englisch – mit Emojis, Tables und allen essenziellen Infos, die Nutzer schnell einsteigen lassen! 🚀  

---

# 🌡️ Pico-Dashboard – Real-Time Weather Station Web Interface 🌐  
*Bridging hardware sensors to your browser – turn your DIY weather station into a smart tool!*  

## **Overview 📖**  
**Pico-Dashboard** is an advanced web dashboard for DIY weather stations built around the **Raspberry Pi Pico W**. 🖥️  
It receives sensor data from one or more **Arduino-based sensor nodes** via wireless modules 📡, processes data in real-time, and visualizes it through a web server 📊.  

This project combines **microcontroller programming, IoT communication, web development, and data visualization** – perfect for makers and developers looking to showcase end-to-end skills in their portfolio 🚀.  

---

## **Goals & Benefits 🎯**  
| **Goal** | **Why It Matters** |  
|----------|--------------------|  
| Real-time data visualization | Watch temperature, humidity, and pressure trends live – no delays! 🌧️ |  
| Multi-node wireless network | No more cables! Connect sensors across your home or workspace 🏠 |  
| Easy extensibility | Add new sensors (CO₂, light) or alerts (Telegram, email, LED) with minimal effort 🚨 |  
| Portfolio-worthy demo | Show hardware + software + web expertise in one repo – boost your GitHub profile! 🌟 |  

---

## **Hardware Requirements 🛠️**  
### **Essential Components**  
| Component | Role | Recommended Version | Where to Buy (Examples) |  
|-----------|------|----------------------|--------------------------|  
| Raspberry Pi Pico W | Web server & data receiver | RP2040 (latest firmware) | [Amazon](https://amzn.to/3ZqZJqJ) | [Raspberry Pi Shop](https://www.raspberrypi.com/products/raspberry-pi-pico-w/) |  
| Arduino Mega 2560 | Sensor data collection & wireless transmitter | ATmega2560 (standard) | [AliExpress](https://www.aliexpress.com/item/arduino-mega-2560.html) |  
| DHT22 or BME280 | Measures temperature, humidity, pressure | DHT22 (budget) / BME280 (precision) | [SparkFun](https://www.sparkfun.com/products/13879) |  
| nRF24L01 or HC-12 | 2.4 GHz wireless communication | nRF24L01 (long-range) | [Amazon](https://amzn.to/3CqZ7Qv) |  
| MicroUSB Cables | Power supply for Pico W/Arduino | 5V/2A (generic) | Any electronics store |  

### **Optional Add-Ons**  
| Component | Use Case | Version |  
|-----------|----------|---------|  
| OLED Display (SSD1306) | Local data preview (no PC needed) | 128x64 pixels | [Amazon](https://amzn.to/3CtX8mZ) |  
| Breadboard + Jumper Wires | Prototyping sensor connections | Standard (700+ wires) | [Conrad](https://www.conrad.de/ce/de/product/1195333/) |  

---

## **Software & Libraries 💾**  
### **Tools & Versions**  
| Tool | Version | Purpose | Documentation |  
|------|---------|---------|---------------|  
| MicroPython | 1.22.0+ | Pico W programming | [MicroPython Docs](https://docs.micropython.org/) |  
| Arduino IDE | 2.0+ | Compile Arduino code | [Arduino IDE](https://www.arduino.cc/en/software) |  
| Chart.js | 4.4.0+ | Web data visualization | [Chart.js Docs](https://www.chartjs.org/docs/latest/) |  

### **Required Libraries**  
| Library | Platform | Function | Installation |  
|---------|----------|----------|--------------|  
| `RF24` | Arduino | Control nRF24L01 wireless modules | Install via Arduino Library Manager ↗️ [GitHub](https://github.com/TMRh20/RF24) |  
| `ujson` | MicroPython | Parse JSON data | Included in modern MicroPython versions |  
| `umqtt.robust` | MicroPython (optional) | MQTT cloud integration (e.g., Adafruit IO) | `pip install umqtt.robust` |  

---

## **Key Features ✨**  
| **Feature** | **Description** | **Visual Update** |  
|-------------|-----------------|-------------------|  
| Real-time data reception | Sensors ping every 1 second 📈 | Web charts update every 2 seconds ⏳ |  
| Multi-node support | Connect up to 5 Arduino nodes simultaneously 🔗 | Table shows node names, temp, humidity 📃 |  
| Local + web display | Optional OLED shows current values (no internet) 🖤 | Web dashboard with colorful charts and alerts 🚨 |  
| Alert system (configurable) | Trigger notifications via Telegram/email/LED for extremes (e.g., temp >30°C) 🤖 | Alerts appear in a dedicated "Status" section on the dashboard 🚨 |  

---

## **Implementation Roadmap 🚧**  
Follow these steps to build your Pico-Dashboard:  

| Step | Platform | Code Link | Expected Outcome |  
|------|----------|-----------|-------------------|  
| 1. Set up Arduino sensor node | Arduino IDE | [Arduino Code](software/arduino_mega/main.ino) | Arduino reads sensors and sends JSON data via radio 📡 |  
| 2. Configure Pico W radio receiver | MicroPython | [Radio Handler](software/pico_w/radio_handler.py) | Pico W receives, parses, and stores data (temporarily) 💾 |  
| 3. Deploy web server on Pico W | MicroPython | [Main Server](software/pico_w/main.py) | Pico W hosts a web server – access via `GET /data` for JSON 🌐 |  
| 4. Build web dashboard frontend | HTML/CSS/JS | [Frontend Files](frontend/) | Interactive charts and current data displayed in browser 📊 |  

*Pro Tip:* Start with one sensor node, then expand to multiple! 💡  

---

## **Code Highlights & Examples 💻**  

### **Arduino Mega: Sensor Data Transmission (Simplified)**  
```cpp  
#include   
RF24 radio(9, 10);  // CE (9), CSN (10) pins  
const byte address[] = "NODE1";  // Unique ID for this sensor  

void setup() {  
  radio.begin();  
  radio.openWritingPipe(address);  // Set radio address  
  Serial.begin(115200);  
}  

void loop() {  
  float temp = readTemperature();  // Use DHT/BME library functions  
  float hum = readHumidity();  

  // Convert data to JSON (example)  
  String payload = "{\"node\":\"" + String(address) + "\",\"temp\":" + String(temp) + ",\"humidity\":" + String(hum) + "}";  

  // Transmit data  
  radio.write(&payload[0], payload.length());  
  Serial.println("Transmitted: " + payload);  

  delay(1000);  // Update every second  
}  
```  

**Note:** Change `address[]` to unique IDs (e.g., "NODE2", "NODE3") for multiple Arduino nodes! 🔗  

---

### **Pico W: Radio Data Reception & Web Server**  
```python  
# software/pico_w/main.py  
import network  
import ujson  
import socket  
from radio_handler import NRF24Radio  

# Initialize radio module  
radio = NRF24Radio(spi_port=0, ce_pin=15, csn_pin=14)  
radio.set_address(b"NODE1")  # Match Arduino node ID  
radio.start_listening()  

# Set up web server (Access Point)  
wlan = network.WLAN(network.AP_IF)  
wlan.active(True)  
wlan.config(essid="PicoWeather", password="maker2024")  # Customize SSID/password  
wlan.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))  

def get_sensor_data():  
    raw_data = radio.read()  # Receive raw radio data  
    if raw_data:  
        return ujson.loads(raw_data)  # Parse JSON  
    return {"node": "NONE", "temp": 0, "humidity": 0}  # Fallback  

# Run web server  
def serve():  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.bind(('', 80))  
    s.listen(5)  
    print(f"Web server running at {wlan.ifconfig()[0]}")  

    while True:  
        conn, addr = s.accept()  
        request = conn.recv(1024).decode("utf-8")  

        if "/data" in request:  
            data = get_sensor_data()  
            response = ujson.dumps(data)  
            conn.send(f"HTTP/1.1 200 OK\nContent-Type: application/json\n\n{response}")  
        else:  
            conn.send("HTTP/1.1 404 Not Found\n\nDashboard not found. Use /data for live data!")  

        conn.close()  

if __name__ == "__main__":  
    serve()  
```  

---

### **Frontend: Real-Time Charts with Chart.js**  
```html  
  
  
  
  
  Pico-Dashboard 🌡️  
    
  
  
  Weather Station Dashboard  
    
      
      Temperature Trend 🌡️  
        
      
      
      Current Readings  
      Temperature: -- °C  
      Humidity: --%  
      
    
    
    
  
  
```  

```javascript  
// frontend/app.js  
document.addEventListener('DOMContentLoaded', () => {  
  // Initialize temperature chart  
  const tempCtx = document.getElementById('tempChart').getContext('2d');  
  const tempChart = new Chart(tempCtx, {  
    type: 'line',  
    data: { labels: [], datasets: [{ label: 'Temperature (°C)', data: [], borderColor: 'red' }] },  
    options: { responsive: true, scales: { y: { min: 15, max: 35 } } }  
  });  

  // Update data every 2 seconds  
  setInterval(() => {  
    fetch('/data')  
      .then(res => res.json())  
      .then(data => {  
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });  

        // Keep last 30 data points  
        if (tempChart.data.labels.length >= 30) {  
          tempChart.data.labels.shift();  
          tempChart.data.datasets[0].data.shift();  
        }  
        tempChart.data.labels.push(time);  
        tempChart.data.datasets[0].data.push(data.temp);  

        // Update current values  
        document.getElementById('current-temp').textContent = data.temp.toFixed(1);  
        document.getElementById('current-humidity').textContent = data.humidity.toFixed(1);  

        tempChart.update();  
      });  
  }, 2000);  
});  
```  

---

## **Installation & Setup Guide 💡**  
### **Step 1: Assemble Hardware**  
1. **Arduino Mega:**  
   - Connect DHT22/BME280 to analog pin A0.  
   - Attach nRF24L01/HC-12 to SPI pins (MOSI: D11, MISO: D12, SCK: D13).  
   - Power Arduino via USB.  

2. **Raspberry Pi Pico W:**  
   - Connect radio module to SPI pins (MOSI: GP19, MISO: GP16, SCK: GP18).  
   - Set CE pin to GP15, CSN pin to GP14.  
   - Power Pico W via USB or battery pack (recommended for portability).  

### **Step 2: Install Software**  
1. **Arduino Code:**  
   - Download [main.ino](software/arduino_mega/main.ino).  
   - Install `RF24` library via Arduino Library Manager.  
   - Upload code to Arduino.  

2. **Pico W Firmware:**  
   - Flash MicroPython to Pico W (use [Thonny](https://thonny.org/) or `ampy`).  
   - Upload [main.py](software/pico_w/main.py) and [radio_handler.py](software/pico_w/radio_handler.py) via `ampy`.  

### **Step 3: Access the Web Dashboard**  
- Connect to the Pico W Wi-Fi network:  
  - SSID: `PicoWeather` (check `main.py` for customizations).  
  - Password: `maker2024` (update in code if needed).  
- Open a browser and navigate to `http://192.168.4.1` – your dashboard is live! 🚀  

---

## **Troubleshooting 🛠️**  
Common issues & fixes:  

| Problem | Solution |  
|---------|----------|  
| No radio connection | - Verify radio addresses (Arduino and Pico W must match).- Ensure both use the same module (nRF24L01 vs HC-12).- Reduce range (nRF24L01: ~100m, HC-12: ~2km). |  
| Sensor data shows 0 | - Check sensor wiring (loose connections?).- Verify sensor library is installed.- Test sensor separately with Serial Monitor. |  
| Web server not responding | - Confirm Wi-Fi SSID/password (check `main.py`).- Update MicroPython to the latest version.- Use `ampy --port /dev/ttyACM0 put main.py` to re-upload code. |  

---

## **Social Media Preview & Screenshots 📸**  
Get people excited about your project with these visuals!  

| Type | Description | Example Image |  
|------|-------------|---------------|  
| Dashboard Screenshot | Overview of charts and current data | ![Dashboard](docs/screenshots/dashboard.png) |  
| Hardware Assembly | Close-up of Arduino + sensor + radio module | ![Hardware](docs/screenshots/hardware-arduino.jpg) |  
| System Flow Diagram | Sequence: Arduino → Radio → Pico W → Web | ![Flow](docs/screenshots/seq-diagram.png) |  


---

## **Documentation & Further Resources 🔗**  
- **nRF24L01 Datasheet:** [Nordic Semiconductor](https://www.nordicsemi.com/-/media/Software-and-tools/SDKs/nrf24le1/rf24l01_product_sheet_v1_0.pdf)  
- **MicroPython SPI Guide:** [RP2040 SPI Docs](https://docs.micropython.org/en/latest/raspberry_pi_pico_w/library/machine.SPI.html)  
- **Chart.js Tutorial:** [Chart.js Getting Started](https://www.chartjs.org/docs/latest/#getting-started)  
- **Arduino RF24 Wiki:** [RF24 Library Guide](https://github.com/TMRh20/RF24/wiki)  

---

## **Support & Community 💬**  
Got questions? Reach out!  
- Open an issue in this repo.  
- Email: [ricardszuikovs@gmail.com](mailto:ricardszuikovs@gmail.com).  

*Let’s build smarter environments – one sensor at a time!* 🌍  

---  
**MIT License** – Use, modify, and share freely.  
*Built with ❤️ by MBZUAI IFM – Advancing AI for Real-World Impact* 🤖  

---  
