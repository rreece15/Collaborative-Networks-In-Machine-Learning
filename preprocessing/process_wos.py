# Parameters: change as needed! #
get_gml = True
get_csv = False
wos_files = ["networkonchip.txt", "blockcipher.txt"]
#################################

class Publication:
    title = ""
    citations = []
    doi = ""
    abstract = ""
    def __init__(self, title, citations, doi, abstract):
        self.title = title
        self.citations = citations
        self.doi = doi.strip()
        self.abstract = abstract
    def __eq__(self, other):
        if isinstance(other, self):
            return self.doi == other.doi
        return False
    def __repr__(self):
        return f"<Publication title:{self.title} citations:{self.citations} doi:{self.doi}>"

def getDOI(line): 
    doi = ""
    splitbyspace = line.split()
    for i in range(len(splitbyspace)):
        if (splitbyspace[i] == "DOI"):
            doi = splitbyspace[i+1]
            break
    return doi

def get_papers_list(publicationsinit, file):
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
            publications.append(Publication(title, citations, doi, abstract))
            break
        elif line[:2] == "TI":
            if (doi != ""):
                publications.append(Publication(title, citations, doi, abstract))
                title = ""
                citations = []
                doi = ""
                abstract = ""
                print("HERE")
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
            print(line)
            while (line[:2] == "  "):
                citations.append(getDOI(line))
                line = file.readline()
        elif line[:2] == "DI":
            split = line.split(" ")
            doi = split[1]
            line = file.readline()
        else:
            line = file.readline()
    file.close()
    return publications

def get_all_publications(files_list):
    publications = []
    for file_not_open in files_list:
        file = (open(file_not_open, encoding="utf8"))
        publications = get_papers_list(publications, file)
    return publications

import networkx as nx
import spacy
# using https://github.com/wjbmattingly/keyword-spacy

def get_output_file(publications):
    if(get_gml): G = nx.Graph()
    dois = [pub.doi for pub in publications]

    i = 0
    for publication in publications:
        print(i)
        i += 1
        # print(publication)
        if(get_gml): G.add_node(publication.doi)
        for citation in publication.citations:
            if (citation in dois):
                if(get_gml): G.add_edge(publication.doi, citation)

    if(get_gml): nx.write_gml(G, "citation_graph_abs_try_savedrecs.gml")

def main():
    publications = get_all_publications(wos_files)
    get_output_file(publications)

if __name__ == "__main__":
    main()