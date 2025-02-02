from google.cloud import pubsub_v1  # Install using: pip install google-cloud-pubsub
import glob
import json
import os
import csv

# Locate the JSON service account key dynamically
json_keys = glob.glob("*.json")
if not json_keys:
    print("Error: No service account JSON file found.")
    exit()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = json_keys[0]

# Define Google Cloud project and Pub/Sub topic
PROJECT_ID = "project1-448716"
TOPIC = "records"

# Initialize Pub/Sub client and construct topic path
pub_client = pubsub_v1.PublisherClient()
topic_full_path = pub_client.topic_path(PROJECT_ID, TOPIC)
print(f"Publishing to topic: {topic_full_path}")

# CSV file containing data
CSV_FILE = "Labels.csv"

def parse_value(val):
    """Attempts to convert a string to int or float where applicable."""
    try:
        return float(val) if '.' in val else int(val)
    except ValueError:
        return val  # Return as string if conversion fails

with open(CSV_FILE, newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    for record in csv_reader:
        # Convert row values appropriately
        formatted_record = {key: parse_value(val) for key, val in record.items()}
        
        # Serialize and publish message
        json_msg = json.dumps(formatted_record).encode('utf-8')
        print("Publishing:", json_msg)
        
        future = pub_client.publish(topic_full_path, json_msg)
        future.result()  # Ensure successful publishing

print("All records successfully published.")
