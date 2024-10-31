
# How to Create an Automated Article Publishing Project

This guide will walk you through creating a project that automatically publishes articles using Gemini, GitHub Actions, Python, and Unsplash.

## Prerequisites

- Basic knowledge of Python
- GitHub account
- Unsplash API key

## Steps

### 1. Set Up the Project

1. **Create a new repository on GitHub**:
    - Go to GitHub and create a new repository.
    - Clone the repository to your local machine.

2. **Initialize a Python environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install necessary packages**:
    ```bash
    pip install requests pyyaml
    ```

### 2. Configure Unsplash API

1. **Get an API key**:
    - Sign up on Unsplash and create a new application to get your API key.

2. **Store the API key**:
    - Create a file named `config.yaml` and add your API key:
      ```yaml
      unsplash_api_key: YOUR_UNSPLASH_API_KEY
      ```

### 3. Write the Python Script

1. **Create a script to fetch images and generate articles**:
    - Create a file named `generate_article.py` and add the following code:
      ```python
      import requests
      import yaml

      with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

      def fetch_image():
            url = "https://api.unsplash.com/photos/random"
            headers = {"Authorization": f"Client-ID {config['unsplash_api_key']}"}
            response = requests.get(url, headers=headers)
            return response.json()

      def generate_article():
            image = fetch_image()
            article = f"![{image['description']}]({image['urls']['regular']})\n\n"
            article += f"Photo by [{image['user']['name']}]({image['user']['links']['html']}) on Unsplash"
            with open('article.md', 'w') as file:
                 file.write(article)

      if __name__ == "__main__":
            generate_article()
      ```

### 4. Set Up GitHub Actions

1. **Create a GitHub Actions workflow**:
    - Create a directory `.github/workflows` and a file `main.yml` inside it:
      ```yaml
      name: Generate and Publish Article

      on:
         schedule:
            - cron: '0 0 * * *'  # Runs daily at midnight
         push:
            branches:
              - main

      jobs:
         build:
            runs-on: ubuntu-latest

            steps:
            - name: Checkout repository
              uses: actions/checkout@v2

            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                 python-version: '3.x'

            - name: Install dependencies
              run: |
                 python -m venv venv
                 source venv/bin/activate
                 pip install requests pyyaml

            - name: Run script
              run: |
                 source venv/bin/activate
                 python generate_article.py

            - name: Commit and push changes
              run: |
                 git config --global user.name 'github-actions[bot]'
                 git config --global user.email 'github-actions[bot]@users.noreply.github.com'
                 git add article.md
                 git commit -m 'Automated article update'
                 git push
      ```

### 5. Commit and Push Your Changes

1. **Commit your changes**:
    ```bash
    git add .
    git commit -m "Initial commit"
    git push origin main
    ```

Your project is now set up to automatically generate and publish articles daily using GitHub Actions, Python, and Unsplash.

