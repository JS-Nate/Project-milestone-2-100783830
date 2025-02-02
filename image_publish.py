from google.cloud import pubsub_v1  # pip install google-cloud-pubsub
import glob
import base64
import os
import time

# Search for the JSON key file and set credentials
auth_files = glob.glob("*.json")
if not auth_files:
    raise FileNotFoundError("No JSON key file found for authentication.")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_files[0]

# Set project and topic details
project_id = "project1-448716"
topic_name = "images"
dataset_folder = "Dataset_Occluded_Pedestrian"

# Initialize Pub/Sub publisher with message ordering
topic_path = f"projects/{project_id}/topics/{topic_name}"
publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=True)
publisher = pubsub_v1.PublisherClient(publisher_options=publisher_options)

print(f"Publishing images to {topic_path}...")

# Find all images in the dataset folder
image_files = glob.glob(os.path.join(dataset_folder, "*.*"))
if not image_files:
    print("No images found in the dataset folder.")
    exit()

# Publish each image
for image_path in image_files:
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read())
    
    image_name = os.path.basename(image_path)
    try:
        future = publisher.publish(topic_path, image_data, ordering_key=image_name)
        future.result()  # Ensure successful publishing
        print(f"Published: {image_name}")
    except Exception as e:
        print(f"Failed to publish {image_name}: {e}")

print("All images processed.")
