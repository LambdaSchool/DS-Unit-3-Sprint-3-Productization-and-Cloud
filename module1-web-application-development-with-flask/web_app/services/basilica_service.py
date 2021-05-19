from basilica import Connection
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY")

connection = Connection(API_KEY)
print("CONNECTION", type(connection))

if __name__ == "__main__":
    sentences = [
        "This is a sentence!",
        "This is a similar sentence!",
        "I don't think this sentence is very similar at all...",
    ]
    embeddings = list(connection.embed_sentences(sentences))
    print(embeddings)

    embedding = list(connection.embed_sentence("Hello world!", model="twitter"))
    print(type(embedding))
    print(type(embedding[0]))
    print(len(embedding))

    breakpoint()