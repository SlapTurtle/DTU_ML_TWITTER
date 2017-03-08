def process():
    data = open("C:/Fagprojekt/data.txt")
    for line in data:
        print(line)
        step1 = tokenize(line)
        print(step1)
        step2 = remove_stopwords()
        print(step2)
        step3 = remove_specialchars()
        print(step3)

# split string by ' ' into word array, remove symbols and emoticons
def tokenize(string):
    return string, string, string

# non-emotional words are removed (a,is, etc.)
# for classification: only adverbs are kept
# for neural network: nouns and adverbs are kept
def remove_stopwords(list = []):
    print()

# remove special characters / unknown symbols / URLs / other irrelevant strings
def remove_specialchars(list = []):
    print()

# move back into new .txt
def insert_to_file(list = []):
    print()

if __name__ == '__main__':
        process()