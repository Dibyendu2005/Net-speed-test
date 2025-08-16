import tkinter as tk
from tkinter import ttk
import speedtest
import threading
import time
import socket

def reset_labels():
    download_label.config(text="Download: -- Mbps")
    upload_label.config(text="Upload: -- Mbps")
    ping_label.config(text="Latency (Ping): -- ms")
    jitter_label.config(text="Jitter: -- ms")
    server_label.config(text="Server: Unknown")
    result_label.config(text="")
    timer_label.config(text="Time Remaining: -- sec")

def run_speed_test():
    reset_labels()
    result_label.config(text="Testing...")
    start_button.config(state=tk.DISABLED)
    countdown(30)

    try:
        st = speedtest.Speedtest()
        best_server = st.get_best_server()
        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000      # Mbps
        ping_result = st.results.ping

        # Approximate Jitter
        jitters = []
        for _ in range(5):
            start = time.time()
            try:
                socket.gethostbyname('google.com')
            except:
                pass
            jitters.append((time.time() - start) * 1000)
        jitter_value = round(max(jitters) - min(jitters), 2)

        # Internet Speed Quality Evaluation
        avg_speed = (download_speed + upload_speed) / 2
        if avg_speed >= 25:
            quality = "Your Internet connection is VERY FAST"
        elif avg_speed >= 20:
            quality = "Your Internet connection is FAST"
        elif avg_speed >= 15:
            quality = "Your Internet connection is MEDIUM"
        elif avg_speed >= 10:
            quality = "Your Internet connection is SLOW"
        else:
            quality = "Your Internet connection is VERY SLOW"

        # Show Results
        download_label.config(text=f"Download: {download_speed:.2f} Mbps")
        upload_label.config(text=f"Upload: {upload_speed:.2f} Mbps")
        ping_label.config(text=f"Latency (Ping): {ping_result:.0f} ms")
        jitter_label.config(text=f"Jitter: {jitter_value} ms")
        server_label.config(text=f"Server: {best_server.get('sponsor', 'Unknown')} ({best_server.get('name', 'Unknown')})")
        result_label.config(text=quality)

    except Exception as e:
        result_label.config(text="Speed test failed. Check connection.")
    finally:
        start_button.config(state=tk.NORMAL)

def start_test():
    thread = threading.Thread(target=run_speed_test)
    thread.start()

def countdown(time_left):
    if time_left > 0:
        timer_label.config(text=f"Time Remaining: {time_left} sec")
        root.after(1000, countdown, time_left - 1)
    else:
        timer_label.config(text="Test Finished")

# GUI setup
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("430x400")
root.resizable(False, False)

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="Speed Test", font=("Helvetica", 18)).pack(pady=10)

timer_label = ttk.Label(frame, text="Time Remaining: -- sec", font=("Helvetica", 12))
timer_label.pack()

download_label = ttk.Label(frame, text="Download: -- Mbps", font=("Helvetica", 12))
download_label.pack()

upload_label = ttk.Label(frame, text="Upload: -- Mbps", font=("Helvetica", 12))
upload_label.pack()

ping_label = ttk.Label(frame, text="Latency (Ping): -- ms", font=("Helvetica", 12))
ping_label.pack()

jitter_label = ttk.Label(frame, text="Jitter: -- ms", font=("Helvetica", 12))
jitter_label.pack()

server_label = ttk.Label(frame, text="Server: Unknown", font=("Helvetica", 12))
server_label.pack()

result_label = ttk.Label(frame, text="", font=("Helvetica", 12), foreground="blue")
result_label.pack(pady=10)

start_button = ttk.Button(frame, text="Start Speed Test", command=start_test)
start_button.pack(pady=10)

root.mainloop()
