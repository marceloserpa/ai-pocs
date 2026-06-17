import cohere
import numpy as np
import pandas as pd
import faiss

from tqdm import tqdm

api_key = '######'
co = cohere.Client(api_key)

text = """
Interstellar is a 2014 epic science fiction film co-written, directed, and pro
duced by Christopher Nolan.
It stars Matthew McConaughey, Anne Hathaway, Jessica Chastain, Bill Irwin,
Ellen Burstyn, Matt Damon, and Michael Caine.
Set in a dystopian future where humanity is struggling to survive, the film
follows a group of astronauts who travel through a wormhole near Saturn in
search of a new home for mankind.
Brothers Christopher and Jonathan Nolan wrote the screenplay, which had its
origins in a script Jonathan developed in 2007.
Caltech theoretical physicist and 2017 Nobel laureate in Physics[4] Kip Thorne
was an executive producer, acted as a scientific consultant, and wrote a tie-in
book, The Science of Interstellar.
Cinematographer Hoyte van Hoytema shot it on 35 mm movie film in the Panavision
anamorphic format and IMAX 70 mm.
Principal photography began in late 2013 and took place in Alberta, Iceland,
and Los Angeles.
Interstellar uses extensive practical and miniature effects and the company
Double Negative created additional digital effects.
Interstellar premiered on October 26, 2014, in Los Angeles.
In the United States, it was first released on film stock, expanding to venues
using digital projectors.
The film had a worldwide gross over $677 million (and $773 million with subse
quent re-releases), making it the tenth-highest grossing film of 2014.
It received acclaim for its performances, direction, screenplay, musical score,
visual effects, ambition, themes, and emotional weight.
It has also received praise from many astronomers for its scientific accuracy
and portrayal of theoretical astrophysics. Since its premiere, Interstellar
gained a cult following,[5] and now is regarded by many sci-fi experts as one
of the best science-fiction films of all time.
Interstellar was nominated for five awards at the 87th Academy Awards, winning
Best Visual Effects, and received numerous other accolades"""

texts = text.split('.')

# removing empty spaces and newlines
texts = [t.strip(' \n') for t in texts]

response = co.embed(
    texts=texts,
    model="embed-english-v3.0",
    input_type="search_document",
).embeddings

embeds = np.array(response)
print(embeds.shape)

# creating the search index
dim = embeds.shape[1]
index = faiss.IndexFlatL2(dim)
print(index.is_trained)
index.add(np.float32(embeds))

def search(query, number_of_results=3):
    # 1. Get the query's embedding
    query_embed = co.embed(texts=[query],
    model="embed-english-v3.0",
    input_type="search_query",).embeddings[0]
    
    # 2. Retrieve the nearest neighbors
    distances , similar_item_ids = index.search(np.float32([query_embed]), number_of_results)
    
    # 3. Format the results
    texts_np = np.array(texts) # Convert texts list to numpy for easier indexing
    results = pd.DataFrame(data={'texts': texts_np[similar_item_ids[0]], 'distance': distances[0]})
    
    # 4. Print and return the results
    print(f"Query:'{query}'\nNearest neighbors:")
    return results

query = "how precise was the science?"
results = search(query)

print(results)