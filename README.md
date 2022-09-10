# Adaptive Customer Service Through Data Analytics And AI

#### Problem Statement

If we consider the flow of a typical service helpdesk ticket, when a customer calls the helpdesk, the customer is connected with a support executive (aka FLS) who would log the helpdesk ticket (in case of new ticket) or provide the current status of the ticket (in case of existing open ticket). The FLS executive would then route the customer to a different support executive (SLS) who would either try to resolve the issue by themselves or re-route it to a different executive who may be able to help. This process would continue until the ticket reaches an executive who is actually able to resolve the issue.
Each such reassignment/routing to a SLS is called Tossing. With each tossing/reassignment cycle, the customer experience as well as satisfaction tends to drop significantly and tickets remain open for a longer period of time resulting in SLA breach. This poor customer experience while dealing with the helpdesk can also result in significant impacts to the organization in the form of:
• Increased MTTR
• SLA breach
• Increase in operational costs
• Unhappy customer leading to churn

#### Business Process Flow
##### Existing Flow
![image](https://user-images.githubusercontent.com/10474901/187494955-5f35b48a-2913-4fd2-a5e8-593f57e11c97.png)

##### Proposed Flow
![image](https://user-images.githubusercontent.com/10474901/187495066-121817e5-11a9-45f5-a88d-77d206eef4ee.png)

#### Objective of The Solution
The objective of the proposed solution is to build a framework using AI (Including NLP and ML) in order to ensure a pleasant, personalized conversational experience with the machine as well as a swift resolution of service helpdesk query by routing the incident to the correct support executive/group who would be able to resolve the issue without further reassignment/tossing in the first place. The resolution of incidents through minimal amount of tossing would lead to significant benefits like:
• Reduced MTTR
• Meeting SLAs
• Significant decrease in operational costs
• Significant improvement in terms of overall customer satisfaction
• Personalized conversational experience.

##### Proposed Solution Architecture
![image](https://user-images.githubusercontent.com/10474901/187495311-a6eae926-fb2c-4245-b4ba-ac6da6af57c4.png)

##### Process workflow for customer phone call in VoxImplantkit
![image](https://user-images.githubusercontent.com/10474901/187495538-db75bb69-e662-421f-8611-ee6840a8e6ee.png)

#### DB Setup (MySQL)
![image](https://user-images.githubusercontent.com/10474901/187301042-9de36aba-9922-4bfe-b2d6-cea7d8135eee.png)

#### File List

##### Dataset - /dataset
##### Trained Models - /output
##### Exploratory Data Analysis (EDA) - Incident_Analysis_Mozilla_Data_Analysis.ipynb
#### Model Building
##### Naive Bayes - Incident_Analysis_Mozilla_NB_RandomSearch.ipynb
##### SVM - Incident_Analysis_Mozilla_SVM_RandomSearch.ipynb
##### LR - Incident_Analysis_Mozilla_LR.ipynb
##### MLP - Incident_Analysis_Mozilla_NN_RandomSearch.ipynb
##### Other helper functions on DB interactions and internal logic for assignee prediction (including sentiment analysis) - /helper/helper.py and in the notebook helper.ipynb for testing dummy scenarios


