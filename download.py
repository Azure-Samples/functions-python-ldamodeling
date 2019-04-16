import nltk

# Downloads the data set and tokenizers into $HOME/nltk_data folder
print("Downloading prequisites...")
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

# Get id's of any dataset you want
def get_dataset(prefixStr):
    dataset = [ids for ids in nltk.corpus.gutenberg.fileids() 
                        if ids.startswith(prefixStr)]
    print(dataset)

# Get Sentences https://www.nltk.org/book/ch02.html
from nltk.corpus import gutenberg
def get_sentences(file_id):
    print(gutenberg.sents(file_id))

# TRY IT...

#get_dataset('shakespeare')
#get_dataset('austen')
#get_sentences('austen-emma.txt')

