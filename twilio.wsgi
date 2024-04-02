from flask import Flask

def create_app():
  """
  This function creates a Flask application instance with proper configuration
  for production deployments (debug mode disabled).
  """
  app = Flask(__name__)

  # Load configuration (consider using environment variables or a config file)
  app.config['DEBUG'] = False  # Set debug mode to False (important for production)
  # ... other configuration options (e.g., secret keys, database connections)

  # Import your main application script (likely twilio.py)
  from twilio import handle_call  # Assuming your call handling logic is in twilio.py

  @app.route("/", methods=["GET", "POST"])
  def handle_request():
    """
    This function routes incoming requests to the handle_call function
    in your main application script (twilio.py).
    """
    return handle_call()

  return app

# Create the application instance (call the create_app function)
app = create_app()

if __name__ == "__main__":
  # This block is only executed when the script is run directly (not imported)
  app.run()  # Run the Flask application (adjust for deployment platform)
