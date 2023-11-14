#################################
# PARAMETERS: change as needed! #
get_gml = True
get_csv = True
get_complete_csv = True
# get_vocab_csv = True

# example files and categories
# note down all wos text files in wos_files, 
# and note their corresponding categories in the same order in wos_categories

wos_files = ["../data/Custom/EdgeML_1.txt", "../data/Custom/EdgeML_2.txt", "../data/Custom/MLAccelerator_1.txt", 
             "../data/Custom/MLAccelerator_2.txt", "../data/Custom/Neuromorphic_1.txt", "../data/Custom/Neuromorphic_2.txt", 
             "../data/Custom/SpikingNN_1.txt", "../data/Custom/SpikingNN_2.txt"]
wos_categories = ["EdgeML", "EdgeML", "MLAccelerator", "MLAccelerator", "Neuromorphic", 
                  "Neuromorphic", "SpikingNN", "SpikingNN"]

# output file naming
wos_cites_file_name = "wos.cites.csv"
wos_content_file_name = "wos.content.csv"
wos_paper_file_name = "wos.paper.csv"
wos_complete_file_name = "wos.complete.csv"
#################################

class Publication:
    title = ""
    citations = []
    doi = ""
    abstract = ""
    category = ""
    year = 0
    keywords = []

    def __init__(self, title, citations, doi, abstract, category, year, keywords=[]):
        self.title = title
        self.citations = citations
        self.doi = doi.strip()
        self.abstract = abstract
        self.category = category
        self.year = year
        self.keywords = keywords
    def __eq__(self, other):
        if isinstance(other, self):
            return self.doi == other.doi
        return False
    def __repr__(self):
        return f"<Publication title:{self.title} citations:{self.citations} doi:{self.doi} category:{self.category} year:{self.year} keywords:{self.keywords}>"

def getDOI(line): 
    doi = ""
    splitbyspace = line.split()
    for i in range(len(splitbyspace)):
        if (splitbyspace[i] == "DOI"):
            doi = splitbyspace[i+1]
            break
    return doi

def get_papers_list(publicationsinit, file, category):
    publications = publicationsinit
    title = ""
    citations = []
    doi = ""
    abstract = ""
    year = 0

    no_dois = 0

    line = file.readline()
    while file:
        # print(line)
        if line == "":
            print("BREAK")
            publications.append(Publication(title, citations, doi, abstract, category, year))
            break
        elif line == "\n":
            if (doi != ""):
                publications.append(Publication(title, citations, doi, abstract, category, year))
                title = ""
                citations = []
                doi = ""
                abstract = ""
                year = 0
            else: 
                print("no doi??")
                no_dois += 1
                print("dois: " + str(no_dois))
                doi = ""
                citations = []
                abstract = ""
                year = 0
            line = file.readline()
        elif line[:2] == "TI":
            title = line[3:].strip()
            line = file.readline()
            # print("TITLE")
            # print(title)
        elif line[:2] == "DI":
            split = line.split(" ")
            doi = split[1]
            line = file.readline()
            # print("DOI")
            # print(doi)
        elif line[:2] == "AB":
            abstract = line[3:]
            line = file.readline()
            # print("Abs")
        elif line[:2] == "CR":
            citations.append(getDOI(line))
            line = file.readline()
            while (line[:2] == "  "):
                citations.append(getDOI(line).replace("[", ""))
                line = file.readline()
            # print("CITATIONS")
            # print(citations)
        elif line[:2] == "PY":
            year = int(line[3:7])
            line = file.readline()
        else:
            line = file.readline()
    file.close()
    return publications

def get_all_publications(files_list, categories_list):
    publications = []
    for i in range(len(files_list)):
        file = (open(files_list[i], encoding="utf8"))
        publications = get_papers_list(publications, file, categories_list[i])
    return publications

import networkx as nx
import pandas as pd
# note: spacy needs python3.7+
import spacy
from keyword_spacy import KeywordExtractor
nlp = spacy.load("en_core_web_md")
# using https://github.com/wjbmattingly/keyword-spacy

def get_output_file(publications):
    # initialize csv file
    if (get_csv):
        output_cites_file = open(wos_cites_file_name, "a")
        output_cites_file.write('"cited_paper_id","citing_paper_id"\n')
        output_categories_file = open(wos_paper_file_name, "a")
        output_categories_file.write('"paper_id","class_label"\n')
        output_content_file = open(wos_content_file_name, "a")
        output_content_file.write('"paper_id","word_cited_id"\n')
    if (get_complete_csv):
        output_complete_file = open(wos_complete_file_name, "a")
        output_complete_file.write('"paper_id","category","year","keywords","cited_by"\n')

    G = nx.Graph()
    if (get_complete_csv):
        G = nx.DiGraph()
    dois = set(pub.doi for pub in publications)
    publications_clean = []

    print("DOIS")
    print(len(dois))
    print("PUBLICATIONS")
    print(len(publications))

    dois.remove("")
    seen = {}
    seen_int = 0

    nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10,
                                                     "top_n_sent": 5,
                                                     "min_ngram": 1,
                                                     "max_ngram": 1,
                                                     "strict": False})

    # i = 0
    for p in range(len(publications)):
        # print(publication)
    
        keywords = {}
        # make sure there are no duplicates

        if publications[p].doi not in seen:
            # print(i)
            # i += 1

            G.add_node(publications[p].doi, category=publications[p].category)

            # process keywords
            doc = nlp(publications[p].abstract)
            # print("Top Document Keywords:", doc._.keywords)
            doc_keywords = list()
            for keyword in doc._.keywords:
                keyword_clean = keyword[0].lower().replace(" ", "_")
                if keyword_clean not in keywords:
                    keywords[keyword_clean] = True
                if keyword_clean not in doc_keywords:
                    if (get_csv or get_complete_csv):
                        output_content_file.write('"%s","%s"\n' % (publications[p].doi, keyword_clean))
                    doc_keywords.append(keyword_clean)
                
            publications[p].keywords = doc_keywords
            publications_clean.append(publications[p])
            
            seen[publications[p].doi] = publications[p].category
        else:
            seen_int += 1
            print("seen: " + str(seen_int))
            print(publications[p].doi)
            print(seen[publications[p].doi])
            print(publications[p].category)
            # print(publications[p].abstract)
            continue   
    
    # if(get_vocab_csv):
    #     vocab_file = open("vocab_csv", "a")
    #     vocab_file.write("doi")
    #     for vocab in keywords:
    #         vocab_file.write(",")
    #         vocab_file.write(vocab)

    # second pass to add edges with existing nodes
    # edges cannot be added if nodes don't exist yet
    for publication in publications_clean:
        for citation in publication.citations:
            if (citation in dois):
                G.add_edge(publication.doi, citation)

                if (get_csv):
                    output_cites_file.write('"%s","%s"\n' % (publication.doi, citation))
        
        if (get_csv):
            output_categories_file.write('"%s","%s"\n' % (publication.doi, publication.category))
    
    # third pass to count up all in-degrees after all edges are added
    # "paper_id","category","year","keywords","cited_by"
    if (get_complete_csv):
        for publication in publications_clean:
            keyword_string = " ".join(map(str, publication.keywords))
            in_degree = G.in_degree(publication.doi)
            output_complete_file.write('"%s","%s",%d,"%s","%s"\n' % 
                                       (publication.doi, publication.category, publication.year, keyword_string, in_degree))
          
    if(get_gml): nx.write_gml(G, "citation_graph.gml")

def main():
    publications = get_all_publications(wos_files, wos_categories)
    get_output_file(publications)

if __name__ == "__main__":
    main()