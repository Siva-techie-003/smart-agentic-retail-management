import threading
import webview
from inventory_api import app  # Make sure inventory_api.py is in the same folder

def run_flask():
    app.run(port=5050, debug=False)

if __name__ == "__main__":
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Launch the PyWebView window with the local web interface
    webview.create_window("Retail Inventory Manager", "http://127.0.0.1:5050")
    webview.start()
