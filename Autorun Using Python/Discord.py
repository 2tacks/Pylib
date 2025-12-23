import os
import webbrowser

# Get folder where the script or exe is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to Example.html
html_file = os.path.join(base_dir, "Example.html")

# Open the HTML file
webbrowser.open(f"file:///{html_file}")
