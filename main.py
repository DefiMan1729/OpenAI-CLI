
import typer
from openai import OpenAI
import json
from art import text2art
# api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key='')

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

VERSION = "0.0.1729"

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