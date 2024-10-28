# Custom CLI App for OpenAI

This project provides a Command Line Interface (CLI) application using Python's `typer` library and OpenAI's API. The app allows users to interact with OpenAI's models and extract key option parameters from input text directly from CLI.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. It's recommended to use a virtual environment to manage your dependencies.

### Setting Up the Virtual Environment

**Create and Activate a virtual environment**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate
```
**Install Dependencies from requirements.txt**
```sh
pip install -r requirements.txt
```
## Project structure

```sh
typer_cli_app/
│
├── main.py              # Main script to run the CLI app
├── README.md            # This README file
└── .venv/               # Virtual environment directory (not included in version control)
```
## Main script
``` sh
import os
import typer
from openai import OpenAI
import json

# Fetch API key from environment variables for better security
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

# Define custom functions for OpenAI
Custom_Function_Derivatives = [
    {
        'name': 'extract_options_info',
        'description': 'Get the key option parameters from the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'option': {
                    'type': 'string',
                    'description': 'Name of the Option call or put'
                },
                'strike': {
                    'type': 'integer',
                    'description': 'Strike price of the option.'
                },
                'premium': {
                    'type': 'integer',
                    'description': 'Premium of the option.'
                }
            }
        }
    }
]

app = typer.Typer()

VERSION = "1.0.1729"

@app.command()
def version():
    """
    CLI command to display the version of the application.
    """
    typer.echo(f"Version: {VERSION}")

@app.command()
def promptai(question: str):
    """
    CLI command to prompt the AI with a question and get a JSON response.
    :param question: The question to ask the AI.
    """
    typer.echo(f"Here is your plain English question: {question}")
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': question}],
        functions=Custom_Function_Derivatives,
        function_call='auto'
    )
    try:
        json_response = json.loads(response.choices[0].message.function_call.arguments)
        typer.echo(f"Here is the JSON extract of key parameters: {json_response}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        typer.echo(f"Failed to parse response: {e}")

@app.command()
def goodbye():
    """
    CLI command to say goodbye.
    """
    typer.echo("Goodbye")

@app.command()
def asciiart():
    """
    CLI command to display fancy ASCII art with the label "AI On CLI".
    """
    art = text2art("AI On CLI")
    typer.echo(art)

if __name__ == "__main__":
    app()

```
## Sample CLI app
<img width="620" alt="AIonCLI" src="https://github.com/user-attachments/assets/9bd62571-37a5-49ee-a453-1a482b581d05">
