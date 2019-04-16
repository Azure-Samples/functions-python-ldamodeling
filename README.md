# Topic Classification using Latent Dirichlet Allocation
---
services: functions, blob-storage
platforms: python
author: priyaananthasankar
---

Latent Dirichlet Allocation (LDA) is a statistical model that classifies a document as a mixture of topics.
The sample uses a HttpTrigger to accept a set of URL's as article links or a dataset from a blob and performs the following tasks:
 - performs tokenization of the entire document using NLTK.
 - removes stop words and performs lemmatization of the document using NLTK.
 - topic models the documents using LDA API's using Python gensim library.
 - Returns a HTML link of the visualized topics through PyLDAVis library.

# How to Deploy

This sample can be deployed using this button:


This deploys the following:

- Python functionality in Linux Consumption Plan
- Blob containers and storage

