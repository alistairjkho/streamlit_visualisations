"""
Visualisations

Author:
    @alistairjkho : https://github.com/alistairjkho

"""

import streamlit as st

st.set_page_config(
    page_title='Visualisations',
    layout="wide",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)

def main():
    st_sidebar()
    st_body()

    return None

def st_sidebar():
    st.sidebar.header('This is the sidebar')

    st.sidebar.markdown('__Instructions__')

    st.sidebar.code('$ pip install streamlit')

    st.sidebar.code('''
    # Import convention
    >>> import streamlit as st
    ''')

    st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)
    st.sidebar.markdown('''<small>[Visualisations v1.0](https://google.com)  | Mar 2024 | [Alistair Ho](https://github.com/alistairjkho/)</small>''', unsafe_allow_html=True)


##########################
# Main body 
##########################
    
def st_body():
    st.write("# Welcome! 👋")

    # col1, col2, col3 = st.columns(3)

    with st.expander("Instructions on how this works", expanded=False):
        st.write("""
            This tool gives an insight on visualisations \n
            Happy plotting! 📈
        """)

    st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )
    
    st.markdown(
        "SHELL IS A PUTPUT, she is biiiiiiiiiiiiig putput 👧"
    )

# Run main()

if __name__ == '__main__':
    main()