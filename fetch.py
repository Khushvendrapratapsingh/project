import requests
import re
import urllib3
import json

# Disable SSL certificate verification warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Send an HTTP GET request to times.com
response = requests.get('https://times.com', verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Extract the HTML content
    html_content = response.text

    # Define the pattern to match the story titles and links
    pattern_section = r'<section class="homepage-section-v2 voices-ls">.*?</section>'

    # Find the "latest stories" section using the pattern
    matches_section = re.findall(pattern_section, html_content, re.DOTALL)

    if matches_section:
        section_content = matches_section[0]

        # Define the pattern to match the story elements within the section
        pattern_story = r'<div class="partial lastest-stories">.*?<h2 class="lastest-stories__heading">(.*?)</h2>.*?<a href="(.*?)">.*?</a>.*?</div>'

        # Find all the story matches within the section content
        matches_story = re.findall(pattern_story, section_content, re.DOTALL)

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
        print("Error: Failed to find the 'latest stories' section in the HTML content.")
else:
    print("Error: Failed to retrieve the website content.")
