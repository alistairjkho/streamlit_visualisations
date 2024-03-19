"""
Visualisations

Author:
    @alistairjkho : https://github.com/alistairjkho

"""

import streamlit as st

st.set_page_config(
    page_title='Visualisations',
    layout="wide",
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
    st.sidebar.markdown('''<small>[Visualisations v1.25.0](https://google.com)  | Mar 2024 | [Alistair Ho](https://github.com/alistairjkho/)</small>''', unsafe_allow_html=True)


##########################
# Main body 
##########################
    
def st_body():
    col1, col2, col3 = st.columns(3)

# Run main()

if __name__ == '__main__':
    main()