from flask import Flask, render_template_string, jsonify
import speedtest
import socket
import subprocess
import platform
import threading
import time

app = Flask(__name__)
latest_results = {}

def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        return {
            "download": round(st.results.download / 1_000_000, 2),  # Convert to Mbps
            "upload": round(st.results.upload / 1_000_000, 2),    # Convert to Mbps
            "ping": round(st.results.ping, 2),
            "server": st.results.server.get("sponsor", "Unknown"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e), "download": 0, "upload": 0, "ping": 0, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}

def get_ip_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return {"hostname": hostname, "ip": ip}
    except Exception as e:
        return {"hostname": "Unknown", "ip": "Unknown", "error": str(e)}

def get_wifi_info():
    system = platform.system()
    info = {}
    try:
        if system == "Windows":
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"], text=True)
            for line in result.splitlines():
                if ":" in line:
                    key, val = line.strip().split(":", 1)
                    info[key.strip()] = val.strip()
        elif system == "Linux":
            result = subprocess.check_output("iwconfig 2>/dev/null", shell=True, text=True)
            for line in result.splitlines():
                if ":" in line:
                    key, val = line.strip().split(":", 1)
                    info[key.strip()] = val.strip()
            # Additional Linux-specific info
            try:
                ssid = subprocess.check_output("iwgetid -r", shell=True, text=True).strip()
                info["SSID"] = ssid
            except:
                info["SSID"] = "Unknown"
        elif system == "Darwin":
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                text=True
            )
            for line in result.splitlines():
                if ":" in line:
                    key, val = line.strip().split(":", 1)
                    info[key.strip()] = val.strip()
    except Exception as e:
        info["error"] = str(e)
    return info

def run_speed_test():
    global latest_results
    while True:
        latest_results = get_speed()
        time.sleep(300)  # Run speed test every 5 minutes

@app.route("/")
def index():
    ip_info = get_ip_info()
    wifi_info = get_wifi_info()

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wi-Fi Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background-color: #f3f4f6; }
        </style>
    </head>
    <body class="min-h-screen flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-2xl">
            <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">📶 Wi-Fi Dashboard</h1>

            <!-- IP Info -->
            <div class="mb-6">
                <h2 class="text-xl font-semibold text-gray-700">IP Information</h2>
                <div class="mt-2 p-4 bg-gray-100 rounded-lg">
                    <p><strong>Hostname:</strong> {{ ip['hostname'] }}</p>
                    <p><strong>Local IP:</strong> {{ ip['ip'] }}</p>
                    {% if ip.get('error') %}
                        <p class="text-red-600"><strong>Error:</strong> {{ ip['error'] }}</p>
                    {% endif %}
                </div>
            </div>

            <!-- Wi-Fi Info -->
            <div class="mb-6">
                <h2 class="text-xl font-semibold text-gray-700">Wi-Fi Information</h2>
                <div class="mt-2 p-4 bg-gray-100 rounded-lg">
                    {% for key, value in wifi.items() %}
                        {% if key != 'error' %}
                            <p><strong>{{ key }}:</strong> {{ value }}</p>
                        {% endif %}
                    {% endfor %}
                    {% if wifi.get('error') %}
                        <p class="text-red-600"><strong>Error:</strong> {{ wifi['error'] }}</p>
                    {% endif %}
                </div>
            </div>

            <!-- Speed Test -->
            <div>
                <h2 class="text-xl font-semibold text-gray-700">Speed Test</h2>
                <div class="mt-2 p-4 bg-gray-100 rounded-lg">
                    <p><strong>Download:</strong> <span id="download">Loading...</span> Mbps</p>
                    <p><strong>Upload:</strong> <span id="upload">Loading...</span> Mbps</p>
                    <p><strong>Ping:</strong> <span id="ping">Loading...</span> ms</p>
                    <p><strong>Server:</strong> <span id="server">Loading...</span></p>
                    <p><strong>Last Updated:</strong> <span id="timestamp">Loading...</span></p>
                    {% if latest_results.get('error') %}
                        <p class="text-red-600"><strong>Error:</strong> {{ latest_results['error'] }}</p>
                    {% endif %}
                </div>
            </div>

            <script>
                async function updateSpeed() {
                    try {
                        const response = await fetch('/api/speed');
                        const data = await response.json();
                        document.getElementById('download').textContent = data.download;
                        document.getElementById('upload').textContent = data.upload;
                        document.getElementById('ping').textContent = data.ping;
                        document.getElementById('server').textContent = data.server;
                        document.getElementById('timestamp').textContent = data.timestamp;
                    } catch (error) {
                        console.error('Error fetching speed:', error);
                    }
                }

                // Initial fetch
                updateSpeed();

                // Auto-refresh speed test every 5 minutes
                setInterval(updateSpeed, 300000);
            </script>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, ip=ip_info, wifi=wifi_info, latest_results=latest_results)

@app.route("/api/speed")
def api_speed():
    global latest_results
    return jsonify(latest_results)

if __name__ == "__main__":
    # Start speed test in background thread
    threading.Thread(target=run_speed_test, daemon=True).start()
    app.run(host="0.0.0.0", port=5000, debug=True)
