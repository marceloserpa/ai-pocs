import os
import string

import cohere
import numpy as np
import pandas as pd
import faiss

from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction import _stop_words
from tqdm import tqdm

load_dotenv()

api_key = os.environ["CO_API_KEY"]
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

# tokenizer used to build the BM25 index and to process queries:
# lowercase, strip punctuation, drop English stop words
def bm25_tokenizer(text):
    tokenized_doc = []
    for token in text.lower().split():
        token = token.strip(string.punctuation)
        if len(token) > 0 and token not in _stop_words.ENGLISH_STOP_WORDS:
            tokenized_doc.append(token)
    return tokenized_doc

# build the BM25 lexical index from the corpus
tokenized_corpus = [bm25_tokenizer(passage) for passage in tqdm(texts)]
bm25 = BM25Okapi(tokenized_corpus)

def keyword_and_reranking_search(query, top_k=3, num_candidates=10):
    print("Input question:", query)
    
    ##### BM25 search (lexical search) #####
    bm25_scores = bm25.get_scores(bm25_tokenizer(query))
    top_n = np.argpartition(bm25_scores, -num_candidates)[-num_candidates:]
    bm25_hits = [{'corpus_id': idx, 'score': bm25_scores[idx]} for idx in top_n]
    bm25_hits = sorted(bm25_hits, key=lambda x: x['score'], reverse=True)
    print(f"Top-3 lexical search (BM25) hits")
    
    for hit in bm25_hits[0:top_k]:
        print("\t{:.3f}\t{}".format(hit['score'], texts[hit['corpus_id']].replace("\n", " ")))
    #Add re-ranking
    docs = [texts[hit['corpus_id']] for hit in bm25_hits]
    print(f"\nTop-3 hits by rank-API ({len(bm25_hits)} BM25 hits re-ranked)")
    results = co.rerank(query=query, documents=docs, model="rerank-english-v3.0", top_n=top_k, return_documents=True)
    # print(results.results)
    for hit in results.results:
        # print(hit)
        print("\t{:.3f}\t{}".format(hit.relevance_score, hit.document.text.replace("\n", " ")))

query = "how precise was the science?"
initial_results = keyword_and_reranking_search(query)

print(initial_results)
