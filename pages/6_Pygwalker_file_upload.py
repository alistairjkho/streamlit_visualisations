from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st
from io import StringIO

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Upload data for Pygwalker in Streamlit",
    layout="wide"
)

# Add Title
st.title("Use Pygwalker In Streamlit")

# Function to load the CSV data
def load_data(uploaded_file):
    if uploaded_file is not None:
        # To read file as string:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        string_df = stringio.read()
        # To convert string data to pandas DataFrame:
        df = pd.read_csv(StringIO(string_df))
        return df
    else:
        return None

# Add a title
st.title('CSV Upload Example')

# Add file uploader to allow users to upload CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # The DataFrame will be stored in the session state
    # if it's not already there
    if 'df' not in st.session_state or st.session_state.uploaded_file_name != uploaded_file.name:
        st.session_state.df = load_data(uploaded_file)
        st.session_state.uploaded_file_name = uploaded_file.name

    # Do something with the DataFrame, for example show the first few rows
    st.write(st.session_state.df.head())

    # Use the DataFrame for other components or operations

# Add a button to clear the session state (and thus the uploaded data)
if st.button('Clear uploaded data'):
    if 'df' in st.session_state:
        del st.session_state.df
        st.session_state.uploaded_file_name = ""
    st.info('Uploaded data cleared!')

# Establish communication between pygwalker and streamlit
init_streamlit_comm()

# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = load_data(uploaded_file)
    # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
    return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode=False)
 
if st.button('Click me!'):
    renderer = get_pyg_renderer()
    # Render your data exploration interface. Developers can use it to build charts by drag and drop.
    renderer.render_explore()