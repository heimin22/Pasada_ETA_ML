import joblib
from pathlib import Path
import json
import requests
import pandas as pd
from datetime import datetime

def format_eta(minutes):
    # round to nearest minute
    total_minutes = round(minutes)

    # handle edge case for 0 minutes
    if total_minutes <= 0:
        return "0 mins"

    # if less than 60 minutes, return in minutes
    if total_minutes < 60:
        return f"{total_minutes} mins"

    # calculate hours and remaining minutes
    hours = total_minutes // 60
    remaining_minutes = total_minutes % 60

    # format the output string
    hour_str = f"{hours} hr" if hours == 1 else f"{hours} hrs"
    minute_str = f"{remaining_minutes} mins" if remaining_minutes > 0 else ""

    # combine parts, handling cases where minutes might be 0
    if minute_str:
        return f"{hour_str} {minute_str}"
    else:
        return hour_str


def load_transport_runs():
    # load and cache the processed transport data
    data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_transport_runs.csv'
    if data_path.exists():
        return pd.read_csv(data_path)
    return None

def get_historical_stats(df, pick_up, drop_off, time_str):
    # calculate historical stats for a given route and time
    try:
        # convert input time to minutes
        time = datetime.strptime(time_str, '%I:%M%p')
        time_minutes = time.hour * 60 + time.minute
        
        # filter relevant routes
        routes_data = df[(df['pick_up'] == pick_up) & (df['drop_off'] == drop_off)]
        
        if routes_data.empty:
            return None
        
        # calculate statistics
        stats = {
            'avg_travel_time': routes_data['lap_minutes'].mean(),
            'min_travel_time': routes_data['lap_minutes'].min(),
            'max_travel_time': routes_data['lap_minutes'].max(),
            'common_traffic': routes_data['traffic'].mode().iloc[0]
        }

        return stats
    except Exception as e:
        return None
    

def gemini_eta_predict(user_input, api_key):    
    uri = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    # get ETA prediction
    try:
        # load the ETA model
        model_path = Path(__file__).parent.parent / 'models' / 'eta_model.pkl'
        model = joblib.load(model_path)
        
        # parse input features
        features = json.loads(user_input)
        
        # load historical transport data
        transport_data = load_transport_runs()
        
        # get historical stats
        stats = None
        if transport_data is not None:
            stats = get_historical_stats(
                transport_data,
                features.get('pick_up'),
                features.get('drop_off'),
                features.get('time')
            )
            
        
        eta_prediction = float(model.predict([features])[0])
        formatted_eta = format_eta(eta_prediction)
        
        # Generate context for Gemini prompt
        context = f"""
        Route Analysis:
        From: {features.get('pick_up', 'Unknown')}
        To: {features.get('drop_off', 'Unknown')}
        Time: {features.get('time', 'Unknown')}
        Traffic: {features.get('traffic', 'Unknown')}
        Estimated Travel Time: {formatted_eta}
        """
        
        if stats:
            context += f"\nHistorical Average Travel Time: {stats['avg_travel_time']}"
        
        data = {
            "contents": [{
                "parts": [{"text": context}]
            }]
        }
        
        response = requests.post(uri, headers=headers, json=data)
        response.raise_for_status()
        
        return {
            "eta_prediction": eta_prediction,
            "formatted_eta": formatted_eta,
            "historical_stats": stats,
            "gemini_response": response.json()["candidates"][0]["content"]["parts"][0]["text"]
        }
    except Exception as e:
        return {
            "eta_prediction": None,
            "formatted_eta": None,
            "historical_stats": None,
            "gemini_response": f"An error occurred: {str(e)}"
        }
        
if __name__ == "__main__":
    # Example usage
    test_input = {
        "pick_up": "Villanova",
        "drop_off": "Tourist",
        "time": "5:05AM",
        "traffic": "Light"
    }
    
    # Test ETA formatting
    print("ETA Format Examples:")
    print(format_eta(45))  # Should output: "45 mins"
    print(format_eta(90))  # Should output: "1 hr 30 mins"
    
    # Load API key from environment variable
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_ML")
    
    if api_key:
        result = gemini_eta_predict(json.dumps(test_input), api_key)
        print("\nPrediction Results:")
        print(json.dumps(result, indent=2))
    else:
        print("Error: GEMINI_API_ML environment variable not set")
    
