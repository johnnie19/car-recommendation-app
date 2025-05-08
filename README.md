# 🚗 Intelligent Car Recommendation System

A Streamlit-based web application that uses Anthropic's Claude AI to provide personalized car recommendations based on user requirements.

## Overview

This system helps users find their ideal car by combining:
- Natural language processing to understand user preferences
- AI-driven recommendations based on car specifications
- Interactive data visualization of car market insights
- User-friendly interface with customizable filters

## Features

- **AI-Powered Recommendations**: Uses Anthropic's Claude model to analyze user requirements and recommend the most suitable cars
- **Natural Language Input**: Describe what you want in a car using everyday language
- **Advanced Filtering**: Refine recommendations by price range, manufacturer, body type, and more
- **Visual Insights**: Interactive charts showing price distributions, body types, and other market trends
- **Dynamic Car Images**: Automatically fetches relevant car images for recommendations
- **Responsive Design**: Clean, user-friendly interface that works on various devices

## Project Structure

- `app.py`: Main Streamlit application with the user interface
- `model.py`: Integration with Anthropic's Claude API for car recommendations
- `data_processor.py`: Functions for loading, cleaning, and filtering car data
- `visualization.py`: Functions that create interactive Plotly visualizations

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Plotly
- Anthropic Python SDK
- python-dotenv
- Requests

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/car-recommendation-system.git
   cd car-recommendation-system
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your Anthropic API key:
   ```
   CLAUDE_API_KEY=your_anthropic_api_key_here
   ```

## Usage

1. Prepare your car dataset as a CSV file with columns like:
   - make (manufacturer)
   - model
   - year
   - price
   - vehicle size class (body type)
   - combined mpg for fuel type1
   - Other relevant specifications

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. In the app:
   - Set the path to your car data CSV file
   - Enter your Anthropic Claude API key if not set in the .env file
   - Describe your car requirements in natural language
   - Use advanced filters if needed
   - Click "Find My Perfect Car" to get recommendations

## How It Works

1. **Data Processing**: The application loads and cleans the car dataset, handling missing values and standardizing formats.

2. **User Input**: When you describe what you're looking for, your requirements are formatted into a prompt for Claude.

3. **AI Recommendation**: The Claude model processes your requirements against the car dataset and returns recommended car models.

4. **Result Matching**: The system finds the best matches in the dataset based on Claude's recommendations.

5. **Visualization**: The app generates market insights using Plotly to help you understand pricing trends and vehicle distributions.

## Customization

### API Configuration
- The app uses Claude 3 Haiku by default. You can modify the model name in `model.py` to use other Claude models.

### Data Schema
- The system is designed to work with various car datasets, adapting to available columns.
- For best results, ensure your dataset includes at least: make, model, year, price, and body type.

### UI Customization
- Modify the CSS in `app.py` to change the appearance of the application.

## Troubleshooting

### API Rate Limiting
- The system includes retry logic with exponential backoff for handling API rate limits.
- If you still encounter rate limit issues, try reducing the sample size in `model.py`.

### Missing Data
- If your dataset is missing certain columns, some features may be disabled.
- Check the console logs for information about missing columns.

## Future Improvements

- Support for more complex filtering options
- Comparison feature between recommended cars
- User feedback system to improve recommendations
- Integration with real-time car inventory APIs
- Enhanced visualization with more market insights

## License

[MIT License](LICENSE)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Anthropic Claude](https://www.anthropic.com/claude)
