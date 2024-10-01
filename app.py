import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px

# Set page config for a light theme
st.set_page_config(
    page_title="Website Analytics",
    page_icon="📊",
    layout="wide",
)

# Custom CSS for professional appearance
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f6;
            color: #333333;
        }
        h1 {
            color: #1f77b4;
            font-weight: 600;
            text-align: center;
            margin-bottom: 20px;
        }
        .stTabs {
            margin-top: 20px;
        }
        .stPlotlyChart {
            padding: 10px;
            border: 1px solid #e6e6e6;
            border-radius: 10px;
            background-color: #ffffff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            margin: 10px 0;
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Adding FMCA Online data to the dataset
def load_data():
    data = {
        'Websites': ['FCCMA', 'FLGISA', 'Florida League of Mayors', 'FBC LEO', 'PSA', 'FMCA Online'],
        'Jan': [5254, 1287, 1945, 1082, 225, 407],
        'Feb': [8257, 1095, 1534, 1077, 318, 518],
        'Mar': [5234, 1084, 1834, 1058, 351, 331],
        'Apr': [6247, 1243, 1932, 1064, 326, 478],
        'May': [4274, 1145, 1864, 1109, 398, 726],
        'Jun': [3258, 1056, 1574, 1165, 328, 405],
        'Jul': [4268, 1254, 1648, 1067, 314, 318],
        'Aug': [3285, 1098, 1648, 1168, 328, 260],
        'Sept': [4175, 1185, 1524, 1085, 274, 151]
    }
    df = pd.DataFrame(data)
    
    # Calculate the total visits for sorting
    df['Total'] = df.iloc[:, 1:].sum(axis=1)
    
    # Sort the dataframe by total visits in descending order
    df = df.sort_values(by='Total', ascending=False)
    
    return df

# Data preparation function
def prepare_data(df):
    data = df.set_index('Websites').drop(columns='Total').transpose()
    sorted_labels = data.columns
    return data, sorted_labels

# Enhanced Line Chart
def create_enhanced_line_chart(data, sorted_labels, title):
    fig = go.Figure()

    for col in sorted_labels:
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data[col], 
            mode='lines+markers', 
            name=col,
            line=dict(width=2.5),  # Increase line width
            marker=dict(size=8),  # Increase marker size
            hoverinfo='x+y+name',  # Enhanced hover text
        ))

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#333333')
        ),
        xaxis=dict(
            title="Month",
            showgrid=True,
            gridcolor='lightgrey',
            tickmode='linear'
        ),
        yaxis=dict(
            title="Visits",
            showgrid=True,
            gridcolor='lightgrey'
        ),
        template="plotly_white",  # Clean, modern theme
        hovermode="x unified",  # Show hover text for all traces
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="Websites",
            font=dict(size=12)
        ),
        autosize=True,
    )
    return fig

# Enhanced Bar Chart
def create_enhanced_bar_chart(data, sorted_labels, title):
    total_visits = data.sum()

    fig = go.Figure(go.Bar(
        x=sorted_labels,
        y=total_visits,
        marker=dict(color='#1f77b4'),  # Custom color
        hoverinfo='x+y',  # Enhanced hover text
    ))

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#333333')
        ),
        xaxis=dict(
            title="Websites",
            showgrid=True,
            gridcolor='lightgrey',
            tickmode='linear'
        ),
        yaxis=dict(
            title="Total Visits",
            showgrid=True,
            gridcolor='lightgrey'
        ),
        template="plotly_white",  # Clean, modern theme
        hovermode="x",  # Show hover text for all bars
        autosize=True,
    )
    return fig

# Enhanced Pie Chart
def create_enhanced_pie_chart(data, sorted_labels, title):
    total_visits = data.sum()

    fig = go.Figure(go.Pie(
        labels=sorted_labels,
        values=total_visits.astype(int),
        hole=.3,  # Donut style
        hoverinfo='label+percent+value',  # Enhanced hover text
        textinfo='label+percent',
        marker=dict(
            colors=px.colors.qualitative.Plotly,
            line=dict(color='#FFFFFF', width=2)
        )
    ))

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#333333')
        ),
        template="plotly_white",  # Clean, modern theme
        showlegend=False,
        autosize=True,
    )
    return fig

# Enhanced Stacked Area Chart
def create_enhanced_stacked_area_chart(data, sorted_labels, title):
    fig = go.Figure()

    for col in sorted_labels:
        fig.add_trace(go.Scatter(
            x=data.index, 
            y=data[col], 
            mode='lines', 
            stackgroup='one',
            name=col,
            line=dict(width=2.5, shape='spline'),  # Smooth lines
            hoverinfo='x+y+name',  # Enhanced hover text
        ))

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#333333')
        ),
        xaxis=dict(
            title="Month",
            showgrid=True,
            gridcolor='lightgrey',
            tickmode='linear'
        ),
        yaxis=dict(
            title="Visits",
            showgrid=True,
            gridcolor='lightgrey'
        ),
        template="plotly_white",  # Clean, modern theme
        hovermode="x unified",  # Show hover text for all traces
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title="Websites",
            font=dict(size=12)
        ),
        autosize=True,
    )
    return fig

# Main application
def main():
    # Load the data
    df = load_data()
    
    # Prepare the data for visualization
    data, sorted_labels = prepare_data(df)

    st.title("Website Analytics Dashboard")

    # Use tabs for better navigation
    tabs = st.tabs(["Monthly Visits Trend", "Total Visits", "Traffic Distribution", "Cumulative Traffic"])

    with tabs[0]:
        st.header("Monthly Visits Trend")
        line_fig = create_enhanced_line_chart(data, sorted_labels, "Monthly Visits Trend")
        st.plotly_chart(line_fig, use_container_width=True)

    with tabs[1]:
        st.header("Total Visits per Website")
        bar_fig = create_enhanced_bar_chart(data, sorted_labels, "Total Visits per Website")
        st.plotly_chart(bar_fig, use_container_width=True)

    with tabs[2]:
        st.header("Traffic Distribution Among Websites")
        pie_fig = create_enhanced_pie_chart(data, sorted_labels, "Traffic Distribution Among Websites")
        st.plotly_chart(pie_fig, use_container_width=True)

    with tabs[3]:
        st.header("Cumulative Traffic Over Time")
        stacked_fig = create_enhanced_stacked_area_chart(data, sorted_labels, "Cumulative Traffic Over Time")
        st.plotly_chart(stacked_fig, use_container_width=True)

if __name__ == "__main__":
    main()
