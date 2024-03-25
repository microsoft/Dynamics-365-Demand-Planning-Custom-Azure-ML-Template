# Custom-ML-in-DemandPlanning

## Introduction 
This project aims to serve as a bridge between Custom ML models developed in Azure ML and the Dynamics 365 Demand Planning application. It is supposed to guide you thought the process of creating your own Custom forecasting model in Azure ML and how to connect demand planning with it. The Documentation consists of this ReadMe file, a scoring script, a Docker file and demonstrative videos. Use the files to easily set up your own Custom ML.
## End-to-end
### Prerequisites
1. Sign in to the [AzureML](https://ml.azure.com/). If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/en-us/free/) before you begin.
2. Select your workspace, if it is not already open. If you don't have one, complete [Create resources you need to get started](https://learn.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources?view=azureml-api-2) to create a workspace and learn about it.
3. You need a storage account for your workspace. If you don't have a storage account complete [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)

### Gettign started 
1. Create a Compute Cluster
   > Compute > Compute Cluster > + New -> Select Virtual machine
3. Create an envrionmemnt using the files attached
   > Environment > Custom Envionments > +Create -> Select form environment source -> Create a new docker context -> use zip file for the docker file and yaml file
4. Create the Scoring Script using the file attached
5. Register a model
   > Models > +Register -> from local files -> upload scoring script 
6. Create an Endpoint
   > Endpoints > Batch Endpoints > +Create -> Name it -> select your model -> select deployment name -> upload scoring script -> select environment -> select compute cluster
6. Add new Deployment
   > your endpoint > +Add deployment -> same steps as in '4. Create endpoint' (Take care to update the default deployment)

For more information go to [Get started woth Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/tutorial-azure-ml-in-a-day?view=azureml-api-2) and watch the first video for demonstration
### Connect demand planning with you Custom Model 

How to [ Use Custom Azure ML in Demand Planning](https://learn.microsoft.com/en-us/dynamics365/supply-chain/demand-planning/custom-azure-machine-learning-algorithms) is supposed to provide detailed documentation to connecting Demand Planning with your Custom ML in AzureML

1. Set up a third party App and Assign access to workspace and storage account
   > this steps are starting from [Azure Portal](https://ms.portal.azure.com/#home)
3. Connect to Azure ML Service from Demand Planning
   > the second video shows in detail where to find the information you need to connect demand planning with AzureML, use the documentation below as well
5. Set up a forecast using your Custom ML



As the maintainer of this project, please make a few updates:

- Improving this README.MD file to provide a great experience
- Updating SUPPORT.MD with content about this project's support experience
- Understanding the security reporting process in SECURITY.MD
- Remove this section from the README

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
