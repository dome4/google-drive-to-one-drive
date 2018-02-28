import os

# Just to check for the existing of DEMO_MODE environment variable,
# but you could also compare its value, pass it forward and so on
DEMO_MODE = os.environ.get("DEMO_MODE", None)

print (DEMO_MODE)

# on debug branch know
# set folder as variable and ./data/ as default

# use env file instead