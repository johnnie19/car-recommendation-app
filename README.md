# 🚗 Intelligent Car Recommendation System

A Streamlit-based web application that helps users find their perfect car using natural language requirements and AI-driven recommendations via Anthropic's Claude. Featuring advanced filters, interactive visualizations, and dynamic car images, this project delivers a seamless and responsive user experience.

## 🎯 Overview

This system empowers users to discover their ideal vehicle by combining:

* **Natural Language Understanding**: Users describe their preferences in plain English.
* **AI-Powered Recommendations**: Claude analyzes requirements against a comprehensive car dataset.
* **Customizable Filters**: Refine results by manufacturer, year range, and body type.
* **Interactive Visual Insights**: Explore market trends through charts for fuel efficiency, model distribution, and more.
* **Dynamic Image Fetching**: Automatically retrieves car images from multiple sources with caching.

## 🚀 Features

* **AI-Powered Recommendations**: Uses Anthropic's Claude (default: Claude 3 Haiku) to generate personalized car suggestions.
* **Natural Language Input**: Describe what you want in a car using everyday language.
* **Advanced Filters**: Filter by make, model year range, body type, and other specifications.
* **Interactive Visualizations**: Dive into market insights with Plotly charts (body type distribution, MPG trends, price analysis).
* **Dynamic Car Images**: Fetch and cache relevant car images for each recommendation.
* **Responsive UI**: Designed with Streamlit for a clean, mobile-friendly interface.

## 📁 Project Structure

```
├── app.py                # Main Streamlit application and UI
├── data_processor.py     # Load, clean, and filter car dataset
├── model.py              # Integrate with Anthropic Claude API + retry logic
├── visualization.py      # Plotly chart-generating helper functions
├── requirements.txt      # Python dependencies
```

### `app.py`

* Sets up Streamlit layout and sidebar UI.
* Loads and caches data using `load_data` and `clean_data` from `data_processor.py`.
* Collects user input, applies filters, and triggers recommendation & visualization.

### `data_processor.py`

* **`load_data(file_path)`**: Reads a CSV into pandas DataFrame.
* **`clean_data(df)`**: Standardizes columns, handles missing values and outliers.
* **`filter_data(df, filters)`**: Applies user-specified year, make, and body type filters.

### `model.py`

* **`get_car_recommendations(requirements, df, api_key)`**: Formats an AI prompt, calls Claude API, parses response, and matches recommendations to dataset entries.
* Implements exponential backoff and rate-limit handling.

### `visualization.py`

* **`create_body_type_chart(df)`**: Plotly pie chart of body type distribution.
* **`create_year_chart(df)`**: Bar chart of vehicle counts by year.
* **`create_fuel_efficiency_chart(df)`**: Scatter plot of MPG trends across models.
* **`create_mpg_comparison_chart(df)`**: Box plot comparing MPG across top manufacturers.

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/car-recommendation-system.git
   cd car-recommendation-system
   ```
2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**

   * Copy `.env.example` to `.env`.
   * Set your Anthropic API key:

     ```dotenv
     CLAUDE_API_KEY=your_anthropic_api_key_here
     ```

## 🚴 Usage

1. **Prepare Data**: Ensure you have a CSV file with columns: `make`, `model`, `year`, `vehicle size class` (body type), `combined mpg for fuel type1`, plus any other specs.
2. **Run the App**:

   ```bash
   streamlit run app.py
   ```
3. **Interact**:

   * Specify your car data CSV path and (optionally) API key in the sidebar.
   * Describe your ideal car in the text input.
   * Apply advanced filters if desired.
   * Click **Find My Perfect Car** to view AI-driven recommendations and market insights.

## 🔧 Configuration & Customization

* **Model Selection**: Change the Claude model in `model.py` (e.g., `claude-3-opus`).
* **Data Schema**: Adaptable to various datasets; include `price` column for price-based insights.
* **UI Styling**: Modify colors and layout in `app.py` CSS.

## 🐞 Troubleshooting

* **API Rate Limits**: The system retries with exponential backoff. If issues persist, reduce the number of samples or upgrade your Anthropic plan.
* **Missing Columns**: Features tied to absent columns will be disabled. Check Streamlit logs for warnings.

## 🔮 Future Improvements

* Enhanced comparison view between recommended cars.
* User feedback loop to refine AI suggestions.
* Integration with real-time dealership inventory APIs.
* Expand visualization dashboard with pricing and safety ratings.

## 📄 License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

* Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).
* Powered by [Anthropic Claude](https://www.anthropic.com/claude).
