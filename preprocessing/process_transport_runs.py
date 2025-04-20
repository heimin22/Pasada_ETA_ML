import json
from pathlib import Path
import pandas as pd

def process_transport_runs():
    # load transport runs data
    data_path = Path(__file__).parent.parent / 'data' / 'transport_runs.json'
    with open(data_path, 'r') as f:
        transport_runs = json.load(f)
        
    # initialize lists to store flattened data
    processed_data = []
    
    # flatten the nested JSON structure
    for run in transport_runs:
        run_number = run['run']
        for stop in run['stops']:
            row ={
                'run_number': run_number,
                'pick_up': stop['pick_up'],
                'drop_off': stop['drop_off'],
                'seating': stop['seating'],
                'standing': stop['standing'],
                'time': stop['time'],
                'lap': stop['lap'],
                'traffic': stop['traffic']
            }
            processed_data.append(row)
            
    # create a dataframe from the processed data
    df = pd.DataFrame(processed_data)
    
    # convert time to minutes since start of day
    df['time_of_day'] = pd.to_datetime(df['time'], format='%I:%M%p').dt.hour * 60 + pd.to_datetime(df['time'], format='%I:%M%p').dt.minute
    
    # convert lap time to minutes
    df['lap_minutes'] = df['lap'].apply(lambda x: int(x.split('h:')[0]) * 60 + int(x.split('h:')[1].split('m:')[0]))
    
    # save processed data 
    output_path = Path(__file__).parent.parent / 'data' / 'processed' / 'processed_transport_runs.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Processed transport runs data saved to {output_path}")
    
    return df
    
if __name__ == "__main__":
    process_transport_runs()
