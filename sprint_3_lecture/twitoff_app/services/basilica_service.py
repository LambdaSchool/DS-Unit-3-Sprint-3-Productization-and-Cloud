from basilica import Connection
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BASILICA_API_KEY", default='OOPS')

connection = Connection(API_KEY)
print(type(connection))

if __name__ == "__main__":

    embedding = connection.embed_sentence("HELLO WORLD")
    print(embedding) #>

    sentences = [
        "This is a sentence!",
        "This is a similar sentence!",
        "I don't think this sentence is very similar at all...",
    ]

    embeddings = list(connection.embed_sentences(sentences))
    for embed in embeddings:
        print("----------")
        print(embed) #> a list with 768 floats from -1 to 1
