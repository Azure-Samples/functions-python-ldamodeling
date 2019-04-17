echo "Provide Service Principal App ID: "
read servicePrincipalAppId

echo "Provide Service Principal Password"
read servicePrincipalPassword

echo "Provide Service Principal Tenant ID"
read servicePrincipalTenantID

echo "Provide Subscription ID"
read subscriptionId

echo "Provide path to nltk_data"
read basePathToNltkData

echo "Provide storage key for ldamodeling101 storage account"
read storageKey

storageName=ldamodel101
cd $basePathToNltkData
az login --service-principal --username $servicePrincipalAppId --password $servicePrincipalPassword --tenant $servicePrincipalTenantID
az account set --subscription $subscriptionId

# Uploading files to blob container

export AZURE_STORAGE_ACCOUNT=ldamodeling101
export AZURE_STORAGE_KEY=$storageKey

echo "Uploading dataset..."
az storage blob upload-batch -d dataset --account-name $storageName -s $basePathToNltkData/corpora/gutenberg/

echo "Uploading tokenizers..."
az storage blob upload --container-name nltk --account-name $storageName -f $basePathToNltkData/tokenizers/punkt/english.pickle -n english.pickle

echo "Uploading stopwords..."
az storage blob upload --container-name nltk --account-name $storageName -f $basePathToNltkData/corpora/stopwords/english -n english.txt

echo "Upload complete."
