import glob,os,logging
import pickle 
import gensim
from gensim import corpora
import pyLDAvis.gensim
import nltk
from nltk.tokenize import RegexpTokenizer   
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk import word_tokenize
from azure.storage.blob import BlobServiceClient

PUNKT_SENTENCE_TOKENIZER_BLOBURL = os.environ.get('NltkPunktSentenceTokenizer')
STOPWORDS_ENGLISH_SET_BLOBURL = os.environ.get('NltkStopWords')
GUTENBERG_BLOB_ACCOUNT_NAME = os.environ.get('GutenbergBlobAccountName')
GUTENBERG_BLOB_ACCOUNT_KEY = os.environ.get('GutenbergBlobAccountKey')

_treebank_word_tokenizer = TreebankWordTokenizer()
_nltk_stopwords = nltk.data.load(STOPWORDS_ENGLISH_SET_BLOBURL).split('\n')
_nltk_tokenizer = nltk.data.load(PUNKT_SENTENCE_TOKENIZER_BLOBURL)
_nltk_stopwords.extend(['could','would','still','shall'])
container_models = "ldamodel"

def classify(container_name, num_topics):
    nltk.download('wordnet')
    # List Blobs in the container
    blob_service_client = BlobServiceClient(
        account_url=f"https://{GUTENBERG_BLOB_ACCOUNT_NAME}.blob.core.windows.net",
        credential={"account_name": f"{GUTENBERG_BLOB_ACCOUNT_NAME}", "account_key":f"{GUTENBERG_BLOB_ACCOUNT_KEY}"}
        )
    container_client = blob_service_client.get_container_client(container=container_name)
    
    logging.info("Listing blobs in the container...")
    generator = container_client.list_blobs()
    data = [] 
    doc_map = {} 
    doc_id = 1

    # First level data cleaning
    for blob in generator:
        logging.info("Blob name: " + blob.name)
        readblob = container_client.download_blob(blob=blob.name)
        if blob.name != "README":
            doc_map[doc_id] = blob.name
            blob_content  = str(readblob.readall())
            raw = blob_content.replace('\n','').replace('\r','').replace('\r\n','')
            cleaned_raw = raw.replace('\\r\\n','')
            data.append(cleaned_raw)
            doc_id += 1
        else:
            pass

    # Tokenizing and Lemmatizing
    token_data = []
    for doc in data:
        tokens = clean_text(doc)
        token_data.append(tokens)
    pickled_token_data = pickle.dumps(token_data) 
    pickled_docmap = pickle.dumps(doc_map)

    # Store token data and document map for gensim
    container_models_client = blob_service_client.get_container_client(container=container_models)
    container_models_client.upload_blob(name="token_data", data=pickled_token_data)
    container_models_client.upload_blob(name="docmap", data=pickled_docmap)

    dictionary = corpora.Dictionary(token_data)
    corpus = [dictionary.doc2bow(text) for text in token_data]

    # Train LDA Model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word=dictionary, passes=10)
    pickled_ldamodel = pickle.dumps(ldamodel)
    container_models_client.upload_blob(name='ldamodel', data=pickled_ldamodel)

    # Construct LDA Blob URL
    lda_model_url = "https://" + GUTENBERG_BLOB_ACCOUNT_NAME + ".blob.core.windows.net/" + container_models + "/" + "ldamodel"
    token_data_url = "https://" + GUTENBERG_BLOB_ACCOUNT_NAME + ".blob.core.windows.net/" + container_models + "/" + "token_data"
    response = {}
    response["lda_model_url"] = lda_model_url
    response["token_data_url"] = token_data_url
    return response

def lemmatize(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def clean_text(text):
    '''
        Removes stopwords (commonly used words), tokenizes
        and removes variants of the same word (lemmatize)

        Returns:
        Cleaned set of tokens
    '''
    stopwords = set(_nltk_stopwords)
    tokens = custom_nltk_tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in stopwords]
    tokens = [lemmatize(token) for token in tokens]
    return tokens

def custom_nltk_tokenize(text,language='english', preserve_line=False):
        '''
        Tokenizes used TreeBank Tokenizer and PunktSentence Tokenizer.
        nltk_tokenizer variable in this method preloads the PunktSentenceTokenizer for English
        from Azure blob

        Returns:
        Tokenized text
        '''
        sentences = [text] if preserve_line else _nltk_tokenizer.tokenize(text, language)
        return [token for sent in sentences
            for token in _treebank_word_tokenizer.tokenize(sent)]
   
