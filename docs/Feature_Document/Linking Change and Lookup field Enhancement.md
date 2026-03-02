# **CH-286 Linking Change Requests and UDF Lookup Enhancements** <span id=_Tocmcoowf9qejqe></span>  
  
#   
**Table of Contents** 

[Linking Change Requests ](#_Toc1luqbur0rlg7) 1 

[Lookup Field Enhancement for Change ](#_Tocb9yvkit5yvu3) 1 



  
# <span id=_Toc79dvb8xx36s5>  
# <span id=_Toc1luqbur0rlg7>**Linking Change Requests** </span>** ** </span></span>  
**Branch Name: ** [link](https://cmsuite.csez.zohocorpin.com/sdplive/code/SDPLIVE_LINKING_CHANGES_BRANCH/)   
**Change link: ** [link](https://sdpondemand.manageengine.com/app/sdpcloudissuemanager/ChangeDetails.cc?CHANGEID=187344000004645162&selectTab=submission&subTab=details)   
**UI Prototype** **:**   [Link](http://sdpod-ui/Prototypes_5/Linking%20Change%20Requests/)   
**_API Design Document_** **_:_** **_ _** **_[Link](https://writer.zoho.com/writer/open/mmxi26a3a01fd44174ae28dd3706dba579925)_**   
  
##### <span id=_Toctpklt1uzdywh>Requirement </span>  
  
The 'Linking Change' feature allows for linking changes in a parent-child relationship, enabling multiple child changes to be linked to a single parent change. This improves traceability and provides better visibility into changes related, with a linking option available on the Change.   
Change Requests need to be linked due to various requirements like   
* Stage Change Request to Production Change Request   
* Similar Changes like Anti Virus Patches on various Services/Asset   
* Phase by phase implementation of a large scale Change Request require linking of Change Requests.   
* Change Requests associated to each other having associated to a particular Release ( A parent Change Request associated to all related Change Requests ),   
* Dependent Change Requests   
* Duplicate Change Requests (if there are multiple change requests created to resolve a single problem, then these changes need to be associated) etc   
  
##### <span id=_Toc8obh1hhazuof>Quick Summary </span><span id=_Toc5e7djox5rswx></span>  
**Quick Summary ** \-  [CH-286](https://sdpondemand.manageengine.in/app/sdpcloudissuemanager/ChangeDetails.cc?CHANGEID=23128000007198740&selectTab=implementation&subTab=details)   
* Change Associations    
	* This feature enables parent-child relationships between change requests, significantly improving traceability and visibility. It's essential for managing related changes, like linking staging to production, grouping similar updates (e.g , antivirus patches), or orchestrating large-scale, multi-phase implementations.   
* How Linking Works    
	* This linking works in a  **non-hierarchical ** structure where a single parent change can have multiple child changes.    
		* A change can be either a parent or a child, but not both in the same relationship.    
	* Change linking is managed via a dedicated 'Association' tab on the Change Details Page.    
	* Changes can be attached or detached with appropriate permissions.    
		* Any user with edit permission for the current stage can associate a parent/child    
		* Once a change is closed, no additional changes can be linked or delinked to it.    
		* However, a closed change can still be linked or delinked from an open change.    
	* Comments can be added to association operations, which are then captured in the change history.    
	* Once a change is linked,    
		* In the Change List view, hovering over the linked change field displays the respective relationship in a tooltip.   
			* For a parent change, hovering over the field shows the child change count along with the relationship type.   
				* Clicking on the child change count opens the list of associated child changes.    
				* Only changes which are scoped to the user will be shown in popup.   
			* For a child change, hovering over the field displays the parent change ID and relationship type.   
				* Clicking on the parent change ID opens the parent change details in a popup.   
				* If user doesnt have scope for the change, an error will be thrown as "User does not have permission".   
		* In the Change Details Page, a badge will be shown along the title whether the current change is a Parent Change or Child Change.   
	* History can be filtered with the newly introduced linking changes operation.   
	* Change Closure Rules   
		* A mandatory closure rule has been introduced to ensure that all child changes are closed when the parent change is closed.   
		* This same rule can also be applied during manual workflow transitions under mandatory rules, allowing closure checks to be enforced before the transition takes place.   
* Rules and Restrictions    
	* The system prevents circular or hierarchical relationships (e.g.. A leading to B, and B leading to A, or A leading to B, which then leads to C).    
	* Each change can either have only one parent or 25 child changes. While existing links to trashed changes persist until disassociation or deletion, new associations with them are not permitted.   
  
##### <span id=_Tocifvhi3ocgkb4>Details </span>  
* **Change Details Page**   
	* Common Association Tab   
		* User can Link / Delink changes from Common Association Tab from LHS (In future all associations will be listed here)   
		* The Change details in the above section follow user scope.   
		* If the user does not have permission to view Parent Change or Child Changes, the count will be shown in RHS, but it won't be listed in the Associated Changes list view.   
	* RHS Association summary count   
		* A change can only be linked as parent change or child change but not both.   
		* If the change has no change associations -\>  **_'Linked Changes' with count as 0 in RHS Association section._**   
		* **_If the change has parent change associations -\> _** 'Linked  Parent Change' with count as 1 in RHS Association section. Trashed change count will not be counted.   
		* **_If the change has child_** **_ changes associations -\> _** **_'Linked _** Child Changes' with count in RHS  Association section.Trashed changes count will not be counted.   
	* **Change Linking:**   
		* Attach and Detach buttons will only be shown if the user has edit permission.   
		* In the Change association tab, Parent Change and Child Changes are available for linking.   
		* But either a Parent Change or Child Changes can be linked with a change.   
		* Target changes will be listed according to user view access permission.   
[IMAGE]  
	* **Child Change's Linking Page:**   
		* In the Child Change association tab, Parent Change is listed.   
		* A Child change will be having Child change tag in title.   
		* Parent Change can be delinked.    
		* On delinking the parent change, the Association tab will be reset, and both Child and Parent Changes are opened for linking.     
[IMAGE]  
  
	* **Parent Change's Association Page:**   
		* In the Parent Change's association tab, only Child Changes are listed.   
		* A Parent change will be having Parent change tag in title.   
		*  Limit for linking child changes is 25.   
		* Child Changes can be linked or delinked.   
		* On delnking all the Child Changes, the Association tab will be reset, and both Child and Parent Changes are opened for linking.   
  
[IMAGE]  
  
  
* **Change List View**   
	* **Linked Changes column is available in the change list view.**   
	* On clicking the  **_linked changes column _** in the list view of a parent change, all child changes of the change is listed.   
**Parent Change Tooltip:**   
[IMAGE]  
  
[IMAGE]  
	* On clicking the linked changes column of a child change in list view, the details popup of parent change will be shown.   
  
**Child Change Tooltip:**   
[IMAGE]  
[IMAGE]  
  
* <span id=_Toc251zb9cwrbt5>**History** </span>  
	* All Linking Change operations and the Link comments will be captured in history if a comment added.   
	* "Linked Changes" operations search filter will only get the related histories.   
###   
* <span id=_Tocahi1epjas7c8>**_Closure Rule_** </span>  
	* **Mandatory closure of all child changes before closing of Parent change is added.** [IMAGE]  
  
* **Workflow Transition **   
	* **A mandatory rule has been added in Change Workflow transition**   
[IMAGE]  
* <span id=_Tocblx6msa11hll></span>**Trash** ** Change** <span id=_Tocnb79n65d89y4></span><span id=_Tocks7582dyi2a1></span><span id=_Toc542fqebkt3dv></span>  
	* O <span id=_Toc29ueitfn1h8r>n trashing a Change, the trashed change will not be listed in the corresponding relationship list view.   
	* But on restoring the trashed change, the change relationships will also be restored.   
	* The changes which are in relationship with trashed change are allowed to associate to other changes   
		* Before that, a confirm popup will be shown for disassociation from trashed change.   
		* Note: The confirm popup will not be shown for a parent change on trying to associate a child change, whose child is trashed. So until the change is deleted, it cannot be removed from association.     
	* On deleting the trashed change, it will be removed from the corresponding relationship.  </span>  
  
* **List ** **View** ** Export**   
	* **Associated changes column will not be available in list view export**   
  
##### <span id=_Tocff5zlk6swlci>Scoping </span>  
* Access permission for performing  **_Linked_**  Changes   
	* Attach and Detach buttons will only be shown if the user has edit permission.   
	* Target changes will be listed according to user view access permission.   
	* Trashed changes will not be listed for linking,    
		* If already linked changes will not be removed from association.   
		* On further linking a change which is linked to a trashed change, a confirmation popup will be shown to remove the trashed change from linking.   
		* The trashed parent/child change count will not be shown in the summary count or in the association list view.   
		* On the restore of trashed change (if it is not removed from the linking) will be  **_linked_**  to the change in the corresponding relationship of before getting trashed.   
	* Deleted changes will be removed from the linking   
* But a trashed change will be showing both summary count in rhs and will list linked changes   
* Parent Change Linking [Association Type \- parent\_change\]   
	* This Linking can be made from the filters Open Changes and Closed Changes with the below criteria   
		* Linking allowed till the source change is closed. But the target change may or may not be closed.   
		* Constraints \- A Change cannot have more than one as its Parent Change\.   
* Child Changes Linking [Association Type \- child\_changes\]   
	* This Linking can be made from the filters Open Changes and Closed Changes with the below criteria   
		* Linking allowed till the source change is closed. **_But the target change may or may not be closed._**   
		* Constraints  :    
			* Child Changes have a client level limit of 25\. However a change with 25 child changes can be linked as parent from another change\[No API Restriction\] \.   
			* A Change can be linked as a Child Change to another Change, only if the Change is not as Child for any other Change.   
  
##### <span id=_Toc1y9g02y64b50>Linking  Constraints </span>  
  
An Explanation of the above requirement is given below:   
|  Example <br>|  Link <br>|  Description <br>|  Valid <br>|
|----------|----------|----------|----------|
|  1. <br>|  A<\-\-\--B <br><br>|  * B is Child Change to A. A is Parent Change of B <br><br>|  Allowed <br>|
|  2. <br>|  <br>A<\-\-\--B ,  A<\-\-\--C  <br>|  <br>	* B and C are Child Changes to A <br>	* A is Parent Change of B and C <br><br>|  <br>Allowed <br>|
|  3. <br>|  <br>A<\-\-\--C,  B<\-\-\-C <br><br>|  <br>	* C is Child Change to A and B <br><br>|  <br>Not allowed <br><br>|
|  4. <br>|  <br>A <\-\-\\- B, <br>B <\-\-\-A <br><br>|  <br>	* B is Parent Change of A <br>	* A is Parent Change of B <br><br>|  <br>Circular linking is not allowed <br><br>|
|  5. <br>|  A <\-\-\\- B,  <br>B <\-\-\\- C,  <br>C <\-\-\\- A <br>|  <br>	* B is Child Change to A <br>	* C is Child Change to B <br>	* A is Child Change  to C <br><br>|  <br>Circular linking is not allowed <br>|
|  6. <br>|  A<\-\-\--B<\-\-\-C <br>|  	* C is Child Change to B. B is Parent Change of C. <br>	* B is Child Change to A. A is Parent Change of B <br><br>|  Hierarchical linking is not allowed <br>|
  
  
##### API  Changes   
    
  
|  CHANGE TYPE <br>|  METHOD <br>|  API CALL <br>|  INPUT DATA <br>|
|----------|----------|----------|----------|
|  **_Parent Change_** <br>|  PUT <br>|  **_api/v3/changes/\<changeid\>/rel/parent_change_** <br>|  **_{"parent\_change":\[\{"parent\_change":{"id":\<target\_changeid\>}}]}_** <br>|
|  <br>|  DELETE <br>|  **_api/v3/changes/_** **_\<changeid\>_** **_/rel/parent_change?ids=_** **_\<changeid\>_** <br>|  - <br>|
|  Child Change <br>|  PUT  <br>|  **_api/v3/changes/\<changeid\>/rel/child_changes_** <br>|  **_{"child\_changes":\[\{"child\_changes":{"id":_** **_\<target\\\_changeid\\\_1\>_** **_}},{"child_changes":{"id":_** **_\<target\\\_changeid\\\_2\>_** **_}}]}_** <br>|
|  <br>|  DELETE <br>|  **_api/v3/changes/_** **_\<changeid\>_** **_/rel/child_changes?ids=_** **_\<changeids\>_** <br>|  - <br>|
  
  
* **_Sample API Call -\> Parent Change \\- PUT_**   
  
|  API CALL <br>|  Input Data <br>|  Response <br>|
|----------|----------|----------|
|  api/v3/changes/\<changeid\>/rel/parent_change <br>|  {"parent\_change":\[\{"parent\_change":{ <br>"id":\<target\_changeid\>}}]} <br>|  1. ```{ ```
<br>2. ```    "response_status": [ ```
<br>3. ```        { ```
<br>4. ```            "status_code": 2000, ```
<br>5. ```            "id": "100000000000045097", ```
<br>6. ```            "status": "success" ```
<br>7. ```        } ```
<br>8. ```    ], ```
<br>9. ```    "parent_change": { ```
<br>10. ```        "created_time": { ```
<br>11. ```            "display_value": "Nov 22, 2024 04:53 PM", ```
<br>12. ```            "value": "1732274596118" ```
<br>13. ```        }, ```
<br>14. ```        "comments": null, ```
<br>15. ```        "created_by": { ```
<br>16. ```            "email_id": "xxx@xyz.com", ```
<br>17. ```            "is_technician": true, ```
<br>18. ```            "sms_mail": null, ```
<br>19. ```            "mobile": "", ```
<br>20. ```            "last_name": "balaji", ```
<br>21. ```            "user\_scope": "internal\_user", ```
<br>22. ```            "sms\_mail\_id": null, ```
<br>23. ```            "cost\_per\_hour": "0", ```
<br>24. ```            "site": { ```
<br>25. ```                "deleted": false, ```
<br>26. ```                "name": "Base Site", ```
<br>27. ```                "id": "100000000000006784", ```
<br>28. ```                "is_default": true ```
<br>29. ```            }, ```
<br>30. ```            "phone": "", ```
<br>31. ```            "employee_id": null, ```
<br>32. ```            "name": "Har#", ```
<br>33. ```            "id": "100000000000040057", ```
<br>34. ```            "photo_url": "https://contacts.csez.zohocorpin.com/file?exp=10&ID=16172118&t=user&height=60&width=60", ```
<br>35. ```            "is\_vip\_user": false, ```
<br>36. ```            "department": null, ```
<br>37. ```            "first_name": "harish", ```
<br>38. ```            "job_title": null ```
<br>39. ```        }, ```
<br>40. ```        "last\_updated\_by": null, ```
<br>41. ```        "last\_updated\_time": null, ```
<br>42. ```        "id": "100000000000045097", ```
<br>43. ```        "child_changes": { ```
<br>44. ```            "display_id": { ```
<br>45. ```                "display_value": "CH-4", ```
<br>46. ```                "value": "4" ```
<br>47. ```            }, ```
<br>48. ```            "change_manager": null, ```
<br>49. ```            "id": "100000000000044286", ```
<br>50. ```            "title": "Firewall Failure" ```
<br>51. ```        }, ```
<br>52. ```        "parent_change": { ```
<br>53. ```            "display_id": { ```
<br>54. ```                "display_value": "CH-2", ```
<br>55. ```                "value": "2" ```
<br>56. ```            }, ```
<br>57. ```            "change_manager": null, ```
<br>58. ```            "id": "100000000000044256", ```
<br>59. ```            "title": "Firewall Upgrade" ```
<br>60. ```        } ```
<br>61. ```    } ```
<br>62. ```} ```
<br>|
  
  
  
##### MSP Cases   
1. A change can be  **_linked_**  with another change either in the Customer Org or MSP Org.   
2. In the association view, a customer filter is provided to choose the desired customer.   
3. When the customer is inactive, the association can be delinked from either change.   
4. **If the user doesn't have the view scope for the linked change, it will not be shown. But the summary count will be shown in RHS.**   
5. **Inactive Customer Changes are not available for linking. **   
  
  
##### Migration Details   
* **DATA Migration**  -   
	* RelationshipType &  ModuleRelationship data will be added   
	* Entries added for ChangeClosureRules table   
* **Zoho Analytics Migration \- ** Wil be catched up in later phases    
**Migration Steps **   
* Steps to do in  **Default branch**     
	*   META_DATA migration  Generate dd-changes.sql and use default Handler to do meta data upgrade.    
* Steps to do in the Feature Branch   
	* Step 1 :  Data Migration (Pre and Post release migration)   
		* **_[source/library/com/manageengine/sdpod/upgrade/isu/SDPSandboxUpgradeHandler.java](https://cmsuite.csez.zohocorpin.com/sdplive/SDPLIVE_LINKING_CHANGES_BRANCH/getdiff/?rev1=965f2c07d897&rev2=5cfa0ef64254&file=source/library/com/manageengine/sdpod/upgrade/isu/SDPSandboxUpgradeHandler.java)_**     
	* ~~Step 2 : ~~ MetaData Migration ~~** (Analytics)**~~   
		* ~~com.manageengine.sdpod.upgrade.isu.ZRUpgradeHandler  ~~   
  
##### <span id=_Tocyj2xyhv6fvqg></span>Support Tickets   
1. **_[#9208194](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24002446738969)_** **_  -\- Linking change as per _** **_following on the ITIL Processes._**   
2. **_#_** **_[7349847](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24001438921108)_** **_ \- Parent \- Child Template concept Changes made to the Parent Template should reflect on the child template \-\-\\\> Informed cx that it is not possible as of now\\\._**   
3. **_[#8580076](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24002048567809)_** **_  -\- Associating _** **_multiple changes to changes_**   
4. **_[#10248943](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24003006407838)_** **_ -\- _** **_association between Change Request with another Change Request_**   
5. **_#_** **_[11494717](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24003792802296)_** **_  -\- stages of development that we would reference one change with another change_**   
6. **_[#11385300](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24003702979029)_** **_ -\- Linking change option_**   
7. **_[#10913141](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24003387508385)_** **_ -\- To attach CR to another CR_**   
8. **_[#4805557](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24000429995219)_** **_ -\-  _** **_Associate additional CR to a single CR -\- 2018_**   
9. **_[#4769939](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24000417113095)_** **_ -\- In process of change some issue occur so need to create a new change and associate _**   
10. **_[#5206420](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24000615776066)_** **_ -\- initiate/link two CR's with the same SR _**   
11. **_[#5856854](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24000868954675)_** **_ -\- parent and child ticket concept in change management where Parent request should not be close unless and until all the child requests gets closed\._**   
12. **_[#6137389](https://pitstop.manageengine.com/agent/manageengine/servicedesk-plus-cloud/tickets/details/24000979258392)_** **_ -\- associate change ticket to change ticket_**   
  
  
  
---  
  
# <span id=_Tocb9yvkit5yvu3><span id=_Toc61tjktoscgm9>**Lookup Field Enhancement for Change ** </span></span><span id=_Tociey96eisdxq0></span>  
##### Requirement  <span id=_Toczjm9gtml6bg0>Summary </span>  
* **Asset and CMDB references are new supported for single lookup fields**   
* **Additional Field Lookup count is increased from 10 to 20.**   
	* **However, the limit will be increased only if the customer requests it via Global Config. **   
* **Limit for User Lookup is 6, which can be increased up to 10 via Global Config.**   
	* **For existing users, if the user has more than 6, they can continue to use the same, but new user lookups cannot be created**   
  
##### <span id=_Tocvt842wtoh26m>JSON Configuration changes </span>  
**Configuration changes are done in ** <u>**udftables.json**</u> ** , ** <u>**udf_field.json**</u> ** and ** <u>**lookupUDFfieldconf.json**</u>   
1. ** ** **udftables.json** ** : Limit introduced for REF type.**   
[IMAGE]  
2. **lookupUDFfieldconf.json ** **: Including asset and CMDB references for change lookup fields** [IMAGE]  
3. **udf_field.json** ** : user ref field with limits introduced**   
[IMAGE]  
  
**4\. Metadata changes** <span id=_Toc8jfifr845tw0></span>** \- ** **[Link](https://writer.zoho.in/writer/open/mmxi26a3a01fd44174ae28dd3706dba579925/bookmarks/toc_i6u2kqtzfv4u)**   
##### <span id=_Tocdun29phkt4dj>Global Config </span>  
  
* UDF\_ALLOCATION\_BUCKET.change.ref is used to increase limit of reference field from 10 to 20   
	* **_To increase the tuple limit for UDF REF_**   
		* **_Category:  TUPLE_LIMIT_**   
		* **_Parameter: UDF\_ALLOCATION\_BUCKET.change.ref_**   
		* **_Value: 15 (11 to 20 can be updated)_**   
* UDF\_ALLOCATION\_BUCKET.change.ref.user\_ref\_field_change is used to increase limit of user reference field from 6 to 10   
	* **To increase the tuple limit for UDF USER REF**   
		* Category:  TUPLE_LIMIT   
		* Parameter: UDF\_ALLOCATION\_BUCKET.change.ref. **_user\_ref\_field_change_**   
		* Value: 8 (7 to 10 can be updated)   
  
##### <span id=_Tocjrd4go43qfb0><span id=_Toctfy33a8pjp47></span></span>Areas to test <span id=_Tocyn7qzit3f04l></span>  
1. **All UDF types for change module.**   
2. **Template and Form**   
3. **Criteria components**   
	1. **Trigger criteria  **   
	2. **Timer abort criteria **   
	3. **Workflow condition nodes criteria **   
	4. **Form rules criteria**   
	5. **Custom menu criteria **   
	6. **Conflict detection criteria (User fields are not supported)**   
	7. **List view Filter criteria **   
	8. **Zoho Survey **   
		1. **Survey rule criteria**   
		2. **Survey exclusion criteria**   
4. **Form Rule Actions**   
	9. **Hide fields**   
	10. **Show fields**   
	11. **Enable fields**   
	12. **Disable fields**   
	13. **Mandate fields**   
	14. **Non mandate fields**   
	15. **Clear options**   
	16. **Add options**   
	17. **Remove options**   
	18. **Set Value**   
	19. **Clear value**   
5. **Notification $ variables: **   
	20. **However, if the $ variable is entered in the template manually, it will be resolved when notification is sent.**   
6. **User fields \-  user/technician/requester lookup fields can be selected in the following places**   
	21. **Notification action \- Notification users**   
	22. **Approval action \- Approvers **   
	23. **Workflow approval \- Approvers**   
	24. **Change status definition \- Notification users**   
	25. **Change status override \- Notification users**   
7. **Field Update Action**   
8. **Change closure rule fields **   
9. **Change history**   
10. **Custom reports**   
11. **Import/Export **   
12. **List view column chooser **   
13. **Sandbox**   
14. **Extension**   
15. **Audit Log        **   
16. **OP2OD            ** **→ OP does n** **ot support lookup fields. However, testing is required with UDFs in template, closure rules, default values, etc**   
17. **DC Migration ** **→ testing needed for change additional fields.**   
18. **MSP              **   
19. **Zoho Analytics**   
  
  
