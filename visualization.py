import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def create_price_comparison_chart(df):
    """Create a box plot showing price distribution by manufacturer"""
    if df is None or 'make' not in df.columns or 'price' not in df.columns:
        return None
    
    # Get top 10 manufacturers by count
    top_makes = df['make'].value_counts().head(10).index.tolist()
    plot_df = df[df['make'].isin(top_makes)]
    
    fig = px.box(plot_df, x='make', y='price', 
                 title='Price Distribution by Top Manufacturers',
                 labels={'make': 'Manufacturer', 'price': 'Price ($)'},
                 color='make')
    
    return fig

def create_body_type_chart(df):
    """Create a pie chart showing distribution of car body types"""
    if df is None or 'vehicle size class' not in df.columns:
        return None
    
    body_counts = df['vehicle size class'].value_counts()
    fig = px.pie(values=body_counts.values, 
                 names=body_counts.index, 
                 title='Distribution of Car Body Types')
    
    return fig

def create_year_chart(df):
    """Create a bar chart showing cars by year"""
    if df is None or 'year' not in df.columns:
        return None
    
    year_counts = df['year'].value_counts().sort_index()
    fig = px.bar(x=year_counts.index, y=year_counts.values,
                labels={'x': 'Year', 'y': 'Number of Cars'},
                title='Cars by Year')
    
    return fig

def create_fuel_efficiency_chart(df):
    """Create a scatter plot of fuel efficiency"""
    if df is None or 'combined mpg for fuel type1' not in df.columns:
        return None
    
    fig = px.scatter(df, x='year', y='combined mpg for fuel type1',
                    color='make', opacity=0.7,
                    labels={'year': 'Year', 'combined mpg for fuel type1': 'Combined MPG'},
                    title='Fuel Efficiency Trends Over Time')
    
    return fig