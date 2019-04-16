---
services: functions, blob-storage
platforms: python
author: priyaananthasankar
---

# Topic Classification using Latent Dirichlet Allocation

[Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) (LDA) is a statistical model that classifies a document as a mixture of topics.
The sample uses a HttpTrigger to accept a set of URL's as article links or a dataset from a blob and performs the following tasks:
 - Tokenization of the entire document using NLTK
 - Removes stop words and performs lemmatization of the document using NLTK.
 - Classifies the document into topics using LDA API's from gensim Python library
 - Returns a visualization of topics using PyLDAVis Python library

# How to Deploy

## Prerequisites

- Python 3 should be installed

## Steps

- Click Deploy to Azure Button to deploy resources
[![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/)

- Run `python3 download.py` to download dataset, tokenizers and stopwords from NLTK

- Run `deploy.sh` to deploy function code and content to blob containers

## Artifacts Deployed

- Python functionality in Linux Consumption Plan
- Blob containers and storage

# Test Function App

- Send the following body in a HTTP POST request
{
    "container_name" : "name of the blob container having the dataset",
    "num_topics" : "5" 
}

# References

- [Create your first Python Function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Gensim](https://radimrehurek.com/gensim/)
- [PyLDAVis](https://github.com/bmabey/pyLDAvis)






