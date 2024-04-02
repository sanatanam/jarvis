import twilio
from flask import Flask, request
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from prompt_toolkit import HTML

# Replace with your actual credentials
account_sid = "SK76708cc8c8615ee09966bb1f8409193b"
auth_token = "WRrpM4iEN9FvWa7K643vjgE6BxkIyBEU"

# Configure API key (replace with your actual API key)
genai.configure(api_key="AIzaSyAo4Vdfe3-FQT2AzyqKbPXJ-R2c2JaupJk")

# Set up generation configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

# Set up safety filters (consider enabling for production)
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Create the model instance
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def handle_call():
    """Handles incoming calls and user input (speech recognition)."""

    if request.method == "POST":
        # Retrieve user input from Twilio's request parameters (optional)
        user_input = request.form.get("Digits", None)

        # Handle valid input (user pressed 1)
        if user_input == "1":
            # Use Twilio's Speech Recognition API
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)

            try:
                # Improve recognition accuracy (consider alternatives)
                user_input = r.recognize_google(audio, language="en-US", show_all=True)
                # Extract the most likely transcription
                most_likely = user_input.get("alternative")[0]["transcript"]
                print(f"You: {most_likely}")
                user_input = most_likely  # Use the most likely transcription
            except sr.UnknownValueError:
                print("Could not understand audio")
                user_input = "Speech recognition failed. Please try again."
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                user_input = "An error occurred. Please try again."

            # Generate response using the model
            prompt_parts = [user_input]
            response = model.generate_content(prompt_parts)

            # Create TwiML response to play back the generated text
            twiml_response = f"""
            <Response>
                <Say>{response.text}</Say>
            </Response>
            """
            return twiml_response

        else:
            # Handle invalid input (e.g., user pressed something else)
            twiml_response = f"""
            <Response>
                <Say>Sorry, I didn't understand that.</Say>
            </Response>
            """
            return twiml_response

    else:
        # Handle initial GET request (optional welcome message)
        welcome_message_text = "Welcome to Chaitanya, the AI Assistant! Came into existence by the efforts of Pranav Visen.Press 1 to interact."
        welcome_message = welcome_message_text
        print(welcome_message)  # Inspect the string for debugging

        # Create TwiML response to play back the welcome message
        twiml_response = f"""
        <Response>
            <Say>{welcome_message}</Say>
        </Response>
        """
        return twiml_response
    


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production