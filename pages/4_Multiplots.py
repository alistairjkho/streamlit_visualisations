import streamlit as st
import pandas as pd
import numpy as np

# Plotting libraries
import waterfall_chart
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title='Multi-Plots',
    layout="wide",
    page_icon="📅",
    initial_sidebar_state="expanded"
)

st.title("Inspiration [link](https://www.blog.dailydoseofds.com/p/8-classic-alternatives-to-traditional)")

col1, col2, col3 = st.columns(3)


def main():
    generate_seaborn_heatmap()
    generate_waterfall_chart()
    generate_bar_bump_chart()
    generate_raincloud_chart()
    generate_bubble_bar_chart()

    return None

def generate_seaborn_heatmap():
    # Load the brain networks dataset, select subset, and collapse the multi-index
    df = sns.load_dataset("brain_networks", header=[0, 1, 2], index_col=0)

    used_networks = [1, 5, 6, 7, 8, 12, 13, 17]
    used_columns = (df.columns
                    .get_level_values("network")
                    .astype(int)
                    .isin(used_networks))
    df = df.loc[:, used_columns]

    df.columns = df.columns.map("-".join)

    # Compute a correlation matrix and convert to long-form
    corr_mat = df.corr().stack().reset_index(name="correlation")

    # Draw each cell as a scatter point with varying size and color
    g = sns.relplot(
        data=corr_mat,
        x="level_0", y="level_1", hue="correlation", size="correlation",
        palette="vlag", hue_norm=(-1, 1), edgecolor=".7",
        height=10, sizes=(50, 250), size_norm=(-.2, .8),
    )

    # Tweak the figure to finalize
    g.set(xlabel="", ylabel="", aspect="equal")
    g.despine(left=True, bottom=True)
    g.ax.margins(.02)
    for label in g.ax.get_xticklabels():
        label.set_rotation(90)
    
    col1.write('Seaborn Size Encoded Heatmap [link](https://seaborn.pydata.org/examples/heat_scatter.html)')
    col1.pyplot(g, use_container_width=True)

def generate_waterfall_chart():
    a = ['sales','returns','credit fees','rebates','late charges','shipping']
    b = [10,-30,-7.5,-25,95,-7]

    fig = waterfall_chart.plot(a, b)
    col2.write('Waterfall chart [link](https://github.com/chrispaulca/waterfall?tab=readme-ov-file)')
    col2.pyplot(fig)

def generate_bar_bump_chart():
    
    # Creating data
    categories = ['A', 'B', 'C', 'D', 'E']
    time_periods = [2010, 2011, 2012, 2013]

    data = np.array([[1, 1, 2, 1],
                    [1, 1, 2, 5],
                    [5, 3, 2, 3],
                    [2, 4, 2, 4],
                    [4, 1, 5, 5]])
    
    # Calculate rank for each category over time
    ranks = np.argsort(data, axis=0)[::-1]
    rank_data = np.zeros_like(data)
    for i in range(len(time_periods)):
        rank_data[:, i] = ranks[:, i] + 1
        
    # Bar chart
    df = pd.DataFrame(6-rank_data.T, columns=[str(i) for i in categories])
    df["Time"] = time_periods

    fig, ax = plt.subplots()

    df.plot(x='Time', kind='bar', stacked=False, ax=ax)

    ax.set_xlabel('Year', fontsize = 15, fontweight="bold")
    ax.set_ylabel('Rank', fontsize = 15, fontweight="bold")
    ax.set_title('Bar Chart', fontsize = 20, fontweight="bold")
    ax.set_xticklabels(df.Time, rotation = 0)
    ax.set_yticklabels(["",5,4,3,2,1])

    col3.write('Bar Chart [link](https://github.com/ChawlaAvi/Daily-Dose-of-Data-Science/blob/main/Plotting/Bump-chart.ipynb)')
    col3.pyplot(fig)

    # Bump chart
    fig, ax = plt.subplots()
    for i, cat in enumerate(categories):
        ax.plot(time_periods, rank_data[i], label=cat, marker = "o")
        
    ax.invert_yaxis()
    ax.set_xlabel('Year', fontsize = 15, fontweight="bold")
    ax.set_ylabel('Rank', fontsize = 15, fontweight="bold")
    ax.set_title('Bump Chart', fontsize = 20, fontweight="bold")

    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    col3.write('Bump Chart [link](https://github.com/ChawlaAvi/Daily-Dose-of-Data-Science/blob/main/Plotting/Bump-chart.ipynb)')
    col3.pyplot(fig)

def generate_raincloud_chart():
    # Generate random distribution of integers between 0-10 as the first feature
    x1 = np.random.choice([0,1,2,3,4,5,6,7,8,9,10], p=[0.01, 0.01, 0.15, 0.19, 0.05, 0.11, 0.2, 0.16, 0.10, 0.01, 0.01], size=(500))

    # Apply random noise on each sample so they don't overlap on the x-axis in scatter plot
    idxs = np.arange(len(x1))
    out = x1.astype(float)
    out.flat[idxs] += np.random.uniform(low=-1, high=1, size=len(idxs))
    x1 = out

    # Generate random distribution of integers between 6-17 as the second feature
    x2 = np.random.choice([6,7,8,9,10,11,12,13,14,15,16,17], p=[0.01, 0.01, 0.15, 0.23, 0.14, 0.06, 0.05, 0.10, 0.12, 0.11, 0.01, 0.01], size=(500))

    # Apply random noise on each sample so they don't overlap on the y-axis in scatter plot
    idxs = np.arange(len(x2))
    out = x2.astype(float)
    out.flat[idxs] += np.random.uniform(low=-1, high=1, size=len(idxs))
    x2 = out

    # Combine features in a list
    data_x = [x1, x2]

    fig, ax = plt.subplots(figsize=(8, 4))

    # Create a list of colors for the boxplots based on the number of features you have
    boxplots_colors = ['yellowgreen', 'olivedrab']

    # Boxplot data
    bp = ax.boxplot(data_x, patch_artist = True, vert = False)

    # Change to the desired color and add transparency
    for patch, color in zip(bp['boxes'], boxplots_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.4)

    # Create a list of colors for the violin plots based on the number of features you have
    violin_colors = ['thistle', 'orchid']

    # Violinplot data
    vp = ax.violinplot(data_x, points=500, 
                showmeans=False, showextrema=False, showmedians=False, vert=False)

    for idx, b in enumerate(vp['bodies']):
        # Get the center of the plot
        m = np.mean(b.get_paths()[0].vertices[:, 0])
        # Modify it so we only see the upper half of the violin plot
        b.get_paths()[0].vertices[:, 1] = np.clip(b.get_paths()[0].vertices[:, 1], idx+1, idx+2)
        # Change to the desired color
        b.set_color(violin_colors[idx])

    # Create a list of colors for the scatter plots based on the number of features you have
    scatter_colors = ['tomato', 'darksalmon']

    # Scatterplot data
    for idx, features in enumerate(data_x):
        # Add jitter effect so the features do not overlap on the y-axis
        y = np.full(len(features), idx + .8)
        idxs = np.arange(len(y))
        out = y.astype(float)
        out.flat[idxs] += np.random.uniform(low=-.05, high=.05, size=len(idxs))
        y = out
        plt.scatter(features, y, s=.3, c=scatter_colors[idx])

    plt.yticks(np.arange(1,3,1), ['Feature 1', 'Feature 2'])  # Set text labels.
    plt.xlabel('Values')
    plt.title("Raincloud plot")
    plt.show()

    col1.write('Raincloud Chart [Link](https://medium.com/@alexbelengeanu/getting-started-with-raincloud-plots-in-python-2ea5c2d01c11)')
    col1.pyplot(fig)

def generate_bubble_bar_chart():
    df = pd.read_csv("data/bubble_data.csv")
    df = df.sort_values("Country", ascending = False)

    # Bar chart
    fig = px.bar(df, color='Country', y='Exports', x='Year', barmode='group')

    col2.write('Bar Chart')
    col2.plotly_chart(fig)

    # Bubble chart
    fig = px.scatter(df, y='Country', x='Year', color='Exports', size='Exports', size_max=20, color_continuous_scale = px.colors.sequential.RdBu)
    # fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    # fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_layout(height=500, width=600)
    # fig.update_coloraxes(colorbar=dict(title='Exports'))
    # fig.update_traces(marker=dict(sizeref=0.09))
    fig.update_yaxes(title="Country")
    fig.update_xaxes(title='Year')
    # fig.update_layout(showlegend=False)

    col2.write('Bubble Chart [GitHub link](https://github.com/ChawlaAvi/Daily-Dose-of-Data-Science/blob/main/Plotting/Bubble-Charts.ipynb)')
    col2.plotly_chart(fig)

if __name__ == '__main__':
    main()