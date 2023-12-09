"""
Perform a traceroute using scapy
and create a graph from it.
"""

from scapy.layers.inet import traceroute

# List of websites to trace
site_list = ["google.com",
             "youtube.com",
             "wikipedia.org"]

# Max number of hops to trace
time_to_live = 30

# This creates the trace using TCP packets
# and outputs the text result to the screen
res, unans = traceroute(site_list, maxttl=time_to_live)

# Alternatively, if TCP doesn't work well, try
# using ICMP packets.
# res, unans = traceroute(site_list, maxttl=time_to_live, l4=ICMP())

# Create a graph in SVG format
res.graph(target="> traceroute_scapy.svg", type="svg")

# Create a graph in PNG format
res.graph(target="> traceroute_scapy.png", type="png")
