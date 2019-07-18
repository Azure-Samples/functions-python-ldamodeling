---
page_type: sample
languages:
- python
products:
- azure
- azure-functions
- azure-storage
description: "The sample uses a HttpTrigger to accept a dataset from a blob and performs a set of tasks."
---

# Topic Classification using Latent Dirichlet Allocation

[Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation) (LDA) is a statistical model that classifies a document as a mixture of topics.

The sample uses a HttpTrigger to accept a dataset from a blob and performs the following tasks:
 - Tokenization of the entire set of documents using NLTK
 - Removes stop words and performs lemmatization on the documents using NLTK.
 - Classifies documents into topics using LDA API's from gensim Python library
 - Returns a visualization of topics from the dataset using PyLDAVis Python library

# Getting Started

## Deploy to Azure

### Prerequisites

- Install Python 3.6+
- Install [Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local#v2)
- Install Docker
- Note: If run on Windows, use Ubuntu WSL to run deploy script

### Steps

- Click Deploy to Azure Button to deploy resources

[![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/)

or

- Deploy through Azure CLI
    - Open AZ CLI and run `az group create -l [region] -n [resourceGroupName]` to create a resource group in your Azure subscription (i.e. [region] could be westus2, eastus, etc.)
    - Run `az group deployment create --name [deploymentName] --resource-group [resourceGroupName] --template-file azuredeploy.json`

- Run `pip install nltk` to install the NLTK Python package

- Run `python3 deploy/download.py` to download dataset, tokenizers and stopwords from NLTK. Typically this will get downloaded to $HOME/nltk_data

- Make sure you have a service principal created. Follow instructions [here](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest)

- Run `sh deploy/deploy.sh` (in Ubuntu WSL or any shell) to deploy function code and content to blob containers. 

- Deploy Function App
  - [Create/Activate virtual environment](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python#create-and-activate-a-virtual-environment)
  - Run `func azure functionapp publish [functionAppName] --build-native-deps` 

## Test

- Send the following body in a HTTP POST request
```
{
    "container_name" : "dataset",
    "num_topics" : "5" 
}
```
- Sample response
```
{
    "lda_model_url": "https://ldamdlstore.blob.core.windows.net/ldamodel/ldamodel",
    "token_data_url": "https://ldamdlstore.blob.core.windows.net/ldamodel/token_data"
}
```

- Visualizing topics through PyLDAVis

  - Open the jupyter notebook VisualizeTopics.ipynb file using instructions [here](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html)

  - In the notebook, plugin values from sample response for LDA_MODEL_BLOB_URL and TOKEN_DATA_URL

Inline-style: 
![alt text](https://github.com/Azure-Samples/functions-python-ldamodeling/blob/master/assets/pyldavis.png "PyLDAVis Topic Visualization")

# References

- [Create your first Python Function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Gensim](https://radimrehurek.com/gensim/)
- [PyLDAVis](https://github.com/bmabey/pyLDAvis)

