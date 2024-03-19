from pyvis import network as net
from IPython.display import display
import streamlit.components.v1 as components
import streamlit as st
import random

st.set_page_config(
    page_title="BLOBS", 
    page_icon="💧",
    layout="centered")

st.title("Blobs blobs blobs, let's add some blobs💧")

# Initiate columns to format display user inputs
cols = st.columns((1, 1))

g=net.Network(cdn_resources='remote',
              bgcolor="white",
              font_color="black",
              height='500px', 
              width='100%',
              notebook=True)

node_number = cols[0].number_input('How many blobs would you like to add?', step=1)

color_list = ['blue', 'green', 'red', 'cyan', 'magenta', 'pink', 'gray', 'teal', 'maroon']
shape_list = ['diamond', 'dot', 'triangle', 'star', 'triangleDown', 'square']

shape_choice = cols[0].radio('Change shape type?', ('Normal', 'Blobs 💧', 'Random Shapes'))

nodes=[]
for node in range(0,node_number):
    node_color = random.choice(color_list)
    shape = random.choice(shape_list)
    if shape_choice == 'Blobs 💧':
        g.add_node(node, color=node_color, label='node '+str(node), shape='image', image='https://static.vecteezy.com/system/resources/thumbnails/009/376/710/small/brownish-green-blob-element-free-png.png')
    if shape_choice == 'Random Shapes':
        g.add_node(node, color=node_color, label='node '+str(node), shape=shape)
    else:
        g.add_node(node, color=node_color, label='node '+str(node))
    
    nodes.append(node)


edge_inputs = {}
for node in nodes:
    # Store each edge location (node) for this current node value to connect to
    edge_inputs[node] = cols[1].multiselect(f'Edges for Blob {node}', nodes, default=[])

for node, edges in edge_inputs.items():
    # For each node, add the edge values to link to nodes
    for edge in edges:
        g.add_edge(node, edge)


g.show("outputs/example.html")

HtmlFile = open("outputs/example.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 500)
