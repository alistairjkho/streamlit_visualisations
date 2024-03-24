import pandas as pd
import streamlit as st
import branca
import folium
import geopandas
import pandas as pd
import requests
import streamlit as st
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium
from io import StringIO

st.write("# GeoJson Popup")
st.write(
    "See [inspiration.](https://github.com/randyzwitch/streamlit-folium/blob/master/examples/pages/geojson_popup.py)"
)

@st.cache_resource
def get_df() -> pd.DataFrame:
    # Retrieve the data via requests package
    response = requests.get(
    "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
    )

    # Convert response to json format, which follows a GeoJSON format
    data = response.json()

    # Convert the GeoJSON features into a GeoDataFrame, crs specifies the Coordinate Reference System (CRS) and the code used to map spatial data
    states = geopandas.GeoDataFrame.from_features(data, crs="EPSG:4326")

    # Get the income data and perform some data-type cleaning
    income = pd.read_csv(
        "https://raw.githubusercontent.com/pri-data/50-states/master/data/income-counties-states-national.csv",
        dtype={"fips": str},
    )
    income["income-2015"] = pd.to_numeric(income["income-2015"], errors="coerce")

    # Reading a mapping file of each state to a 2 letter equivalent
    response = requests.get(
        "https://gist.githubusercontent.com/tvpmb/4734703/raw/"
        "b54d03154c339ed3047c66fefcece4727dfc931a/US%2520State%2520List"
    )

    # Convert the response text (JSON string) into a file-like object
    json_str_io = StringIO(response.text)

    # Read the JSON into a pandas DataFrame
    abbrs = pd.read_json(json_str_io)

    # Merging data
    statesmerge = states.merge(abbrs, how="left", left_on="name", right_on="name")

    # Reducing geometry boundary processing overheads
    statesmerge["geometry"] = statesmerge.geometry.simplify(0.05)

    income.groupby("state")["income-2015"].median().head()

    statesmerge["medianincome"] = statesmerge.merge(
        income.groupby("state")["income-2015"].median(),
        how="left",
        left_on="alpha-2",
        right_on="state",
    )["income-2015"]

    statesmerge["change"] = statesmerge.merge(
        income.groupby("state")["change"].median(),
        how="left",
        left_on="alpha-2",
        right_on="state",
    )["change"]

    return statesmerge

df = get_df()

# Colormap
colormap = branca.colormap.LinearColormap(
    vmin=df["change"].quantile(0.0),
    vmax=df["change"].quantile(1),
    colors=["red", "orange", "lightblue", "green", "darkgreen"],
    caption="State Level Median County Household Income (%)",
)

# Initiates a map centered in the US
m = folium.Map(location=[35.3, -97.6], zoom_start=4)

# Pop-up
popup = GeoJsonPopup(
    fields=["name", "change"],
    aliases=["State", "% Change"],
    localize=True,
    labels=True,
    style="background-color: yellow;",
)

# Tool-tip
tooltip = GeoJsonTooltip(
    fields=["name", "medianincome", "change"],
    aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

folium.GeoJson(
    df,
    style_function=lambda x: {
        "fillColor": colormap(x["properties"]["change"])
        if x["properties"]["change"] is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.4,
    },
    tooltip=tooltip,
    popup=popup,
).add_to(m)

colormap.add_to(m)

# Set whether data should be shown dynamically when hovering
return_on_hover = st.checkbox("Return on hover?", True)

output = st_folium(m, width=700, height=500, return_on_hover=return_on_hover)

left, right = st.columns(2)
with left:
    st.write("## Tooltip")
    st.write(output["last_object_clicked_tooltip"])
with right:
    st.write("## Popup")
    st.write(output["last_object_clicked_popup"])