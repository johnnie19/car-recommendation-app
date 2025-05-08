import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from dotenv import load_dotenv
import plotly.express as px

# Import custom modules
from data_processor import load_data, clean_data, filter_data
from model import get_car_recommendations
from visualization import create_body_type_chart, create_year_chart, create_fuel_efficiency_chart, create_mpg_comparison_chart
import requests
from urllib.parse import quote
import random
import time

# Function to get car image URL from the web
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_car_image_url(make, model, year):
    """
    Get a car image URL based on make, model, and year.
    Uses a combination of reliable car image sources.
    Falls back to a placeholder if no image is found.
    """
    try:
        # Clean and format the search terms
        make = make.strip()
        model = model.strip()
        year = year.strip() if year else ""
        
        # Create search query
        search_query = f"{year} {make} {model}".strip()
        if not search_query:
            return "https://via.placeholder.com/200x150?text=Car+Image"
            
        # List of reliable car image sources
        image_sources = [
            # CarPix API - a simple and reliable source for car images
            f"https://cdn.imagin.studio/getimage?customer=img&make={quote(make)}&modelFamily={quote(model)}&year={year}",
            
            # Fallback to a car stock image site
            f"https://www.carsized.com/resources/honda/{model.lower()}-{year}/h_3_4_1.png",
            
            # Another reliable source
            f"https://www.carpixel.net/w/61d36/{make.lower()}-{model.lower()}-{year}.jpg"
        ]
        
        # Try each source until we find a working image
        for img_url in image_sources:
            try:
                # Check if image exists with a HEAD request
                response = requests.head(img_url, timeout=2)
                if response.status_code == 200:
                    return img_url
            except:
                continue
                
        # If no image is found, use a placeholder with the car name
        return f"https://via.placeholder.com/200x150?text={quote(make)}+{quote(model)}"
        
    except Exception as e:
        print(f"Error fetching car image: {e}")
        # Return a placeholder image if anything goes wrong
        return "https://via.placeholder.com/200x150?text=Car+Image"

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Car Recommendation System",
    page_icon="🚗",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 42px !important;
    }
    .stSubheader {
        color: #34495e;
    }
    .card {
        border-radius: 5px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🚗 Intelligent Car Recommendation System")
st.markdown("""
<div class="card">
    <p>This app helps you find the perfect car based on your specific requirements.
    Simply enter your preferences in natural language, and our AI will analyze our database
    to recommend the best matches for you.</p>
</div>
""", unsafe_allow_html=True)

# Data file path configuration
default_data_path = r"C:\Users\binsu\Downloads\car_data.csv"

# Add data file configuration in sidebar
with st.sidebar:
    st.subheader("Data Configuration")
    data_file_path = st.text_input("Data File Path:", value=default_data_path)
    
    # Button to reload data
    reload_data = st.button("Load Data")

@st.cache_data(show_spinner=True, ttl=None)
def cached_load_data(file_path):
    df = load_data(file_path)
    if df is not None:
        df = clean_data(df)
    return df

# Initialize session state for data loading
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None

# Load data when button is clicked or on initial load
if reload_data or not st.session_state.data_loaded:
    try:
        st.session_state.df = cached_load_data(data_file_path)
        st.session_state.data_loaded = st.session_state.df is not None
        if st.session_state.data_loaded:
            st.sidebar.success(f"Data loaded successfully from: {data_file_path}")
        else:
            st.sidebar.error(f"Failed to load data from: {data_file_path}")
    except Exception as e:
        st.sidebar.error(f"Error loading dataset: {e}")
        st.session_state.data_loaded = False

# Use the loaded dataframe
df = st.session_state.df
data_loaded = st.session_state.data_loaded

# Check if critical columns are present
required_columns = ['make', 'model', 'year', 'vehicle size class', 'combined mpg for fuel type1']

if data_loaded and df is not None:
    missing_important_columns = [col for col in required_columns if col not in df.columns]

    if missing_important_columns:
        with st.sidebar:
            st.error(f"Dataset is missing critical columns: {', '.join(missing_important_columns)}")
            st.stop()

# Set up Claude API
if 'claude_api_key' not in st.session_state:
    st.session_state.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
    st.session_state.claude_key_set = bool(st.session_state.claude_api_key)

with st.sidebar:
    st.subheader("API Configuration")
    
    # Claude API configuration
    if not st.session_state.claude_key_set:
        api_key = st.text_input("Enter your Anthropic Claude API key:", type="password")
        if st.button("Set Claude API Key"):
            if api_key:
                os.environ["CLAUDE_API_KEY"] = api_key
                st.session_state.claude_api_key = api_key
                st.session_state.claude_key_set = True
                st.success("Claude API key set successfully!")
            else:
                st.error("Please enter a valid API key")

if data_loaded and st.session_state.claude_key_set:
    # Create two columns for the layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Your Requirements")

        # User input section
        user_requirements = st.text_area(
            "Describe what you're looking for in a car:",
            placeholder="Example: I need a fuel-efficient SUV with good safety ratings for a family of 4.",
            height=150
        )

        # Advanced filters
        with st.expander("Advanced Filters"):
            # Year range slider
            min_year = 2000
            max_year = 2023
            if 'year' in df.columns:
                min_year = int(df['year'].min())
                max_year = int(df['year'].max())
                
            year_range = st.slider("Year Range", 
                                min_value=min_year, 
                                max_value=max_year,
                                value=(min_year, max_year))

            makes = []
            if 'make' in df.columns:
                makes = st.multiselect("Manufacturers", options=sorted(df['make'].unique()))

            body_types = []
            if 'vehicle size class' in df.columns:
                body_types = st.multiselect("Body Types", options=sorted(df['vehicle size class'].unique()))

        # Search button
        search_button = st.button("Find My Perfect Car", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if search_button and user_requirements:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Recommended Cars")

            # Create a progress message that can be updated
            progress_message = st.empty()
            progress_message.info("Our AI is finding the best matches for you...")
            
            try:
                # Apply filters to dataset
                filters = {
                    'year_range': year_range,
                    'makes': makes,
                    'body_types': body_types
                }
                filtered_df = filter_data(df, filters)
                
                # Get recommendations
                # Get the API key from session state
                current_api_key = st.session_state.claude_api_key
                recommendations = get_car_recommendations(user_requirements, filtered_df, api_key=current_api_key)

                # Clear the progress message
                progress_message.empty()
                
                if recommendations is not None and not recommendations.empty:
                    # Display recommendations
                    for i, (_, car) in enumerate(recommendations.iterrows()):
                        with st.container():
                            cols = st.columns([1, 2])
                            # First, get the car information
                            make_col = 'make' if 'make' in car else ''
                            model_col = 'model' if 'model' in car else ''
                            
                            # Get car details for image
                            make = car[make_col] if make_col else ""
                            model = car[model_col] if model_col else ""
                            year = str(car['year']) if 'year' in car else ""
                            
                            # Display image in first column
                            with cols[0]:
                                # Construct image URL for the car
                                img_url = get_car_image_url(make, model, year)
                                st.image(img_url, width=200)
                            
                            # Display information in second column
                            with cols[1]:

                                if make_col and model_col:
                                    st.subheader(f"{car[make_col]} {car[model_col]}")
                                elif make_col:
                                    st.subheader(f"{car[make_col]}")
                                elif model_col:
                                    st.subheader(f"{car[model_col]}")
                                else:
                                    st.subheader(f"Car #{i+1}")

                                # Display key specifications based on available columns
                                specs = []
                                if 'year' in car:
                                    specs.append(f"Year: {car['year']}")
                                if 'combined mpg for fuel type1' in car:
                                    specs.append(f"MPG: {car['combined mpg for fuel type1']}")
                                if 'fuel type' in car:
                                    specs.append(f"Fuel: {car['fuel type']}")
                                if 'transmission' in car:
                                    specs.append(f"Transmission: {car['transmission']}")

                                st.write(" | ".join(specs))

                            st.markdown("<hr>", unsafe_allow_html=True)
                else:
                    st.warning("No cars matching your criteria were found. Try adjusting your requirements or filters.")
                    
            except Exception as e:
                # Handle any errors that occur during recommendation
                progress_message.error(f"An error occurred: {str(e)}")
                if "429" in str(e) or "rate limit" in str(e).lower():
                    st.error("Rate limit exceeded. Please try again in a few moments.")
                else:
                    st.error("There was a problem getting recommendations. Please try again.")
                import traceback
                print(f"Error details: {traceback.format_exc()}")

            st.markdown('</div>', unsafe_allow_html=True)

            # Add visualization section
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Market Insights")

            # Choose visualization based on available columns
            viz_tab1, viz_tab2, viz_tab3 = st.tabs(["Fuel Efficiency Trends", "MPG by Manufacturer", "Body Types"])

            with viz_tab1:
                mpg_chart = create_fuel_efficiency_chart(df)
                if mpg_chart:
                    st.plotly_chart(mpg_chart, use_container_width=True)
                else:
                    st.info("Fuel efficiency chart is not available with current data.")
                    
            with viz_tab2:
                mpg_comparison = create_mpg_comparison_chart(df)
                if mpg_comparison:
                    st.plotly_chart(mpg_comparison, use_container_width=True)
                else:
                    st.info("MPG comparison chart is not available with current data.")

            with viz_tab3:
                body_chart = create_body_type_chart(df)
                if body_chart:
                    st.plotly_chart(body_chart, use_container_width=True)
                else:
                    st.info("Body type distribution chart is not available with current data.")

            st.markdown('</div>', unsafe_allow_html=True)

    # Dataset insights in the sidebar
    with st.sidebar:
        st.subheader("Dataset Insights")
        if data_loaded and df is not None:
            st.write(f"Total cars in database: {len(df)}")

            if 'make' in df.columns:
                st.write(f"Number of manufacturers: {df['make'].nunique()}")

            if 'vehicle size class' in df.columns:
                top_body_types = df['vehicle size class'].value_counts().head(5)
                st.write("Top 5 body types:")
                st.write(top_body_types)

            # Add a small visualization
            if 'year' in df.columns:
                st.subheader("Cars by Year")
                year_counts = df['year'].value_counts().sort_index()
                st.bar_chart(year_counts)
else:
    if not data_loaded:
        st.warning("Please make sure your dataset is loaded correctly.")

    if not st.session_state.claude_key_set:
        st.info("Please set your Claude API key in the sidebar to use the recommendation feature.")

# Add footer
st.markdown("""
<div style="text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 12px;">
    <p>Car Recommendation System | Created with Streamlit and Anthropic Claude</p>
</div>
""", unsafe_allow_html=True)
