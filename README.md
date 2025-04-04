🚀 Auto-WordPress Generator with Gemini 🤖
This project contains a Python script that runs automatically every 3 hours to upload articles to a WordPress website. The script uses Gemini, Google's powerful AI, to generate high-quality content.

📝 Description
This script has been designed to automate the publication of articles in WordPress. Every 3 hours, the script is executed that:

🧠 Generate SEO-optimized articles using Google's Gemini AI.
📷 Generate quality images and include them in the article.
🌐 Automatically upload content to a WordPress website.
⏲️ Manage publication scheduling efficiently.
🚀 Characteristics
Full automation: Automatic posts every 3 hours.
AI-generated content: Leverage Google Gemini's artificial intelligence to create high-quality articles.
WordPress integration: Automatic upload and publish in WordPress.
⚙️ Installation
To run this project in your local environment, follow these steps:

Clone the repository:

git clone https://github.com/alexcerezo/wordpress-article-generator.git
cd wordpress-article-generator
Configure the repository

Set up workflow permissions so they can read and write:
Go to Settings >> Actions -> Workflow permissions and select Read and write permissions
Set up secrets

Configure the secrets of the Actions so that they can be executed correctly. Go to Settings >> Secrets and variables >> Actions and add the following secrets:
WORDPRESS_URL=https://tudominio.com/wp-json/wp/v2/posts
WORDPRESS_TOKEN=XXXX XXXX XXXX XXXX XXXX XXXX
WORDPRESS_USERNAME=username
GEMINI_API_KEY=xxxxxxxxxxxxxxx
RSS_URL=https://undominio.com/feed
🧠 Additional resources
How to create an app on WordPress?
How to get the Gemini API key?
How to get the RSS feed of a page?
🤝 Contributions
Contributions are welcome! If you have ideas or improvements, feel free to open an issue or submit a pull request.
📝 License
This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

Personal Use: You may use the software for personal or educational purposes.

Non-Commercial: Commercial use of the software is not permitted under any circumstances.

No modifications: Redistribution or creation of derivative works based on this software is not permitted unless prior authorization. If the creation of modifications is allowed, but not their distribution.
