from pycirclize import Circos
import numpy as np
import streamlit as st

st.set_page_config(
    page_title='Circlize',
    layout="wide",
    page_icon="🟠",
    initial_sidebar_state="expanded"
)

st.write("Inspiration https://towardsdatascience.com/cant-believe-how-easy-it-is-to-plot-such-a-data-visualisation-in-python-5bcd612e0277")

np.random.seed(0)

# Sectors represent different areas in a city, with the x-axis representing 24 hours of the day
sectors = {"North": 24, "East": 24, "South": 24, "West": 24}
circos = Circos(sectors, space=5)

for sector in circos.sectors:
    # Simulate x (24 hours) and y (number of vehicles)
    x = np.linspace(0, 24, 24)
    y = np.random.randint(10, 1000, 24)  # Simulated hourly vehicle numbers

    # Plot bars for the number of vehicles passed the intersection
    bar_track = sector.add_track((10, 50))
    bar_track.bar(x, y)

    # Plot a line chart showing traffic volume trends throughout the day
    line_track = sector.add_track((60, 100))
    line_track.xticks_by_interval(1)
    line_track.line(x, y)

    # Plot sector name for identification
    sector.text(sector.name, r=110, size=15)

    # Add enclosed axis of the charts in the sectors
    line_track.axis()
    bar_track.axis()

fig = circos.plotfig()

st.pyplot(fig)