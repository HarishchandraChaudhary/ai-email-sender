import os
import json
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# A placeholder function to simulate an AI's response.
# In a real-world scenario, you would replace this with a call to an external API (like Groq, OpenAI, etc.).
def generate_email_with_ai(prompt):
    """
    Simulates an AI generating an email based on a prompt.
    Returns a dictionary with the subject and body of the email.
    """
    # This is a placeholder for a real API call.
    # A real call might look like this:
    # from groq import Groq
    # client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    # chat_completion = client.chat.completions.create(...)
    # generated_text = chat_completion.choices[0].message.content

    print(f"Simulating AI generation for prompt: {prompt}")

    # Generate a simple, structured response based on the prompt.
    subject = f"Follow-up Regarding: {prompt[:50]}..."
    body = f"""
Dear [Recipient Name],

This email is in reference to the following topic: "{prompt}".

Based on your request, here is a draft:
[AI generated content here]

Please let me know if you have any questions or require further details.

Best regards,
[Your Name]
"""
    return {"subject": subject, "body": body.strip()}


@app.route("/", methods=["GET"])
def index():
    """
    Renders the main application page with a form.
    """
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Email Sender</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen">
    <div class="w-full max-w-3xl bg-white shadow-xl rounded-2xl p-8 space-y-6">
        <h1 class="text-4xl font-extrabold text-center text-gray-900">AI Email Sender</h1>

        <form id="emailForm" class="space-y-4">
            <div>
                <label for="recipients" class="block text-sm font-medium text-gray-700">Recipients (comma-separated)</label>
                <input type="text" id="recipients" name="recipients" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2" placeholder="e.g., alice@example.com, bob@example.com" required>
            </div>
            <div>
                <label for="prompt" class="block text-sm font-medium text-gray-700">Email Prompt</label>
                <textarea id="prompt" name="prompt" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2" placeholder="e.g., Write a professional email to a client, summarizing our project progress." required></textarea>
            </div>
            <button type="button" id="generateButton" class="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-bold hover:bg-blue-700 transition-colors disabled:bg-blue-400">Generate Email</button>
        </form>

        <div id="emailContainer" class="hidden space-y-4 mt-6">
            <h2 class="text-2xl font-bold text-gray-900">Edit and Send Email</h2>
            <div>
                <label for="emailSubject" class="block text-sm font-medium text-gray-700">Subject</label>
                <input type="text" id="emailSubject" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2" readonly>
            </div>
            <div>
                <label for="emailBody" class="block text-sm font-medium text-gray-700">Body</label>
                <textarea id="emailBody" rows="10" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-2" required></textarea>
            </div>
            <button type="button" id="sendButton" class="w-full bg-green-600 text-white py-2 px-4 rounded-md font-bold hover:bg-green-700 transition-colors disabled:bg-green-400">Send Email</button>
        </div>

        <div id="message" class="text-center mt-4 hidden"></div>
    </div>

    <script>
        const form = document.getElementById('emailForm');
        const generateButton = document.getElementById('generateButton');
        const sendButton = document.getElementById('sendButton');
        const emailContainer = document.getElementById('emailContainer');
        const messageDiv = document.getElementById('message');

        generateButton.addEventListener('click', async () => {
            const recipients = document.getElementById('recipients').value;
            const prompt = document.getElementById('prompt').value;

            if (!recipients || !prompt) {
                messageDiv.className = 'text-red-500';
                messageDiv.textContent = 'Please fill out all fields.';
                messageDiv.style.display = 'block';
                return;
            }

            generateButton.disabled = true;
            messageDiv.className = 'text-gray-500';
            messageDiv.textContent = 'Generating email...';
            messageDiv.style.display = 'block';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt })
                });

                const data = await response.json();
                if (response.ok) {
                    document.getElementById('emailSubject').value = data.subject;
                    document.getElementById('emailBody').value = data.body;
                    emailContainer.style.display = 'block';
                    messageDiv.className = 'text-green-500';
                    messageDiv.textContent = 'Email generated successfully. You can now edit it.';
                } else {
                    messageDiv.className = 'text-red-500';
                    messageDiv.textContent = data.error || 'Failed to generate email.';
                }
            } catch (error) {
                console.error('Error:', error);
                messageDiv.className = 'text-red-500';
                messageDiv.textContent = 'An error occurred. Please try again.';
            } finally {
                generateButton.disabled = false;
            }
        });

        sendButton.addEventListener('click', async () => {
            const recipients = document.getElementById('recipients').value;
            const subject = document.getElementById('emailSubject').value;
            const body = document.getElementById('emailBody').value;

            if (!recipients || !subject || !body) {
                messageDiv.className = 'text-red-500';
                messageDiv.textContent = 'Email content is incomplete. Please fill all fields.';
                messageDiv.style.display = 'block';
                return;
            }

            sendButton.disabled = true;
            messageDiv.className = 'text-gray-500';
            messageDiv.textContent = 'Sending email...';
            messageDiv.style.display = 'block';

            try {
                const response = await fetch('/send_email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        recipients: recipients.split(',').map(r => r.trim()),
                        subject: subject,
                        body: body
                    })
                });

                const data = await response.json();
                if (response.ok) {
                    messageDiv.className = 'text-green-500';
                    messageDiv.textContent = data.message;
                    emailContainer.style.display = 'none';
                    form.reset();
                } else {
                    messageDiv.className = 'text-red-500';
                    messageDiv.textContent = data.error || 'Failed to send email.';
                }
            } catch (error) {
                console.error('Error:', error);
                messageDiv.className = 'text-red-500';
                messageDiv.textContent = 'An error occurred. Please try again.';
            } finally {
                sendButton.disabled = false;
            }
        });
    </script>
</body>
</html>
    """)

@app.route("/generate", methods=["POST"])
def generate_email():
    """
    Endpoint to generate the email using the AI.
    """
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        email_data = generate_email_with_ai(prompt)
        return jsonify(email_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send_email", methods=["POST"])
def send_email():
    """
    Endpoint to "send" the email. This is a simulation.
    """
    data = request.json
    recipients = data.get("recipients")
    subject = data.get("subject")
    body = data.get("body")

    if not all([recipients, subject, body]):
        return jsonify({"error": "All fields are required"}), 400

    # In a real application, you would use a library like smtplib or a service API (SendGrid, Mailgun)
    # to send the email. This is a placeholder that prints to the console.
    print("\n--- Email Sending Simulation ---")
    print(f"Recipients: {', '.join(recipients)}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print("--------------------------------")

    return jsonify({"message": "Email sending simulated successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
