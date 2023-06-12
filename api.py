import requests
import json
import urllib3
import re
from flask import Flask, jsonify

# Disable SSL certificate verification warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/get_stories', methods=['GET'])
def get_stories():
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

            # Return the JSON object
            return jsonify(stories)
        else:
            return jsonify({'message': 'No story matches found in the HTML content.'}), 500
    else:
        return jsonify({'message': 'Failed to retrieve the website content.'}), 500

if __name__ == '__main__':
    app.run()
