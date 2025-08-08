AI Email Sender
This is a simple full-stack application that uses an AI to generate email drafts. Users can provide a prompt, generate an editable email, and then "send" it to a list of recipients.

Project Structure
ai_email_sender_app.py: The main Flask application file. It contains both the backend logic and the frontend HTML/JavaScript.

requirements.txt: Lists all the necessary Python dependencies.

.env: This file (not provided in the repo) is used to store sensitive information like API keys.

README.md: This file, which explains the project and setup.

Setup Instructions
1. Create the .env file
Create a file named .env in the root of the project. If you were using a real AI and email service, you would put your keys here. For this simulation, the file can be empty, but it's good practice to include it.

# Example .env file for a real application
# GROQ_API_KEY="your-groq-api-key"
# SMTP_SERVER="smtp.your-provider.com"
# ...etc

2. Install Dependencies
Using a virtual environment is highly recommended.

# Create and activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

3. Run the Application
Once the dependencies are installed, you can start the Flask application.

python ai_email_sender_app.py

The application will be running on http://127.0.0.1:5000. Open this URL in your web browser to use the application.
