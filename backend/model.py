import numpy as np
import pandas as pd
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import porter
from nltk.corpus import stopwords
from nltk import pos_tag


def preprocess(sentences):
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

    clean_sentences = [s.lower() for s in clean_sentences]

    # remove stop words
    stop_words = set(stopwords.words('english'))

    tags = set(["NN", "NNS", "NNP", "JJ", "JJR", "JJS"])

    stemmer = porter.PorterStemmer()
    # print(clean_sentences)
    filtered_sentences = []

    # remove stop words and filter based on tags, allow only nouns and adjective words
    for sent in clean_sentences:
        filter_sent = []
        for word, tag in pos_tag(word_tokenize(sent)):
            if tag not in tags or word in stop_words:
                continue
        
            filter_sent.append(stemmer.stem(word))
        filtered_sentences.append(filter_sent)
    
    return filtered_sentences

def find_similarity(sentences):
    S = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            
            S[i][j] = sentence_similarity(sentences[i], sentences[j])

    return normalize_matrix(S)

def normalize_matrix(S):
    for i in range(len(S)):
        if S[i].sum() == 0:
            S[i] = np.ones(len(S))

        S[i] /= S[i].sum()

    return S

def sentence_similarity(sent1, sent2):
    overlap = len(set(sent1).intersection(set(sent2)))

    if overlap == 0:
        return 0

    return overlap / (np.log10(len(sent1)) + np.log10(len(sent2)))


def pagerank(A, eps=0.0001, d=0.85):
    R = np.ones(len(A))

    while True:
        r = np.ones(len(A)) * (1 - d) + d * A.T.dot(R)
        if abs(r - R).sum() <= eps:
            return r
        R = r

def get_topk_sent(sentences, scores, k=3):
    zip_sent = zip(sentences, scores)
    sorted_sent, scores = zip(*sorted(zip_sent, key=lambda x:x[1], reverse=True))
    return sorted_sent[:k]

def summarize(raw):
    summary = []

    sentences = sent_tokenize(raw.get('data', ""))
    # print(sentences)
    # sentences = [s.replace("\n", "") for row in sentences for s in row]

    filtered_sentences = preprocess(sentences)
    sim_mat = find_similarity(filtered_sentences)
    # print(sim_mat)
    scores = pagerank(sim_mat)
    final_summary = get_topk_sent(sentences, scores)
    
    for sens in final_summary:
        summary.append("".join(sens))
    
    return summary