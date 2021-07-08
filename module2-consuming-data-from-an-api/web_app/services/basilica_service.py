
from basilica import Connection
from pdb import set_trace as st
import os
from dotenv import load_dotenv

load_dotenv()
BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="oops")

# sentences = [
#     "This is a sentence!",
#     "This is a similar sentence!",
#     "I don't think this sentence is very similar at all...",
# ]
# x = 12
# connection = Connection(BASILICA_API_KEY)


def basilica_api_client():
    connection = Connection(BASILICA_API_KEY)
    print(type(connection)) #> <class 'basilica.Connection'>
    return connection
# embeddings = list(connection.embed_sentences(sentences))
#     # embeddings = list(c.embed_sentence(sentence)) for one sentence
# print(embeddings)
# # st()