### Step-by-Step Guide to Run the Wi-Fi Dashboard

1. **Install Python**:
   - Ensure Python 3.8 or higher is installed on your system. Download it from [python.org](https://www.python.org/downloads/) if needed.
   - Verify installation by running `python --version` or `python3 --version` in your terminal/command prompt.

2. **Install Required Libraries**:
   - Install the required Python packages by running the following command in your terminal or command prompt:
     ```bash
     pip install flask speedtest-cli
     ```
   - This installs `Flask` for the web server and `speedtest-cli` for performing speed tests.

3. **Save the Code**:
   - Copy the provided Python code (`wifi_dashboard.py`) into a new file named `wifi_dashboard.py` on your computer.
   - You can use any text editor (e.g., VS Code, Notepad, or PyCharm) to create and save the file.

4. **Run the Application**:
   - Open a terminal or command prompt and navigate to the directory containing `wifi_dashboard.py`. For example:
     ```bash
     cd path/to/your/directory
     ```
   - Run the script using:
     ```bash
     python wifi_dashboard.py
     ```
   - If your system requires `python3`, use:
     ```bash
     python3 wifi_dashboard.py
     ```

5. **Access the Dashboard**:
   - Open a web browser and go to `http://localhost:5000` or `http://127.0.0.1:5000`.
   - The dashboard will display:
     - **IP Information**: Your device's hostname and local IP address.
     - **Wi-Fi Information**: Details about your Wi-Fi connection (e.g., SSID, signal strength, depending on your OS).
     - **Speed Test**: Download speed, upload speed, ping, server, and timestamp, updated every 5 minutes.

6. **Platform-Specific Notes**:
   - **Windows**: The script uses `netsh` to fetch Wi-Fi details. Ensure you're connected to a Wi-Fi network.
   - **Linux**: The script uses `iwconfig` and `iwgetid`. Ensure these tools are installed (usually available in `wireless-tools` package). Install them on Debian/Ubuntu with:
     ```bash
     sudo apt-get install wireless-tools
     ```
   - **macOS**: The script uses the `airport` command. Ensure you have the necessary permissions to run it.

7. **Troubleshooting**:
   - If the speed test fails, ensure you have an active internet connection.
   - If Wi-Fi info is missing, check if your system supports the commands used or if you're connected to a Wi-Fi network.
   - For permission errors on Linux/macOS, try running the script with `sudo` (e.g., `sudo python3 wifi_dashboard.py`).
   - If the server doesn't start, ensure port 5000 is not in use by another application.

8. **Stopping the Server**:
   - To stop the server, press `Ctrl+C` in the terminal where the script is running.

This dashboard provides a clean, user-friendly interface to monitor your Wi-Fi network's performance and details. The speed test runs automatically every 5 minutes, and the page updates in real-time via JavaScript. If you encounter issues or need further customization, let me know!
