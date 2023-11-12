#################################
# PARAMETERS: change as needed! #
get_gml = True
get_csv = True

# example files and categories
# note down all wos text files in wos_files, 
# and note their corresponding categories in the same order in wos_categories

wos_files = ["EdgeML_1.txt", "EdgeML_1.txt", "MLAccelerator_1.txt", "MLAccelerator_2.txt", 
             "Neuromorphic_1.txt", "Neuromorphic_2.txt", "SpikingNN_1.txt", "SpikingNN_1.txt"]
wos_categories = ["EdgeML", "EdgeML", "MLAccelerator", "MLAccelerator", "Neuromorphic", 
                  "Neuromorphic", "SpikingNN", "SpikingNN"]

# output file naming
wos_cites_file_name = "wos.cites.csv"
wos_content_file_name = "wos.content.csv"
wos_paper_file_name = "wos.paper.csv"
#################################

class Publication:
    title = ""
    citations = []
    doi = ""
    abstract = ""
    category = ""
    def __init__(self, title, citations, doi, abstract, category):
        self.title = title
        self.citations = citations
        self.doi = doi.strip()
        self.abstract = abstract
        self.category = category
    def __eq__(self, other):
        if isinstance(other, self):
            return self.doi == other.doi
        return False
    def __repr__(self):
        return f"<Publication title:{self.title} citations:{self.citations} doi:{self.doi} category:{self.category}>"

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

    line = file.readline()
    while file:
        # print(line)
        if line == "":
            print("BREAK")
            publications.append(Publication(title, citations, doi, abstract, category))
            break
        elif line[:2] == "TI":
            if (doi != ""):
                publications.append(Publication(title, citations, doi, abstract, category))
                title = ""
                citations = []
                doi = ""
                abstract = ""
            else: 
                print("no doi??")
            split = line.split(" ")
            title = split[1]
            line = file.readline()
        elif line[:2] == "AB":
            abstract = line[3:]
            line = file.readline()
        elif line[:2] == "CR":
            citations.append(getDOI(line))
            line = file.readline()
            while (line[:2] == "  "):
                citations.append(getDOI(line).replace("[", ""))
                line = file.readline()
        elif line[:2] == "DI":
            split = line.split(" ")
            doi = split[1]
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
# note: spacy needs python3.7+
import spacy
from keyword_spacy import KeywordExtractor
nlp = spacy.load("en_core_web_md")
# using https://github.com/wjbmattingly/keyword-spacy

def get_output_file(publications):
    if(get_gml): G = nx.Graph()
    dois = set(pub.doi for pub in publications)
    dois.remove("")
    seen = set()

    i = 0
    for publication in publications:
        print(i)
        i += 1
        # print(publication)
        if(get_gml): G.add_node(publication.doi, category=publication.category)

        # make sure there are no duplicates
        if publication.doi not in seen:
            seen.add(publication.doi)
        else:
            continue
    
    # initialize csv file
    if (get_csv):
        output_cites_file = open(wos_cites_file_name, "a")
        output_cites_file.write('"cited_paper_id","citing_paper_id"\n')
        output_categories_file = open(wos_paper_file_name, "a")
        output_categories_file.write('"paper_id","class_label"\n')
        output_content_file = open(wos_content_file_name, "a")
        output_content_file.write('"paper_id","word_cited_id"\n')

    nlp.add_pipe("keyword_extractor", last=True, config={"top_n": 10,
                                                     "top_n_sent": 5,
                                                     "min_ngram": 1,
                                                     "max_ngram": 1,
                                                     "strict": False})
    
    keywords = set()
    for publication in publications:
        if (get_csv):
            # process keywords
            doc = nlp(publication.abstract)
            print("Top Document Keywords:", doc._.keywords)
            doc_keywords = set()
            for keyword in doc._.keywords:
                keyword_clean = keyword[0].lower().replace(" ", "_")
                if keyword_clean not in keywords:
                    keywords.add(keyword_clean)
                if keyword_clean not in doc_keywords:
                    output_content_file.write('"%s","%s"\n' % (publication.doi, keyword_clean))
                    doc_keywords.add(keyword_clean)

        # process edge graph
        for citation in publication.citations:
            if (citation in dois):
                if(get_gml): G.add_edge(publication.doi, citation)
                if (get_csv):
                    output_cites_file.write('"%s","%s"\n' % (publication.doi, citation))
                    output_categories_file.write('"%s","%s"\n' % (publication.doi, publication.category))
                    
    if(get_gml): nx.write_gml(G, "citation_graph.gml")

def main():
    publications = get_all_publications(wos_files, wos_categories)
    get_output_file(publications)

if __name__ == "__main__":
    main()