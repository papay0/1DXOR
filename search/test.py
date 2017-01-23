"""
Generates all graphics for recall and precision
using different methods.
"""

import os
import matplotlib.pyplot as plt
from search import SearchEngine
from augment_query import augment
from stem import stem_query
from bs4 import BeautifulSoup
from query_helpers import text_to_query

QUERIES_FILE = os.path.dirname(os.path.abspath(__file__))+"/test/requetes.html"
GROUND_TRUTH_DIR = os.path.dirname(os.path.abspath(__file__))+"/test/"

def compute_recall(scores, ground_truth):
    """ return document string """
    relevant_documents = [doc_relevance[0] for doc_relevance in ground_truth if doc_relevance[1]]
    relevant_selected = [score for score in scores if score[0] in relevant_documents]
    return len(relevant_selected)/len(relevant_documents)

def compute_precision(scores, ground_truth):
    """ return document string """
    relevant_documents = [doc_relevance[0] for doc_relevance in ground_truth if doc_relevance[1]]
    relevant_selected = [score for score in scores if score[0] in relevant_documents]
    return len(relevant_selected)/len(scores)

def process_request(query, ground_truth):
    """ process a request and compute quality """
    search_engine = SearchEngine(augment, stem_query, "localhost:27017")
    search_engine.search(query)
    results = search_engine.get_results()
    evaluation = dict()
    for distance_method in ["scalar", "dice", "cosinus", "jaccard"]:
        for tf_method in ["simple", "normalized", "robertson"]:
            for idf in [True, False]:
                scores = results.get_scores(
                    use_idf=idf,
                    tf_method=tf_method,
                    distance_method=distance_method)
                recall = [0]
                precision = [1]
                for limit in range(1, len(scores)):
                    recall.append(compute_recall(scores[:limit], ground_truth))
                    precision.append(compute_precision(scores[:limit], ground_truth))
                plt.plot(recall, precision, '-' if distance_method == "scalar" else '--')
                evaluation[distance_method] = (recall, precision)
    plt.show()
    return evaluation

def parse_requests():
    """ parse queries file """
    html = open(os.path.dirname(os.path.abspath(__file__))+"/test/requetes.html")
    soup = BeautifulSoup(html, "html.parser")
    queries = [text_to_query(tag.text) for i, tag in enumerate(soup.findAll("dd")) if i%2 == 0]
    return queries

def main():
    """ Make a search using program input as base query """
    queries = parse_requests()
    for query_id, query in enumerate(queries):
        print(query)
        gt_file = open(GROUND_TRUTH_DIR+"qrelQ"+str(query_id + 1)+".txt")
        ground_truth = []
        for line in gt_file.readlines():
            doc_name, relevant = line.split()
            ground_truth.append((doc_name, int(relevant) > 0))
        print(process_request(query, ground_truth))

   # search_engine = SearchEngine(augment, stem_query, "localhost:27017")
   # search_engine.search(input_to_query(argv))
   # results = search_engine.get_results()
   # print(results.get_scores("robertson", "scalar", True))


if __name__ == "__main__":
    main()
