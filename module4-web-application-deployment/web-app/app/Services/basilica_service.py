import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")
def basilica_api_client():
    connection = basilica.Connection(API_KEY)
    return connection

if __name__ == "__main__":
    connection = basilica.Connection(API_KEY)

    sentences = ["Hello world!", "How are you?"]

    print(sentences)

    embeddings = connection.embed_sentences(sentences)

    print(list(embeddings)) # [[0.8556405305862427, ...], ...]