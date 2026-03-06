## **Problem Statement** <span id=_Tocopxhkk3stiwf></span>  
Current workflow configurations enforce a limit on the number of statements and connectors allowed within a tuple. Complex customer implementations frequently exceed this threshold, leading to design constraints, forced workarounds, and fragmented workflows.   
This restriction impacts scalability, maintainability, and adoption of advanced use cases.   
CustomerID :   
## **Proposed Solution** <span id=_Tocxj33lq5lxeyu></span>  
### **Overview** <span id=_Tocxv74be9t6lm5></span>  
Increase the allowable upper bound for statements and connectors within a workflow tuple by introducing configurable, performance-validated limits across the workflow stack (UI → API → DB) .   
The current and enhanced tuple limit is given below.   
|  **WF Statement/Connector** <br>|  **Default Limit** <br>|  **Enhanced Limit** <br>|
|----------|----------|----------|
|  Statement <br>|  100 <br>|  150 <br>|
|  Connector <br>|  250 <br>|  300 <br>|
  
  
This enhanced tuple limit will be applied only to the selected customers based on the required limit.   
## **Detailed Requirements** <span id=_Tocvgv5narh9m5h></span>  
* Application shall allow configuration up to  **\<new\\\_limit\\\_value\>**  tuples.   
	* CRUD operations of workflow and its performance must be ensured    
* Validation errors must reflect the updated threshold.   
* APIs must accept and process payloads within the new range.   
* UI must support creation/editing beyond old limits.   
* Proper error messaging if exceeding the new maximum.   
* Workflow PDF generation and execution must be ensured.   
* Other modes of WF Creation to be ensured   
	* **Sandbox**   
	* **Extension**   
	* OP-OD Migration   
	* DC Migration   
**_Design_**   
**_workflow.json \- Tuple limit added for statements and connectors as given below\._**   
[IMAGE]  
  
  
  
  
_Note : To Enable this new enhancement the below global config must be added for the app account._   
[IMAGE]  
## <span id=_Tocmn4i3fvut9hc>Test Cases </span>  
  
1. Workflow save (POST & PUT) with maximum number of statements with all statement types including the below configurations:   
	1. Notification and approval nodes with large description content   
	2. DRE custom functions in CF, If, Wait for, Timer nodes   
2. Duplicate workflow operation for the above workflow   
3. Workflow history for connectors for all type of source/target statements   
4. Above cases to be run in sandbox accounts and deployment also to be verified   
  
## <span id=_Tocj4od93slcqi5>API Test Cases </span>  
1. Start & end nodes must be present.   
2. Workflow must have at least one flow node.   
3. K ey field value of statements should be unique in a workflow.   
4. All nodes except start and end nodes must have a valid path from start node to end node.   
5. Target node of a connector cannot be start node. Source node of a connector cannot be end node.   
6. Error should be thrown when more than one flow node is present for the same status/stage.   
7. Workflow with duplicate connectors (more than one connector between the same source node-port and target node-port)   
8. At least one completed status node to be present, inactive status nodes cannot be present in request and problem workflows   
9. Submission & close stages must be present in Change & Release workflows .   
10. All connectors should have source and target statements and ports.   
11.   
