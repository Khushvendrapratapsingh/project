import requests
import json
import urllib3
import re


# Disable SSL certificate verification warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Send an HTTP GET request to times.com
response = requests.get('https://times.com', verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Extract the HTML content
    html_content = response.text

    # Define the pattern to match the story elements
    pattern_story = r'<h2.*?>(.*?)<\/h2>.*?<a.*?href="(.*?)".*?>'

    # Find all the story matches within the HTML content
    matches_story = re.findall(pattern_story, html_content, re.DOTALL)

    if matches_story:
        # Process the story matches to extract the title and link
        stories = []
        for match in matches_story:
            title = match[0].strip()
            link = match[1]
            story = {'title': title, 'link': link}
            stories.append(story)

        # Save the data to a JSON file
        with open('stories.json', 'w') as file:
            json.dump(stories, file, indent=4)

        print("Data saved to stories.json file.")
    else:
        print("Error: No story matches found in the HTML content.")
else:
    print("Error: Failed to retrieve the website content.")
