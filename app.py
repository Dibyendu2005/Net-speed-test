from flask import Flask, render_template, jsonify
import speedtest
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run_test")
def run_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Mbps
    upload_speed = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping

    result = {
        "download": download_speed,
        "upload": upload_speed,
        "ping": ping,
        "server": st.get_best_server()['host'],
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
