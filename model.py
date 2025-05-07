import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_car_recommendations(user_requirements, car_data, api_key=None, top_n=5):
    """
    Use Anthropic's Claude API to recommend cars
    
    Args:
        user_requirements: String of user's requirements
        car_data: DataFrame containing car information
        api_key: Claude API key (optional if set in environment)
        top_n: Number of recommendations to return
        
    Returns:
        DataFrame with top recommendations
    """
    # Get API key from parameters or environment
    if not api_key:
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            print("Claude API key not found")
            return None
    
    # Use standard client
    print("Using direct Claude API connection")
    client = Anthropic(api_key=api_key)
    
    # Sample the car data - Claude can handle much larger token sizes
    car_sample = car_data.sample(min(200, len(car_data))).to_string()
    
    # Create a more specific prompt for the Claude model
    prompt = f"""
    You are an automotive expert assistant. I have a dataset of cars with the following sample:
    {car_sample}
    
    The user has the following requirements:
    {user_requirements}
    
    Based on these requirements, provide the names of {top_n} DIFFERENT car models (not just different years of the same model) 
    that best match these criteria. Consider factors like price, fuel efficiency, body type, and features that align with the user's needs.
    
    IMPORTANT: 
    1. Select DIVERSE models - do not recommend multiple years of the same model
    2. Each recommendation should be a different make/model
    3. For each car, specify both make and model (e.g., "Toyota Camry", "Honda Accord")
    4. Format your response as a comma-separated list (e.g., "Toyota Camry, Honda Accord, Ford Fusion")
    
    Your response should ONLY contain the comma-separated list, with no additional text.
    """
    
    # Add retry logic with exponential backoff for rate limiting
    import time
    import random
    
    max_retries = 5
    base_delay = 1  # Start with a 1-second delay
    
    for retry_count in range(max_retries):
        try:
            # Query the Claude API with a higher token limit
            print(f"Making API request (attempt {retry_count + 1}/{max_retries})")
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # If we get here, the request was successful
            break
            
        except Exception as e:
            # Check if it's a rate limit error (429)
            if "429" in str(e) or "rate limit" in str(e).lower() or "too many requests" in str(e).lower():
                if retry_count < max_retries - 1:  # Don't sleep on the last retry
                    # Calculate exponential backoff with jitter
                    delay = base_delay * (2 ** retry_count) + random.uniform(0, 1)
                    print(f"Rate limit exceeded. Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    print("Maximum retry attempts reached. Giving up.")
                    raise
            else:
                # Not a rate limit error, re-raise
                raise
    
    try:
        # Process the response (this will only execute if the API call succeeded)
        
        # Extract the recommended car names
        response_content = response.content[0].text
        print(f"Claude API response: {response_content}")
        recommended_cars = response_content.split(',')
        recommended_cars = [car.strip() for car in recommended_cars]
        print(f"Extracted car names: {recommended_cars}")
        
        # Find matches in the dataset with improved logic for diversity
        import pandas as pd
        all_matches = []
        unique_models = set()  # Track unique models to ensure diversity
        
        print(f"Looking for matches in dataset with columns: {car_data.columns.tolist()}")
        
        for car_name in recommended_cars:
            print(f"Looking for matches for car: {car_name}")
            
            # Check if the car name contains both make and model (e.g., "Toyota Camry")
            if ' ' in car_name:
                make_part, model_part = car_name.split(' ', 1)
                
                # Try to find cars that match both make and model parts
                if 'make' in car_data.columns and 'model' in car_data.columns:
                    combined_matches = car_data[
                        (car_data['make'].str.contains(make_part, case=False, na=False)) & 
                        (car_data['model'].str.contains(model_part, case=False, na=False))
                    ]
                    
                    if not combined_matches.empty:
                        print(f"Found {len(combined_matches)} combined make/model matches for {car_name}")
                        # Get the best match (newest or most fuel efficient)
                        if 'year' in combined_matches.columns:
                            best_match = combined_matches.sort_values('year', ascending=False).head(1)
                        elif 'combined mpg for fuel type1' in combined_matches.columns:
                            best_match = combined_matches.sort_values('combined mpg for fuel type1', ascending=False).head(1)
                        else:
                            best_match = combined_matches.head(1)
                        
                        # Check if we already have this model
                        model_key = f"{best_match['make'].iloc[0]}-{best_match['model'].iloc[0]}"
                        if model_key not in unique_models:
                            unique_models.add(model_key)
                            all_matches.append(best_match)
                        continue
            
            # Try exact model match
            if 'model' in car_data.columns:
                model_matches = car_data[car_data['model'].str.contains(car_name, case=False, na=False)]
                if not model_matches.empty:
                    print(f"Found {len(model_matches)} model matches for {car_name}")
                    # Get the best match (newest or most fuel efficient)
                    if 'year' in model_matches.columns:
                        best_match = model_matches.sort_values('year', ascending=False).head(1)
                    elif 'combined mpg for fuel type1' in model_matches.columns:
                        best_match = model_matches.sort_values('combined mpg for fuel type1', ascending=False).head(1)
                    else:
                        best_match = model_matches.head(1)
                    
                    # Check if we already have this model
                    model_key = f"{best_match['make'].iloc[0]}-{best_match['model'].iloc[0]}"
                    if model_key not in unique_models:
                        unique_models.add(model_key)
                        all_matches.append(best_match)
                    continue
                else:
                    print(f"No model matches found for {car_name}")
            
            # Try make match
            if 'make' in car_data.columns:
                make_matches = car_data[car_data['make'].str.contains(car_name, case=False, na=False)]
                if not make_matches.empty:
                    print(f"Found {len(make_matches)} make matches for {car_name}")
                    # Group by model and get the best of each model
                    if 'model' in make_matches.columns:
                        # Get the first model we haven't seen yet
                        for model_name in make_matches['model'].unique():
                            model_key = f"{car_name}-{model_name}"
                            if model_key not in unique_models:
                                unique_models.add(model_key)
                                model_group = make_matches[make_matches['model'] == model_name]
                                
                                # Get the best match in this model group
                                if 'year' in model_group.columns:
                                    best_match = model_group.sort_values('year', ascending=False).head(1)
                                elif 'combined mpg for fuel type1' in model_group.columns:
                                    best_match = model_group.sort_values('combined mpg for fuel type1', ascending=False).head(1)
                                else:
                                    best_match = model_group.head(1)
                                
                                all_matches.append(best_match)
                                break
                    else:
                        # No model column, just take the first match
                        best_match = make_matches.head(1)
                        all_matches.append(best_match)
                    continue
                else:
                    print(f"No make matches found for {car_name}")
        
        if all_matches:
            # Combine all matches and ensure we have at most top_n unique models
            result = pd.concat(all_matches).drop_duplicates().head(top_n)
            print(f"Returning {len(result)} diverse recommendations")
            return result
        else:
            print("No matches found, returning top cars as fallback")
            # Fallback: return top cars if no matches found
            if len(car_data) > 0:
                # Sort by price if available, otherwise just take the first few rows
                if 'price' in car_data.columns:
                    fallback_results = car_data.sort_values('price').head(top_n)
                else:
                    fallback_results = car_data.head(top_n)
                return fallback_results
            else:
                return None
            
    except Exception as e:
        print(f"Error with the AI recommendation: {e}")
        # Print more detailed error information to help diagnose issues
        import traceback
        print(f"Detailed error: {traceback.format_exc()}")
        return None