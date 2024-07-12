import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
import networkx as nx
import pandas as pd
import time

# Define the scopes required for the YouTube Data API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Function to authenticate and create the YouTube service
def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

# Authenticate and create the YouTube service
youtube = get_authenticated_service()

# Function to get channel details
def get_channel_details(channel_id):
    try:
        request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]
        else:
            print(f"No channel details found for channel ID: {channel_id}")
    except googleapiclient.errors.HttpError as e:
        print(f"HttpError occurred while retrieving channel details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# Function to get subscriptions of a channel with pagination
def get_subscriptions(channel_id, max_results=50):
    subscriptions = []
    try:
        request = youtube.subscriptions().list(
            part='snippet,contentDetails',
            channelId=channel_id,
            maxResults=max_results
        )
        while request:
            response = request.execute()
            subscriptions.extend(response.get('items', []))
            request = youtube.subscriptions().list_next(request, response)
    except googleapiclient.errors.HttpError as e:
        print(f"HttpError occurred while retrieving subscriptions: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return subscriptions

# Function to get videos of a channel with pagination
def get_videos(channel_id, max_results=50):
    videos = []
    try:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=max_results,
            type='video'
        )
        while request:
            response = request.execute()
            videos.extend(response['items'])
            request = youtube.search().list_next(request, response)
            if len(videos) >= 2500: 
                break
    except googleapiclient.errors.HttpError as e:
        print(f"HttpError occurred while retrieving videos: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return videos[:2500] 

# Function to get video details including channel title
def get_video_details(video_id):
    try:
        request = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        )
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]
        else:
            print(f"No video details found for video ID: {video_id}")
    except googleapiclient.errors.HttpError as e:
        print(f"HttpError occurred while retrieving video details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# Function to save network periodically
def save_network(G, filename):
    with open(filename, "wb") as f:
        pickle.dump(G, f)
    print(f"Network saved to {filename}")

# Create a directed graph using NetworkX
G = nx.DiGraph()
start_channels = [
    'UCqUp2qAQf0SN6-1qW6rQOYg' 
]
processed_channels = set()
max_channels = 500 
save_interval = 10  


while len(processed_channels) < max_channels and start_channels:
    channel_id = start_channels.pop(0)
    if channel_id in processed_channels:
        continue

    channel_details = get_channel_details(channel_id)
    if channel_details:
        G.add_node(channel_id, type='channel',
                   title=channel_details['snippet']['title'],
                   genre=channel_details['snippet'].get('categoryId', 'Unknown'),
                   views=int(channel_details['statistics'].get('viewCount', 0)),
                   label='channel')
        processed_channels.add(channel_id)

        subscriptions = get_subscriptions(channel_id, max_results=50)
        for subscription in subscriptions:
            subscribed_channel_id = subscription['snippet']['resourceId']['channelId']
            if subscribed_channel_id not in processed_channels:
                start_channels.append(subscribed_channel_id)
                subscribed_channel_details = get_channel_details(subscribed_channel_id)
                if subscribed_channel_details:
                    G.add_node(subscribed_channel_id, type='channel',
                               title=subscribed_channel_details['snippet']['title'],
                               genre=subscribed_channel_details['snippet'].get('categoryId', 'Unknown'),
                               views=int(subscribed_channel_details['statistics'].get('viewCount', 0)),
                               label='channel')
                G.add_edge(channel_id, subscribed_channel_id, type='subscription')

        videos = get_videos(channel_id, max_results=50)
        for video in videos:
            if 'id' in video and 'videoId' in video['id']:  # Check if 'videoId' exists
                video_id = video['id']['videoId']
                video_details = get_video_details(video_id)
                if video_details:
                    view_count = int(video_details['statistics'].get('viewCount', 0))
                    channel_title = video_details['snippet'].get('channelTitle', 'Unknown')
                    G.add_node(video_id, type='video', title=video['snippet']['title'], genre='video', views=view_count, channelname=channel_title, label='video')
                    G.add_edge(channel_id, video_id, type='upload')

    if len(processed_channels) % save_interval == 0:
        save_network(G, "youtube_network.pickle")

# Final save
save_network(G, "youtube_network_final.pickle")

# Save node and edge attributes to CSV files
edges = []
for u, v, data in G.edges(data=True):
    if G.nodes[v]['type'] == 'video':  # Ensure this is a video node
        edge_data = {
            'videoid': v,
            'channelname': G.nodes[u]['title'],
            'channelid': u,
            'videotitle': G.nodes[v]['title'],
            'views': G.nodes[v]['views']
        }
        edges.append(edge_data)
edges_df = pd.DataFrame(edges)
edges_df.to_csv('youtube_edges.csv', index=False)

nodes = []
for node, data in G.nodes(data=True):
    if data['type'] == 'video':  # Ensure this is a video node
        node_data = {
            'videoid': node,
            'genre': data.get('genre', 'Unknown'),
            'views': data.get('views', 0),
            'channelname': data.get('channelname', 'Unknown')  # Using 'channelname' for the channel name
        }
        nodes.append(node_data)
nodes_df = pd.DataFrame(nodes)
nodes_df.to_csv('youtube_nodes.csv', index=False)

print("Data collection and network creation completed successfully.")
