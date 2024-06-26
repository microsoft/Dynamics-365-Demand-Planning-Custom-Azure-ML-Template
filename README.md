# Custom-ML-in-DemandPlanning

## Introduction 
This code repository serves primarily as an illustrative example demonstrating key aspects of interfacing with the Dynamics 365 Demand Planning application through Azure Machine Learning (Azure ML). It provides insights into how to read input data, handle standard and custom parameters, and generate output that aligns with the application's consumption requirements.

The repository consists of this ReadMe file, a scoring script, a Docker file and demonstrative videos.

## Usage Recommendations
While the provided code offers valuable insights into the integration process, it is essential to understand that it is not intended for direct deployment in production environments. Instead, it should be treated as a reference or starting point for developers looking to implement similar solutions.
Given the complexity and specific requirements of production environments, including considerations such as scalability, security, and performance optimization, it is recommended to further customize and validate the codebase according to the unique needs of the target deployment scenario.

## End-to-end
### Prerequisites
1. Sign in to the [AzureML](https://ml.azure.com/). If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/en-us/free/) before you begin.
2. Select your workspace, if it is not already open. If you don't have one, complete [Create resources you need to get started](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2) to create a workspace and learn about it.
3. You need a storage account for your workspace. If you don't have a storage account complete [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)

### Getting started 
1. Create a Compute Cluster
   > Compute > Compute Cluster > + New > Select Virtual machine
3. Create an envrionment using the files attached
   > Environment > Custom Envionments > +Create > Select form environment source > Create a new docker context > use zip file for the docker file and yaml file
4. Create the Scoring Script using the file attached
5. Register a model
   > Models > +Register > from local files > upload scoring script 
6. Create an Endpoint
   > Endpoints > Batch Endpoints > +Create > Name it > select your model > select deployment name > upload scoring script > select environment > select compute cluster
6. Add new Deployment
   > your endpoint > +Add deployment > same steps as in '4. Create endpoint' (Take care to update the default deployment)

For more information go to [Get started woth Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/tutorial-azure-ml-in-a-day?view=azureml-api-2) and watch the first video for demonstration
### Connect demand planning with you Custom Model 

How to [ Use Custom Azure ML in Demand Planning](https://learn.microsoft.com/en-us/dynamics365/supply-chain/demand-planning/custom-azure-machine-learning-algorithms) is supposed to provide detailed documentation to connecting Demand Planning with your Custom ML in AzureML

1. Set up a third party App and Assign access to workspace and storage account
   > this steps are starting from [Azure Portal](https://ms.portal.azure.com/#home)
2. Connect to Azure ML Service from Demand Planning
   > the second video shows in detail where to find the information you need to connect demand planning with AzureML
   
> Subscription ID - got to workspace, select your storage account, there you find the subscription ID

   > Resource Group Name - go to workspace, there you find your Resource Group
   
   > Workspace Name - enter your workspace name
   
   > Storage Account Name - go to workspace there you find your workspace's storage account
   
   > Application ID - go to your third party app, there you find the application ID
   
   > Application Secret - go to you third party app, go to Certificates & Secrets, create a new client secret (it gets deleted once you leave the page) -> you need the 'Value' not the Secret ID!

3. Set up a forecast using your Custom ML
   > Operations > Forecast profiles > add Custom step > three dots > settings > Custom action configuration > select you Custom ML Model >  Azure ML Endpoints > select your batch endpoint

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
