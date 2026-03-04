// $Id$
package com.zoho.automater.selenium.modules.changes.change.common;

import java.util.function.BiFunction;
import java.util.function.Function;

import org.openqa.selenium.By;

import com.zoho.crm.action.Locator;

public interface ChangeLocators {
	
	Function<String, Locator> SELECT_CHECKBOX_ENTITYID_CHANGE = (EntityId) -> new Locator(By.xpath("//*[@current_id='" + EntityId + "']/td/label/span[@class='sdpcustom-checkbox-value']"), "Select checkbox for the Change");
	
	interface ChangeListview {
		
		Locator FRAME_ZE_NOTIFICATION_MESSAGE = new Locator(By.xpath("//*[@class='ze_area wcag-focus-visible']"), "Editor Iframe");
		Function<String, Locator> CLICK_ROW_ACTIONS_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("//*[@data-row-id='" + EntityId + "']/descendant::span[@class='global-actions-ico']"), "Click row actions of change");
		Locator CLICK_ROW_ACTIONS_EDIT = new Locator(By.xpath("//div[@class='action-list']//descendant::a[text()='Edit']"), "Click Edit row actions of change");
		Locator CLICK_ROW_ACTIONS_DELETE = new Locator(By.xpath("//div[@class='action-list']//descendant::a[text()='Delete']"), "Click Delete row actions of change");
		Function<String, Locator> SELECT_CHECKBOX_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("//*[@data-row-id='" + EntityId + "']/td/label/span[@class='sdpcustom-checkbox-value']"), "Click the checkbox for change with entity id " + EntityId);
		Function<String, Locator> CLICK_VIEW_NOTES_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("// *[@data-row-id='" + EntityId + "']/descendant::span[contains(@class,'notesicon')]"), "Click the note for change with entity id " + EntityId);
		Function<String, Locator> CLICK_WORKFLOW_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("// *[@data-row-id='" + EntityId + "']/descendant::span[contains(@class,'workflow-ico')]"), "Click the workflow for change with entity id " + EntityId);
		Function<String, Locator> SELECTED_NOTE = (noteID) -> new Locator(By.xpath("//div[@note-id='" + noteID + "']/descendant::span[@class='requested-drop-arrow selected']"), "Selected note with id " + noteID);
		Function<String, Locator> SELECT_NOTE = (noteID) -> new Locator(By.xpath("//div[@note-id='" + noteID + "']/descendant::span[@class='requested-drop-arrow']"), "Select note with id " + noteID);
		Function<String, Locator> UI_NOTE_TEXT = (noteID) -> new Locator(By.xpath("//div[contains(@class,'notes-list atp-container')]"), "Note text created via UI with id " + noteID);
		Function<String, Locator> API_NOTE_TEXT = (noteID) -> new Locator(By.xpath("//div[@id='note_content_" + noteID + "']"), "Note text created via api with id " + noteID);
		Function<String, Locator> ROW_USING_ENTITYID = (entityID) -> new Locator(By.xpath("//table[@data-sdp-table-id='sdp-table']/tbody/tr[@data-row-id='" + entityID + "']"), "Row in list view using entityID");
		
		Locator BULK_SELECT_CHECKBOX = new Locator(By.xpath("//*[@data-column-index='0']/label"), "Check Box");
		
		Function<String, Locator> ACTIONS_LIST = (Action) -> new Locator(By.xpath("//div[@class='action-list']/descendant::a[text()='" + Action + "']"), "Actions Dropdown List");
		Locator VIEW_NOTES = new Locator(By.xpath("//*[@class='actionheader change_notesfield evenRow']"), "View Notes Icon from List View");
		Function<String, Locator> LISTVIEW_SEARCH_INPUT = (fieldName) -> new Locator(By.xpath("//div[@data-search-field-name='" + fieldName + "']/label/input"), "Searching values from the input");
		Locator CLICK_SEARCH_ICON = new Locator(By.xpath("//span[@title='Search']"), "Click search icon in requestlistview");
		Locator NEW_CHANGE_DROPDOWN = new Locator(By.xpath("//button[contains(@class,'new-inc-btn')]/descendant::span[@class='adrop']"), "");
		Locator NEW_CHANGE_BUTTON = new Locator(By.xpath("//button[contains(@class,'new-inc-btn')]/descendant::span[@class='adrop']/ancestor::button"), "");
		Locator CHANGE_REQUESTER_ICON_IN_FORM = new Locator(By.xpath("//div[@title='Search Requester List']"), "click change requester icon in form");
		
		Locator SELECT_RADIO_BTN_IN_POPUP = new Locator(By.xpath("//div[contains(@id,'sdppopupdiv')]/descendant::span[@class='sdpcustom-radio-value']"), "click radio btn in poopup");
		Locator CLICK_SAVE_BUTTON_USING_SUBMIT = new Locator(By.xpath("//div[contains(@class,'ui-dialog ui-widget')]/descendant::div/button[@name='submit']"), "click save button in popup using submit");
		
		Function<String, Locator> VERIFY_USER = (mailid) -> new Locator(By.xpath("//li[@data-fieldrefname='change_requester']/descendant::span[contains(text(),'" + mailid + "')]"), "Actions Dropdown List");
		
		Function<String, Locator> SELECT_FILTER = (filters) -> new Locator(By.xpath(("//span[contains(@class, 'requestnameanc') and text() = '" + filters + "']")), "select filters");
		
		Function<String, Locator> SELECT_EXPORT_OPTIONS = (exportOptions) -> new Locator(By.xpath("(//input[@value='" + exportOptions + "']/following-sibling::span[@class='sdpcustom-radio-value'])[last()]"), "select export options in popup");
		
		Locator VERIFY_SELECTED_DATA_OPTIONS_DISABLED_IN_EXPORT = new Locator(By.xpath("//input[@value='selected-data' and @disabled]"), "verify selected data is disabled in export popup");
		
		Locator SELECT_ALL_CHECKBOX = new Locator(By.xpath("//th/label/span[@class='sdpcustom-checkbox-value']"), "select all checkbox in listview");
		
		Locator CLICK_ADD_DOWNTIME_IN_CHANGE_FORM = new Locator(By.xpath("//button[contains(text(),'Add Downtime')]"), "add downtime");
		
		Locator VERIFY_ADD_DOWNTIME_BTN_DISABLED = new Locator(By.xpath("//button[contains(text(),'Add Downtime')]"), "click/verify add downtime btn");
		
		Locator VERIFY_ADD_DOWNTIME_HOVER_TEXT = new Locator(By.xpath("//div[contains(@class,'new-dialog opacity-in new-dialog-theme-default')]"), "verify add downtime hover text");
		
		Locator SEARCH_TEMP_IN_REQUESTER_LOGIN = new Locator(By.xpath("//input[@id='changeTemplateSearch']"), "search temp in req login");
		
		BiFunction<String, String, Locator> VERIFY_STATUS_IN_LISTIVEW = (entityId, status) -> new Locator(By.xpath("//tr[@data-row-id='" + entityId + "']/descendant::td[@title='" + status + "']"), "verify status in listview");
		
		Function<String, Locator> VERIFY_FIELD_NAME_IN_POPUP = (fieldName) -> new Locator(By.xpath("//div[contains(@class,'change-header-details')]/descendant::*[@class='field-label'][contains(text(),'" + fieldName + "')]"), "verify field name in popup");
		
		Function<String, Locator> TITLE_NAME = (titleName) -> new Locator(By.xpath("//h1[contains(text(),'" + titleName + "')]"), "verify title name");
		
		Locator VERIFY_ROLES_ICON_IN_CHANGELISTVIEW = new Locator(By.xpath("//*[@class='roles-listview-icon']"), "verify roles icon in change listview");
		
		Locator VERIFY_ROLES_AND_ASSIGNED_USERS_IN_CHANGELISTVIEW = new Locator(By.xpath("//*[@class='new-dialog roles-association pointer']"), "verify roles and assigned users in change listview");
		
		Locator REMOVE_HASH_REQUEST_ID = new Locator(By.xpath("//td[@data-sdplayoutid='display_id']/span"), "change id");
		
		Locator DATAEXP = new Locator(By.xpath("//span[@role='button' and @sdptitles='Data Export']"), " export");
		
		Locator EXPNOTIFICATION = new Locator(By.xpath("//h4[@class='f-h4 states-notif']"), "export verification");
		
		Locator DELETE_EXP_NOTIFCATION = new Locator(By.xpath("//a[@data-action='deleteNotify']"), "delete export notification");
		
		Function<String, Locator> TRASH_FILTER = (trashFilter) -> new Locator(By.xpath("//a[contains(@title, '" + trashFilter + "')]"), "Trash from Listview filters");
		
		Locator CLICK_LISTVIEW_FILTERS = new Locator(By.xpath("//span[@class='requestnamecss']/descendant::span[@class='requestnameanc']"), "click Requests Listview Filters");
		
		Function<String, Locator> CHECKLIST_DROP_DRAG = (item) -> new Locator(By.xpath("//span[contains(text(),'" + item + "')]"), "Drop Field in Checklist");
		
		Function<String, Locator> CONFLICT_ALERT_BUTTON = (button) -> new Locator(By.xpath("//span[@class='ui-button-text' and contains(text(),'" + button + "')]"), "Conflict Alert Button");
		
		Locator CHANGE_REQUESTER_FIELD = new Locator(By.xpath("//li[@data-fieldrefname='change_requester']"), "Requester Field in request form");
		
		Locator SEARCH_CIS_INVOLVED = new Locator(By.xpath("//div[@class='field-picker configuration_item']"), "");
		
		Function<String, Locator> CLICK_ENTITY = (Id) -> new Locator(By.xpath("//div[contains(text(),'" + Id + "')]"), "");
		
		Function<String, Locator> VIEW_TYPE = (viewType) -> new Locator(By.xpath("//li[@title='" + viewType + "']"), "changeto listview or templateview");
		
		Function<String, Locator> LISTVIEW_FILTER_NAME = (filterName) -> new Locator(By.xpath(("//span[contains(@class, 'requestnameanc') and text() = '" + filterName + "']")), "select filter name");
		
		Locator IFRAME_APPROVAL_RHS = new Locator(By.xpath("//div[@class='field-picker configuration_item']"), "");
		
		Locator TRASH_DETAILS_VIEW = new Locator(By.xpath("//a[@class='popout-icon msteams-dashboard-hide' and text()='View Details']"), "verify roles icon in change listview");
		
		Locator DELETE_CHANGE = new Locator(By.xpath("//button[text()=' Delete ']"), "delete change in change listview");
		
		Function<String, Locator> LISTVIEW_DISPLAY_ID = (displayid) -> new Locator(By.xpath(("//td[@class='evenRow' and @title='CH-" + displayid + "']")), "Locate Display ID from List View");
		
	}
	
	interface ChangeDetailsview {
		
		Locator CAB_NAME = new Locator(By.id("name"), "");
		
		Locator ADD_APPROVAL_LEVEL_NAME = new Locator(By.xpath("//div[@class='sdp-layout-input']/descendant::input[@id='name']"), "Add Approval level name locator");
		
		Locator ADD_APPROVAL_ABORT_MSG = new Locator(By.xpath("//div[contains(@class,'system-error')][@role='alert'][text()]"), "Add Approval level name cbr abort message");
		
		Locator CHANGE_ID_TXT = new Locator(By.xpath("//td[@data-sdplayoutid='display_id']/descendant::span"), "Get Change ID");
		
		Locator TASK_ACTION_BTN = new Locator(By.xpath("//td/span[@class='global-actions-ico']"), "TASK ACTION BTN");
		
		Locator TASK_CHANGE_STAGE = new Locator(By.id("s2id_change_stage"), "select change stage in task select field");
		
		Locator NOTES_TEXT = new Locator(By.xpath("//div[@class='conversion-open-thread']/descendant::div[contains(@class,'conversation-info')]"), "Get Notes Text");
		
		Locator NOTES_EDIT_BTN = new Locator(By.xpath("//div[@class='conversion-open-thread']/descendant::div[contains(@class,'con-action-box')]/descendant::span[@title='Edit Note']"), "Notes Edit Btn");
		
		Locator ATTACHMENT_ICON = new Locator(By.xpath("//span[contains(@id,'changesFileAttachments')]/descendant::div[@class='basic-attach']"), "ATTACHMENT ADD Btn");
		
		Function<String, Locator> ATTACHMENT_FILE_NAME = (mode) -> new Locator(By.xpath("//*[@data-viewmode='" + mode + "']//span[@class='sdattach-filename']"), "Get name for the Attached file");
		
		Function<String, Locator> FILE_INPUT = (mode) -> new Locator(By.xpath("//*[@data-viewmode='" + mode + "']//input[@id='AttachBtn']"), "");
		
		Function<String, Locator> CLICK_ATTACHMENT_ICON = (viewmode) -> new Locator(By.xpath("//*[@data-viewmode='" + viewmode + "']//*[@class='basic-attach']"), "click " + viewmode + " attachment icon");
		
		Locator ATTACHMENT_COUNT_DETAILS = new Locator(By.xpath("//*[@data-viewmode='detailview']//span[@class='num-attach']"), "Get Attachment count in detailsview");
		
		Function<String, Locator> CLICK_RHS_FIELD_DROPDOWN = (field) -> new Locator(By.xpath("//*[contains(@class,'sdp-layout-field') and @data-fieldrefname='" + field + "']/descendant::div[@class='sdp-layout-input']/descendant::a[@class='select2-choice']"), "click " + field + " dropdown");
		
		Locator STATUS_COMMENT = new Locator(By.xpath("//span[contains(text(),'Status Comments')]/span"), "Get status comments ");
		
		Function<String, Locator> LHS_SUBTAB = (tab) -> new Locator(By.xpath("//div[contains(@class,'tab-text')]/ancestor::a[@data-tabname='" + tab + "']"), "Click " + tab + " in lhs");
		
		Locator GO_BACK = new Locator(By.xpath("//button[@sdp-event-ref='goBack']"), "Click back button");
		
		Function<String, Locator> SPOT_EDIT = (fieldName) -> new Locator(By.xpath("// span[@class='sdp-field-label' and contains(text(),'" + fieldName + "')]/parent::div/following-sibling::div/descendant::a"), "Click/verify spot edit field " + fieldName);
		
		Function<String, Locator> SPOT_EDIT_ASSET = (fieldName) -> new Locator(By.xpath("//span[@class='sdp-field-label' and contains(text(),'" + fieldName + "')]/parent::div/following-sibling::div/descendant::a/span[3]"), "Click/verify spot edit field " + fieldName);
		
		Locator ADDED_TASKS = new Locator(By.xpath("//div[contains(@class,'task-list-template-view')]/descendant::h2/a"), "Verify/Click added task from the task subtab");
		
		// Stages
		Function<String, Locator> STAGES = (stage) -> new Locator(By.xpath("//div[contains(@class,'details-lhs-section')]/descendant::a[@data-stage='" + stage + "']"), "Click/verify Stage" + stage);
		
		// Verify Stages opened
		Function<String, Locator> VERIFY_STAGES_OPENED = (fieldName) -> new Locator(By.xpath("//h2[contains(text(),'" + fieldName + "')]"), "verify Stages Name in the middle container" + fieldName);
		
		Function<String, Locator> PLANNING_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//h2[contains(text(),'" + fieldName + "')]"), "verify Details subtab in Planning Stages" + fieldName);
		
		// click Plus icon
		Function<String, Locator> CLICK_PLUS_ICON = (fieldName) -> new Locator(By.xpath("//div[contains(@class,'" + fieldName + "')]/descendant::*[contains(@class,'plus-icon')]"), "Click Plus icon in Details subtab in Planning Stages" + fieldName);
		
		Function<String, Locator> EXPAND_FIELDNAME_IN_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//*[@title='" + fieldName + "']"), "expand Details subtab in Planning Stages");
		
		// Verify added details
		Function<String, Locator> VERFIY_ADDED_TEXT_IN_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//span[contains(@data-sdplayoutfieldid,'" + fieldName + "')]"), "Verify Added text in Details subtab in Planning Stages" + fieldName);
		
		// Edit icon in details subtab
		Function<String, Locator> CLICK_EDIT_ICON_IN_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//div[contains(@class,'" + fieldName + "')]/descendant::*[@class='stage-planning-edit']"), "click edit icon in Details subtab in Planning Stages" + fieldName);
		
		// Verify Edited text in Details Suubtab
		Function<String, Locator> VERFIY_EDITED_TEXT_IN_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//div[contains(@data-fieldrefname,'" + fieldName + "')]"), "verify edited text in Details subtab in Planning Stages" + fieldName);
		
		// Expand / Collapsed Details subtab
		Function<String, Locator> EXPANDED_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//span[contains(@class,'fright pointer') and contains(text(),'" + fieldName + "')]"), "Expanded Details subtab in Planning Stages" + fieldName);
		
		// Verify not available
		Locator VERIFY_NOT_AVAILABLE_DETAILS_SUBTAB = new Locator(By.xpath("//span[contains(@class,'sdp-layout-input')]/descendant::div[contains(text(),'Not available')]"), "verify not available text in Details subtab in Planning Stages");
		
		BiFunction<String, String, Locator> PLANNING_DETAILS_BI_FUNCTION = (subTab, desc) -> new Locator(By.xpath("//*[@data-sdplayoutfieldid='" + subTab + "']/descendant::div[contains(text(),'" + desc + "')]"), "");
		
		// expand or collapse
		Function<String, Locator> EXPAND_COLLAPSE_DETAILS_SUBTAB = (fieldName) -> new Locator(By.xpath("//div[contains(@class,'" + fieldName + "')]/descendant::div[contains(@class,'collapsearrow')]"), "Expand / collapse Details subtab in Planning Stages" + fieldName);
		
		// RHS Associations
		Function<String, Locator> RHS_ASSOCIATIONS = (fieldName) -> new Locator(By.xpath("//div[contains(@class,'rhs-associations')]/descendant::a[contains(text(),'" + fieldName + "')]"), "RHS - Associations" + fieldName);
		
		// verify association tab is opened for request in implementation stage
		Locator VERIFY_ASSOCIATIONS_TAB_OPENED_REQUEST = new Locator(By.id("change_associations_initiated_requests"), "Verify associations subtab opened in the implementation stage for associate request");
		
		// verify association tab is opened for problems in implementation stage
		Locator VERIFY_ASSOCIATIONS_TAB_OPENED_PROBLEMS = new Locator(By.id("ShowAssociatedProblems_CT"), "Verify associations subtab opened in the implementation stage for associate problems");
		
		// verify association tab is opened for projects in implementation stage
		Locator VERIFY_ASSOCIATIONS_TAB_OPENED_PROJECTS = new Locator(By.id("AssociatedProjects_CT"), "Verify associations subtab opened in the implementation stage for associate projects");
		
		// verify association tab is opened for release in implementation stage
		Locator VERIFY_ASSOCIATIONS_TAB_OPENED_RELEASE = new Locator(By.id("change_associations_releases"), "Verify associations subtab opened in the implementation stage for associate release");
		
		// click attach button in Request caused by change in association subtab in implementation
		
		Function<String, Locator> ATTACH_DETACH_REQUEST = (fieldName) -> new Locator(By.xpath("//div[@id='change_associations_initiated_requests']/descendant::button[contains(text(),'" + fieldName + "')]"), "Attach / detach Request caused by change" + fieldName);
		
		// click attach button in Request initiated change in association subtab in planning
		
		Function<String, Locator> ATTACH_DETACH_REQUEST_INITIATED_CHANGE = (fieldName) -> new Locator(By.xpath("//div[@id='change_associations_initiated_by_requests']/descendant::button[contains(text(),'" + fieldName + "')]"), "Attach / detach Request initiated by change" + fieldName);
		
		// click attach button in associate problem in association subtab under planning
		
		Function<String, Locator> ATTACH_DETACH_PROBLEM = (fieldName) -> new Locator(By.xpath("//div[@id='Problem']/descendant::button[@data-refid='" + fieldName + "']"), "Attach / detach Problem" + fieldName);
		
		// click attach button in project casued by change in association subtab under implementation
		
		Function<String, Locator> ATTACH_DETACH_PROJECTS_CAUSED_BY_CHANGE = (fieldName) -> new Locator(By.xpath("//div[contains(@id,'change_associations_initiated_projects')]/descendant::button[contains(text(),'" + fieldName + "')]"), "Attach / detach Projects" + fieldName);
		
		Function<String, Locator> ATTACH_DETACH_PROJECTS_THAT_INITIATED_CHANGE = (fieldName) -> new Locator(By.xpath("//div[contains(@id,'change_associations_initiated_by_project')]/descendant::button[contains(text(),'" + fieldName + "')]"), "Attach / detach Projects" + fieldName);
		
		Function<String, Locator> ATTACH_DETACH_RELEASE = (fieldName) -> new Locator(By.xpath("//div[contains(@id,'releases')]/descendant::button[@data-refid='" + fieldName + "']"), "Attach / detach Release" + fieldName);
		
		Locator CLICK_CHANGE_RHS_STATUS = new Locator(By.xpath("//div[@class='rhs-section']/descendant::td[@data-sdplayoutid='status']"), "click to to open dropdown change RHS status in detailview");
		
		Function<String, Locator> VERIFY_CHANGE_RHS_STATUS = (fieldName) -> new Locator(By.xpath("//td[@data-sdplayoutid='status']/descendant::span[@title='Status - Approved']"), "Verify Change RHS Status" + fieldName);
		
		Function<String, Locator> PLANNING_SUBTAB = (fieldName) -> new Locator(By.xpath("//li[@title='" + fieldName + "']/a"), "Planning Subtabs" + fieldName);
		
		Locator CLICK_SAVE_BUTTON_USING_SUBMIT = new Locator(By.xpath("//div[contains(@class,'ui-dialog ui-widget')]/descendant::div/button[@name='submit']"), "click save button in popup using submit");
		
		// Cab Evaluation
		
		Function<String, Locator> LHS_STAGES_SUBTABS = (fieldName) -> new Locator(By.xpath("//li[@data-sdptabid='" + fieldName + "']/a"), "LHS Stages" + fieldName);
		
		Locator VERIFY_APPROVALS_NOT_ADDED_TEXT = new Locator(By.xpath("//div[contains(text(),'Approvals are yet to be added through workflow.')]"), "Verify Approvals are yet to be added through workflow Text in approvals subtab when no approvals configured");
		
		Locator VERIFY_NO_APPROVAL_CONFIGURED_TEXT = new Locator(By.xpath("//div[contains(text(),'No approval configured')]"), "Verify No Approvals Configured");
		
		// Locator BTN_ADD_CAB_MEMBER = new Locator(By.xpath("//button[contains(text(),'Add CAB Member')]"), "Click Add CAB Member");
		
		Locator BTN_ADD_APPORVAL_LEVEL = new Locator(By.xpath("//button[contains(text(),'Add Approval Level')]"), "Click Add approval level");
		
		Locator CLICK_SELECT_CAB_DROPDOWN = new Locator(By.xpath("//div[contains(@class,'select2-container flat-select')]/a"), "Click select CAB dropdown in popup");
		
		Locator CLICK_SELECT_CAB_MEMBERS_DROPDOWN = new Locator(By.xpath("//li[@class='select2-search-field']/input"), "Click select CAB Members dropdown in popup");
		
		Locator CLICK_SAVE_IN_POPUP = new Locator(By.xpath("//input[@title='Save']"), "click save in popup");
		
		Locator VERIFY_CAB_MEMBERS_ADDED = new Locator(By.xpath("//div[@class='stage-open-thread']/descendant::table[contains(@class,'tableComponent')]/descendant::td[1]"), "verify cab members added");
		
		Locator CLICK_STAGE_DROPDOWN = new Locator(By.xpath("//div[@id='s2id_stage']/a"), "click stage dropdown in rhs");
		
		Locator CLICK_STATUS_DROPDOWN = new Locator(By.xpath("//div[@id='s2id_status']/a"), "click status dropdown in rhs");
		
		Function<String, Locator> BUTTONS = (fieldName) -> new Locator(By.xpath("//button[contains(text(),'" + fieldName + "')]"), "Click / verify Buttons" + fieldName);
		
		Locator VERIFY_PENDING_APPROVAL_STATUS = new Locator(By.xpath("//div[@class='stage-open-thread']/descendant::div[contains(text(),'Pending Approval')]"), "verify Pending Apporoval Status");
		
		// uat
		Locator CLICK_DESCRIPTION_PLUS_ICON = new Locator(By.xpath("//div[contains(@data-sdplayoutlabelid,'description')]/descendant::span[contains(@class,'plus-icon')]"), "click plus/add icon in description");
		
		Locator CLICK_DESCRIPTION_EDIT_ICON = new Locator(By.xpath("//div[contains(@data-sdplayoutlabelid,'description')]/descendant::span[contains(@class,'write-ico')]"), "click edit icon in description");
		
		Locator VERIFY_DESCRIPTION_IN_DETAILS_SUBTAB = new Locator(By.xpath("//span[contains(@data-sdplayoutfieldid,'description')]/descendant::div[@sdpdisplaytype='html']"), "Verify description in details subtab in stages");
		
		Function<String, Locator> CLICK_NOT_CONFIGURED_IN_DATE_FIELD = (fieldName) -> new Locator(By.xpath("//span[@data-sdplayoutfieldid='" + fieldName + "']/a"), "click not configured for date field");
		
		Locator NOT_CONFIG_DATE = new Locator(By.xpath("//*[contains(@data-fieldrefname,'release_details-release_scheduled_start')]/descendant::span[@data-sdplayoutfieldid='release_details-release_scheduled_start']"), "");
		
		Function<String, Locator> VERIFY_RELEASE_TITLE_IN_CHANGE_ASSOCIATION = (fieldName) -> new Locator(By.xpath("//td[contains(text(),'" + fieldName + "')]"), "verify release title" + fieldName);
		
		// RHS
		Locator ATTACHMENT_COUNT = new Locator(By.xpath("//span[@id='changes-attachcount']"), "Get Attachment count and Addattachment");
		
		Locator ATTACHMENT_IN_FORM = new Locator(By.xpath("//div[@class='basic-attach']"), "");
		
		Locator ATTACHMENT_IN_RHS = new Locator(By.xpath("//div[@id='change_attachments_rhs']/descendant::*[@class='basic-attach']"), "");
		
		Function<String, Locator> CLICK_PROJECT_TITLE_IN_PROJECT_CAUSED_BY_CHANGE = (fieldName) -> new Locator(By.xpath("//*[@title='" + fieldName + "']/ancestor::div[@id='change_associations_initiated_projects']/descendant::td//span[@class='sdpcustom-checkbox-value']"), "verify/click project title" + fieldName);
		
		Function<String, Locator> VERIFY_PROJECT_TITLE_IN_PROJECT_INITIATED_BY_CHANGE = (fieldName) -> new Locator(By.xpath("//div[@id='change_associations_initiated_by_project']/descendant::td[@title='" + fieldName + "']"), "verify/click project title" + fieldName);
		
		Function<String, Locator> VERIFY_APPROVAL_LEVEL_NAME_IN_STAGES = (approvalLevelName) -> new Locator(By.xpath("//td/descendant::span[@title='" + approvalLevelName + "']"), "verify approval level name");
		
		BiFunction<String, String, Locator> CLICK_APPROVE_OR_REJECT = (approvalLevelName, status) -> new Locator(By.xpath("//span[@title='" + approvalLevelName + "']/ancestor::td[2]/descendant::a[contains(text(), '" + status + "')]"), "approve or reject");
		
		BiFunction<String, String, Locator> CLICK_DELETE_APPROVAL = (approvalLevelName, status) -> new Locator(By.xpath("//span[@title='" + approvalLevelName + "']/ancestor::div[@class='stage-open-thread']/descendant::div[contains(@class,'responseframe')]/descendant::span[@class='delete-ico']"), "approval delete icon");
		
		BiFunction<String, String, Locator> VERIFY_APPROVED_OR_REJECTED_STATUS = (approvalLevelName, status) -> new Locator(By.xpath("//span[@title='" + approvalLevelName + "']/../../preceding-sibling::tr/descendant::span[text() = '" + status + "']"), "verify approved status");
		
		BiFunction<String, String, Locator> VERIFY_APPROVAL_LEVEL_COMMENTS = (approvalLevelName, comments) -> new Locator(By.xpath("//span[@title='" + approvalLevelName + "']/ancestor::td[2]/descendant::div[contains(text(), '" + comments + "')]"), "verify approval level comments");
		
		BiFunction<String, String, Locator> VERIFY_APPROVAL_RULE_NAME_IN_STAGES = (ruleName, status) -> new Locator(By.xpath("//span[contains(text(), '" + ruleName + "')]/../preceding-sibling::div/descendant::span[text() = '" + status + "']"), "verify rule name in approval level stages");
		
		Locator VERIFY_APPROVAL_LEVEL_2_IN_STAGES = new Locator(By.xpath("//div[@class='stage-info'][text() = 'Level - 2']"), "verify approval level number");
		
		Locator SWITCH_TO_PRINT_FRAME = new Locator(By.xpath("//*[@name='PreviewFrame']"), "switch to print Iframe popup");
		
		Locator VERIFY_PRINT_FORM_LOADED = new Locator(By.xpath("//div[@id='changeDetailsDiv']"), "verify print form loaded");
		
		Locator VERIFY_NO_DATA_PRESENT_IN_PRINT_FORM = new Locator(By.xpath("//div[@id='changeDetailsInnerDiv']"), "verify no data present ");
		
		Function<String, Locator> UNCHECK_RHS_PRINT_PREVIEW = (sectionName) -> new Locator(By.xpath("//label[@title='" + sectionName + "']"), "verify section name");
		
		Function<String, Locator> VERIFY_SECTION_NAME_NOT_PRESENT_PRINT_PREVIEW = (sectionName) -> new Locator(By.xpath("//h1[contains(text(),'" + sectionName + "')]"), "verify section name");
		
		Locator VERIFY_CHANGE_DETAILS_VERIFY_NOT_VERIFY_IN_PRINT_FORM = new Locator(By.xpath("//*[@class='details-title']"), "verify change details data present ");
		
		Locator CLICK_VERIFY_ARCHIEVED_INCIDENTS = new Locator(By.xpath("//span[@id='archive_request_filter']"), "click/verify Archived incidents in associations subtab");
		
		Function<String, Locator> ASSOCIATED_REQUEST_CAUSED_IN_CHANGE = (option) -> new Locator(By.xpath("//tr[@data-row-id='" + option + "']"), "");
		
		Function<String, Locator> TABLE_SETTINGS_IN_ASSOCIATION = (associationName) -> new Locator(By.xpath("//div[@id='" + associationName + "']/descendant::div[@data-sdp-table-id='sdp-table-list-settings']"), "");
		
		Locator CHANGE_APPROVELS_DELETE_ICON_LOCATOR = new Locator(By.xpath("//span[@title='Delete Approval']"), "Change approvels delete icon locator");
		
		Function<String, Locator> CHANGE_DOWNTIME_ACTIONS_LOCATOR = (name) -> new Locator(By.xpath("//td[@title='" + name + "']/parent::tr/td/span[@class='global-actions-ico']"), "");
		
		Locator VERIFY_CHANGE_DETAILS_POPUP_OPENED_FROM_LISTVIEW = new Locator(By.xpath("//iframe[@id='change-details-popup']"), "verify change details popup opened from listview");
		
		Locator CLICK_CAB_APPROVAL = new Locator(By.xpath("//*[@title='CAB Approval']"), "click cab approval in popup opened from listview");
		
		Locator CLICK_STATUS_DROPDOWN_IN_POPUP = new Locator(By.xpath("//div[@id='s2id_status-drop-down']"), "click status dropdown in popup opened from listview");
		
		Locator TYPE_STATUS_TEXTAREA = new Locator(By.xpath("//textarea[@id='status-comment']"), "type comments in popup opened from listview");
		
		Locator CLICK_SAVE_BUTTON_USING_ID_SUBMIT = new Locator(By.xpath("//div[contains(@class,'ui-dialog ui-widget')]/descendant::div/button[@id='submit']"), "click save button in popup using submit");
		
		Locator SCHEDULER_BUTTON = new Locator(By.xpath("//button[contains(text(),'Scheduler')]"), "scheduler button in detailspage");
		
		Function<String, Locator> SCHEDULER_PAGE_CHANGE_ID = (value) -> new Locator(By.xpath("//div[@id='ElementMark']/descendant::a[@data-id='" + value + "']"), "Change ID in scheduler page");
		
		Function<String, Locator> CLICK_SPOT_EDIT_DROPDOWN = (value) -> new Locator(By.xpath("//*[contains(@id,'" + value + "')]/descendant::a"), "click spotedit dropdown");
		
		Locator SCHEDULE_EDIT = new Locator(By.xpath("//span[@title='Edit Planning Schedule']"), "Click Edit Option or schedule");
		
		Function<String, Locator> SELECT_CHECKBOX_USING_NAME = (name) -> new Locator(By.xpath("//td[@title='" + name + "']"), "select checkbox using CMDB name");
		
		Locator VERIFY_ASSOCIATIONS_TAB_OPENED_CHANGES_CAUSED_BY_PROJECT = new Locator(By.id("initiated_changes_listView"), "Verify associations subtab opened for associate changes caused by project");
		
		Function<String, Locator> DETAILVIEW_ACTIONS_DROPDOWN = (actionsName) -> new Locator(By.xpath("//div[@id='quickactiondiv']/descendant::a[text()='" + actionsName + "']"), "Click the Actions dropdown field");
		
		Locator NOTIFICATION_TO_FIELD = new Locator(By.id("TO_FIELD"), "");
		
		Locator GOBACK_BUTTON_LOCATOR = new Locator(By.xpath("//button[@title='Go back']"), "go back button in the details view");
		
		Locator CLICK_VERIFY_RECENT_INCIDENTS = new Locator(By.xpath("//span[@id='active_request_filter']"), "click/verify Active incidents in associations subtab");
		
		Locator BTN_ATTACH_INCIDENT = new Locator(By.xpath("//div[@id='problem_associations_requests']/descendant::button[contains(text(),'Attach')]"), "Attach button locator in Associate Incident");
		
		Locator BTN_DETACH_INCIDENT = new Locator(By.xpath("//div[@id='problem_associations_requests']/descendant::button[contains(text(),'Detach')]"), "Detach button locator in Associate Incident");
		
		Function<String, Locator> DEPENDENCY_NODE = (EntityId) -> new Locator(By.xpath("//*[@id='" + EntityId + "']/parent::*[@class='node']/descendant::*[@id='rectNode']"), "Task node in Task Dependency page");
		
		Locator BTN_CLOSEDEPENDENCY = new Locator(By.xpath("//span[@class='close-icon-min']"), "Close icon in Task Dependency page");
		
		Function<String, Locator> ENABLE_CHECKBOX_CHANGE_ATTACHED_WITH_DISPLAY_ID = (DisplayId) -> new Locator(By.xpath("//td[@title='" + DisplayId + "']/preceding-sibling::td/label/span"), "");
		
		Locator IFRAME_NOTIFICATION = new Locator(By.xpath("//div[@class='tb-slide-details'] [@data-errorstate='false']/iframe[@class='tb-iframe']"), "switch IFrame Approval notification");
		
		Locator POPU_OUT_ICON = new Locator(By.xpath("//a[@class='tb-slide-popout popout-icon'][contains(@href,'ChangeDetails')][@route='true']"), "popuout icon in LHS");
		
		Locator VIEW_DETAILS_ICON = new Locator(By.xpath("//*[@id='changeDetailsInnerDiv']/descendant::*[@class='tb-slide-popout popout-icon']"), "click view details icon");
		
		Locator VERIFY_CHANGE_DETAILS_PAGE_RHS = new Locator(By.xpath("//*[@id='rhs_panel']"), "verify change detailspage rhs");
		
		Locator ATTACH = new Locator(By.xpath("//button[text()='Attach']"), "attach downtimes");
		
		Locator DOWNTIMESPAGE = new Locator(By.xpath("//a[@title='Downtime' and text()='Downtime']"), "attach downtimes");
		
		Function<String, Locator> VERIFY_DOWNTIMES = (downtimeName) -> new Locator(By.xpath("//td[contains(@title, '" + downtimeName + "')]"), "Verify Text in popup: " + downtimeName);
		
		Locator ASSOCIATIONS_DETAILSPAGE = new Locator(By.xpath("//a[@title='Associations']"), "associations in detailspage");
		
		Locator NEW_RELEASE_DETAILSPAGE = new Locator(By.xpath("//button[text()=' New Release ']"), "associations in detailspage");
		
		Function<String, Locator> CREATE_RELEASE_OPTIONS = (fieldName) -> new Locator(By.xpath("//label[@class='sdpcustom-radio-label' and @title='" + fieldName + "']"), "create release in association");
		
		Locator NEW_RELEASE_APPLY = new Locator(By.xpath("//button[@title='Apply']"), "apply create release option");
		
		Locator ASSOCIATE_RELEASE = new Locator(By.xpath("//span[@class='var-half-gray-txt'and text()='-- Select Release --']"), "associations in detailspage");
		
		Locator ATTACHMENT_DOWNLOAD = new Locator(By.xpath("//span[@class='sdattach-download-ico']"), "attchment download");
		
		Locator ATTACHMENT_DELETE = new Locator(By.xpath("//li[contains(@id,'changesFileAttachments-details')]//span[@class='delete-ico']"), "attchment delete");
		
		Locator NOTES_DELETE = new Locator(By.xpath("//div[contains(@class,'change-conversation')]//span[@title='Delete Note']"), "delete notes in conversation tab");
		
		Function<String, Locator> SYSTEM_ERROR = (error) -> new Locator(By.xpath("//div[@class='system-error' and contains(text(),'" + error + "')]"), "System Error");
		
		Locator SAVE_BUTTON = new Locator(By.xpath("//button[@name='submit' and contains(text(),'Save')]"), "Save button(Alternative for Submit)");
		
		Function<String, Locator> VERIFY_APPROVAL_LEVEL_NUMBER_IN_STAGES = (levelName) -> new Locator(By.xpath("//div[@class='stage-info'][text() = '" + levelName + "']"), "verify/click Approval Level Stage");
		
		Locator IMPACT_DETAILS = new Locator(By.xpath("//h2[@title='Impact Details']"), "Click impact details in Planning Stage");
		
		Function<String, Locator> ATTACHMENTS_IN_PLANNING_STAGE = (fieldName) -> new Locator(By.xpath("//div[@id='" + fieldName + "']/descendant::div[@class='basic-attach']"), "Click required Add Attachment button in planning Stage");
		
		Locator EDIT_BUTTON_IMPACT_DETAILS = new Locator(By.xpath("//div[@class='sdp-layout-section impact_details']/descendant::div[@class='reply-actions-new pointer']/descendant::span[contains(text(),'Edit')]"), "Edit button of Impact details in Planning Stage");
		
		Function<String, Locator> OPTIONS_ON_CHANGE_LHS = (fieldName) -> new Locator(By.xpath("//div[@class='level0 word-break no-children']/descendant::div[contains(text(),'" + fieldName + "')]"), "Options in Change LHS");
		
	}
	
	interface LinkingChange {
		
		// LHS Association tab (main tab in left panel, not stage sub-tab)
		Locator LHS_ASSOCIATION_TAB = new Locator(By.xpath("//a[@data-tabname='associations']"), "Click Association tab in LHS");
		
		// Verify Association tab content area — container ID is 'change_associations_parent_change'
		Locator VERIFY_ASSOCIATION_TAB_OPENED = new Locator(By.xpath("//div[@id='change_associations_parent_change']"), "Verify linking changes association tab opened");
		
		// Attach button dropdown in linked changes section
		Locator ATTACH_BUTTON_DROPDOWN = new Locator(By.xpath("//div[@id='change_associations_parent_change']//button[@name='associating-change-button']"), "Click Attach button in linking changes");
		
		// Attach Parent Change option (dropdown link)
		Locator ATTACH_PARENT_CHANGE_OPTION = new Locator(By.xpath("//a[@name='associate_parent_change']"), "Click Attach Parent Change option");
		
		// Attach Child Changes option (dropdown link)
		Locator ATTACH_CHILD_CHANGES_OPTION = new Locator(By.xpath("//a[@name='associate_child_changes']"), "Click Attach Child Changes option");
		
		// Detach Parent Change button
		Locator DETACH_PARENT_CHANGE = new Locator(By.xpath("//div[@id='change_associations_parent_change']//button[contains(text(),'Detach')]"), "Click Detach button for parent change");
		
		// Parent Change section — same as main linked changes container
		Locator PARENT_CHANGE_SECTION = new Locator(By.xpath("//div[@id='change_associations_parent_change']"), "Parent Change section in association tab");
		
		// Child Changes section
		Locator CHILD_CHANGES_SECTION = new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]"), "Child Changes section in association tab");
		
		// Parent Change badge in title
		Locator PARENT_CHANGE_BADGE = new Locator(By.xpath("//span[contains(@class,'tag') and contains(text(),'Parent Change')]"), "Parent Change badge in details page title");
		
		// Child Change badge in title
		Locator CHILD_CHANGE_BADGE = new Locator(By.xpath("//span[contains(@class,'tag') and contains(text(),'Child Change')]"), "Child Change badge in details page title");
		
		// RHS Linked Changes count
		Function<String, Locator> RHS_LINKED_CHANGES_COUNT = (count) -> new Locator(By.xpath("//div[contains(@class,'rhs-associations')]//a[contains(text(),'Linked')]//span[contains(text(),'" + count + "')]"), "RHS Linked Changes count " + count);
		
		// Records count text in association list
		Locator RECORDS_COUNT_TEXT = new Locator(By.xpath("//div[@id='change_associations_parent_change']//span[contains(@class,'navigatorDetailsColumn')]"), "Records count in linking changes list");
		
		// Page navigation - Next
		Locator PAGE_NEXT = new Locator(By.xpath("//div[@id='change_associations_parent_change']//div[@title='Next']"), "Next page in linking changes list");
		
		// Page navigation - Previous
		Locator PAGE_PREVIOUS = new Locator(By.xpath("//div[@id='change_associations_parent_change']//div[@title='Previous']"), "Previous page in linking changes list");
		
		// Table settings icon
		Locator TABLE_SETTINGS = new Locator(By.xpath("//div[@id='change_associations_parent_change']//div[@data-sdp-table-id='sdp-table-list-settings']"), "Table settings in linking changes list");
		
		// View details icon for a linked change (popout span with href containing CHANGEID)
		Function<String, Locator> VIEW_DETAILS_ICON = (entityId) -> new Locator(By.xpath("//div[@id='change_associations_parent_change']//span[contains(@href,'CHANGEID=" + entityId + "') and @title='View Details']"), "View details icon for linked change " + entityId);
		
		// Select checkbox for child change (find row by popout href CHANGEID)
		Function<String, Locator> SELECT_CHILD_CHECKBOX = (entityId) -> new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]//span[contains(@href,'CHANGEID=" + entityId + "')]/ancestor::tr//span[@class='sdpcustom-checkbox-value']"), "Select child change checkbox " + entityId);
		
		// Verify linked change row by entity ID (popout span href contains CHANGEID)
		Function<String, Locator> LINKED_CHANGE_ROW = (entityId) -> new Locator(By.xpath("//div[@id='change_associations_parent_change']//span[contains(@href,'CHANGEID=" + entityId + "')]/ancestor::tr"), "Linked change row " + entityId);
		
		// Comments field in association popup
		Locator COMMENTS_FIELD = new Locator(By.xpath("//textarea[contains(@placeholder,'comments') or contains(@placeholder,'Comments')]"), "Comments field in linking change popup");
		
		// --- Child Changes section locators ---
		
		// Linked child change row by entity ID (in child changes container)
		Function<String, Locator> LINKED_CHILD_CHANGE_ROW = (entityId) -> new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]//span[contains(@href,'CHANGEID=" + entityId + "')]/ancestor::tr"), "Linked child change row " + entityId);
		
		// Detach button in child changes section
		Locator DETACH_CHILD_CHANGES = new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]//button[contains(text(),'Detach')]"), "Click Detach button for child changes");
		
		// Records count in child changes section
		Locator RECORDS_COUNT_TEXT_CHILD = new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]//span[contains(@class,'navigatorDetailsColumn')]"), "Records count in child changes list");
		
		// Table settings in child changes section
		Locator TABLE_SETTINGS_CHILD = new Locator(By.xpath("//div[contains(@id,'change_associations_child_change')]//div[@data-sdp-table-id='sdp-table-list-settings']"), "Table settings in child changes list");
		
		// --- History tab locators for linking changes ---
		
		// LHS History tab
		Locator LHS_HISTORY_TAB = new Locator(By.xpath("//a[@data-tabname='history']"), "Click History tab in LHS");
		
		// History entry containing text (for linked-changes operation type filter/entry)
		Function<String, Locator> HISTORY_ENTRY_CONTAINING_TEXT = (text) -> new Locator(By.xpath("//div[contains(@class,'history-container') or contains(@class,'history-row')]//span[contains(text(),'" + text + "')]"), "History entry containing text: " + text);
		
		// History filter dropdown (to filter by "Linked Changes" operation)
		Locator HISTORY_FILTER_DROPDOWN = new Locator(By.xpath("//span[contains(@id,'change-history-search-filter') or contains(@class,'history-filter')]"), "History filter dropdown");
		
		// Linking constraint violation error in alert/toast
		Locator CONSTRAINT_VIOLATION_ERROR = new Locator(By.xpath("//div[contains(@class,'sdp-error') or contains(@class,'alert-message')]//span[contains(text(),'not allowed') or contains(text(),'cannot') or contains(text(),'already has a parent')]"), "Linking constraint violation error message");
		
		// RHS summary — linked changes section heading/count
		Locator RHS_LINKED_CHANGES_SECTION = new Locator(By.xpath("//div[contains(@class,'rhs-container')]//a[contains(text(),'Linked Changes') or contains(@title,'Linked Changes')]"), "RHS Linked Changes section link");
		
		// RHS linked changes count badge (the number next to 'Linked Changes' heading)
		Locator RHS_LINKED_CHANGES_COUNT_BADGE = new Locator(By.xpath("//div[contains(@class,'rhs-container')]//a[contains(text(),'Linked Changes') or @title='Linked Changes']/following-sibling::span[contains(@class,'count')] | //div[contains(@class,'rhs-container')]//*[contains(@class,'association-count') and ancestor::*[contains(text(),'Linked')]]"), "RHS Linked Changes count badge");
		
	}
	
	interface LinkingChangePopup {
		
		// Popup title
		Function<String, Locator> POPUP_TITLE = (title) -> new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'" + title + "')]"), "Verify popup title: " + title);
		
		// Filter options in popup (Select2 renders dropdown at body level with class select2-result-label)
		Function<String, Locator> FILTER_OPTION = (filterName) -> new Locator(By.xpath("//div[contains(@class,'select2-result-label') and contains(text(),'" + filterName + "')]"), "Filter option: " + filterName);
		
		// Filter dropdown/toggle (select2 container in popup)
		Locator FILTER_DROPDOWN = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//span[contains(@class,'select2-chosen')] | //span[contains(@class,'requestnamecss')]"), "Click filter dropdown in popup");
		
		// Radio button for parent selection (single select)
		Function<String, Locator> SELECT_RADIO_WITH_ENTITYID = (entityId) -> new Locator(By.xpath("//*[@data-row-id='" + entityId + "']/td/label/span[@class='sdpcustom-radio-value']"), "Select radio for parent change " + entityId);
		
		// Checkbox for child selection (multi select)
		Function<String, Locator> SELECT_CHECKBOX_WITH_ENTITYID = (entityId) -> new Locator(By.xpath("//*[@data-row-id='" + entityId + "']/td/label/span[@class='sdpcustom-checkbox-value']"), "Select checkbox for child change " + entityId);
		
		// Associate button (scoped to popup — avoids matching stray Associate buttons on the underlying page)
		Locator BTN_ASSOCIATE = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//button[contains(text(),'Associate')]"), "Click Associate button in popup");
		
		// Cancel button (scoped to popup — previously unscoped XPath matched wrong Cancel on page, causing silent misfire)
		Locator BTN_CANCEL = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//button[contains(text(),'Cancel')]"), "Click Cancel button in popup");
		
		// Popup dialog container — used to assert popup is OPEN or CLOSED after an action
		// After clicking Cancel/Associate the popup should not be present
		Locator POPUP_DIALOG = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup') and not(contains(@style,'display: none'))]"), "Association dialog popup container");
		
		// Search input in popup list
		Function<String, Locator> SEARCH_INPUT = (fieldName) -> new Locator(By.xpath("//div[@data-search-field-name='" + fieldName + "']/label/input"), "Search input for field: " + fieldName);
		
		// Records count in popup
		Locator POPUP_RECORDS_COUNT = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//span[contains(@class,'navigatorDetailsColumn')]"), "Records count in popup");
		
		// Page navigation in popup - Next
		Locator POPUP_PAGE_NEXT = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//div[@title='Next']"), "Next page in popup");
		
		// Page navigation in popup - Previous
		Locator POPUP_PAGE_PREVIOUS = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//div[@title='Previous']"), "Previous page in popup");
		
		// Table settings in popup
		Locator POPUP_TABLE_SETTINGS = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//div[@data-sdp-table-id='sdp-table-list-settings']"), "Table settings in popup");
		
		// Column search icon in popup (scoped to association-dialog-popup, NOT slide-down-popup)
		Locator POPUP_SEARCH_ICON = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//span[@class='tableSearchButton' and @title='Search'] | //div[contains(@class,'association-dialog-popup')]//button[@title='Search']"), "Search icon in association popup");
		
		// Table header columns in popup (for determining column index by name)
		Locator POPUP_TABLE_HEADER = new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//table[contains(@class,'tableComponent')]/*/tr[1]/th"), "Table header columns in association popup");
		
		// Search input for a specific column index in popup (1-based)
		Function<String, Locator> POPUP_SEARCH_TABLE_HEADER = (index) -> new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//table[contains(@class,'tableComponent')]/*/tr[contains(@class,'search')]/th[" + index + "]//input"), "Search input for column " + index + " in association popup");
		
		// View details icon in popup row
		Function<String, Locator> POPUP_VIEW_DETAILS = (entityId) -> new Locator(By.xpath("//div[contains(@class,'association-dialog-popup')]//*[@data-row-id='" + entityId + "']//a[contains(@class,'popout')]"), "View details for change " + entityId);
		
		// Validation message when no change selected
		Locator NO_SELECTION_WARNING = new Locator(By.xpath("//div[contains(text(),'select at least one change') or contains(text(),'Select at least one')]"), "Warning when no change selected");
		
	}
	
	/**
	 * Locators for the "Linked Changes" column in Change List View (CH-286 feature).
	 * The column shows a count link for parent changes and a parent link for child changes.
	 */
	interface LinkingChangeListView {
		
		// Column header "Linked Changes" in list view table
		Locator LINKED_CHANGES_COLUMN_HEADER = new Locator(By.xpath("//th[@data-sdplayoutid='linked_changes' or @title='Linked Changes']//*[contains(text(),'Linked Changes')]"), "Linked Changes column header in list view");
		
		// Linked Changes cell for a specific change row — the clickable count/link element
		Function<String, Locator> LINKED_CHANGES_CELL = (entityId) -> new Locator(By.xpath("//tr[@data-row-id='" + entityId + "']//td[@data-sdplayoutid='linked_changes']//*[contains(@class,'linked-changes') or self::a or self::span]"), "Linked Changes cell for change " + entityId);
		
		// Tooltip/popup that appears when Linked Changes cell is clicked (lists child changes for parent)
		Locator LINKED_CHANGES_TOOLTIP_POPUP = new Locator(By.xpath("//div[contains(@class,'new-dialog') and contains(@class,'linked-changes')] | //div[contains(@id,'linked-changes-popup')]"), "Linked Changes tooltip popup");
		
		// Change title link in the tooltip popup (to verify child changes are listed)
		Function<String, Locator> LINKED_CHANGES_TOOLTIP_ITEM = (title) -> new Locator(By.xpath("//div[contains(@class,'new-dialog')]//a[contains(text(),'" + title + "')] | //div[contains(@id,'linked-changes-popup')]//a[contains(text(),'" + title + "')]"), "Linked change entry '" + title + "' in tooltip");
		
		// Detail popup shown when clicking Linked Changes on a child change row (shows parent details)
		Locator PARENT_CHANGE_DETAIL_POPUP = new Locator(By.xpath("//div[contains(@class,'change-header-details')] | //div[contains(@class,'quick-view')]"), "Parent change detail popup in list view");
		
	}
	
	interface Popup {
		
		Locator VERIFY_ATTACH_REQUEST_TEXT_IN_POPUP = new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'Attach Requests')]"), "Verify popup text as Attach Requests");
		
		// Locator BTN_ASSOCIATE = new Locator(By.xpath("//button[contains(text(),'Associate')]"), "Click Associate button in the popup");
		
		Locator CLICK_LISTVIEW_FILTERS = new Locator(By.xpath("//span[contains(@class,'requestnamecss')]"), "click Listview Filters");
		
		Locator CLICK_ALL_REQUESTS_FILTERS = new Locator(By.xpath("//div[@class='filter-search-menu']/descendant::span[contains(text(),'All Requests')]"), "click All Request Filters");
		
		Locator CLICK_ALL_CANCELED_REQ_FILTERS = new Locator(By.xpath("//div[@class='filter-search-menu']/descendant::span[contains(text(),'Canceled Requests')]"), "click Canceled request Request Filters");
		
		Locator VERIFY_ATTACH_PROBLEM_TEXT_IN_POPUP = new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'Attach Problems')]"), "Verify popup text as Attach Problem");
		
		Locator CLICK_ALL_PROBLEMS_FILTERS = new Locator(By.xpath("//div[@id='filterdiv']/descendant::a[contains(text(),'All Problems')]"), "click All Problems Filters");
		
		Locator VERIFY_ATTACH_PROJECTS_TEXT_IN_POPUP = new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'Attach Projects')]"), "Verify popup text as Attach Projects");
		
		Locator CLICK_ALL_PROJECTS_FILTERS = new Locator(By.xpath("//div[contains(@id,'select2-drop')]/descendant::div[contains(text(),'All Projects')]"), "click All Projects Filters");
		
		Locator VERIFY_ASSOCIATE_RELEASE_TEXT_IN_POPUP = new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'Associate Release')]"), "Verify popup text as Associate Release");
		
		Locator CLICK_PROJECTS_LISTVIEW_FILTERS = new Locator(By.xpath("//div[contains(@id,'project-association-filter')]/descendant::a"), "click Projects Filters");
		
		Function<String, Locator> TEXT_IN_POPUP = (fieldName) -> new Locator(By.xpath("//span[contains(@class,'ui-dialog-title') and contains(text(),'" + fieldName + "')]"), "Verify Text in popup" + fieldName);
		
		Function<String, Locator> SELECT_RADIOBTN_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("//*[@data-row-id='" + EntityId + "']/td/label/span[@class='sdpcustom-radio-value']"), "Click the radio button with entity id " + EntityId);
		
		Locator SEARCH_IN_BELL_NOTIFICATION = new Locator(By.xpath("//div[@id='Notification_popup']/descendant::input[@name='search']"), "Search in bell notification popup");
		
		Function<String, Locator> CLICK_TEMP_ID_IN_REQUESTER_LOGIN = (entityId) -> new Locator(By.xpath("//li[@id='" + entityId + "']/div"), "click temp name popup");
		
		Locator CLICK_VIEW_DETAILS_IN_BELL_NOTIFICATION = new Locator(By.xpath("//a[@class='popout-icon']"), "clivk viewdetails in bell notification popup");
		
		Function<String, Locator> VERIFY_TABLE_HEADER = (fieldValue) -> new Locator(By.xpath("//th/div[contains(text(),'" + fieldValue + "')]"), "verify table header column " + fieldValue);
		
		Function<String, Locator> SELECT_CHECKBOX_WITH_ENTITYID = (EntityId) -> new Locator(By.xpath("//*[@data-row-id='" + EntityId + "']/td/label/span[@class='sdpcustom-checkbox-value']"), "Click the checkbox for change with entity id " + EntityId);
		
		Locator NEW_RELEASE_APPLY = new Locator(By.xpath("//button[@title='Apply']"), "apply create release option");
		
		Locator ATTACH_DOWNTIME = new Locator(By.xpath("//button[@data-refid='attach_downtimes']"), "attach downtimes");
		
		Locator VERIFY_NEW_RELEASE_FORM_FIELDS = new Locator(By.xpath("//span[contains(@class,'select2-chosen') and normalize-space(text())='-- Select Impact --']"), "apply create release option");
		
		Function<String, Locator> SELECT_CHECKBOX_BY_TITLE = (title) -> new Locator(By.xpath("//tr[td//span[@title='" + title + "']]//span[@class='sdpcustom-checkbox-value']"), "Click the checkbox span for row with title '" + title + "'");
		
	}
	
	interface ChangeWorkflow {
		
		Function<String, Locator> WORKFLOW_BY_NAME = (name) -> new Locator(By.xpath("//a[contains(text(),'" + name + "')]"), "Workflow by name");
		
		Locator WORKFLOW_HEADER_ICON = new Locator(By.xpath("//a[contains(@class,'workflow-ico')]"), "Workflow header icon");
		
	}
	
	interface Ajax {
		
		Locator TEXT_AJAXMESSAGETEXT = new Locator(By.xpath("//div[@id='ajax_message_tab']/descendant::span[@class='sdp-ajax-msg-txt']"), "Ajax notification text");
		
	}
	
	interface CustomerIssue {
		
		Function<String, Locator> CHANGE_SUB_HEADING = (subheading) -> new Locator(By.xpath("//div[@class='req-header-view table-extension']/descendant::div[@data-sdp-table-id='sdp-table-list-buttons']/descendant::span/descendant::button/child::span[text()='" + subheading + "']"), "Click subheading Name in Changes Listview");
		
		Locator FILL_TITLE = new Locator(By.xpath("//input[@data-fieldrefname='title']"), "Fill Change Title field");
		
		Locator SEARCH_CHANGE_TEMPLATE = new Locator(By.xpath("//input[@id='changeTemplateSearch']"), "Search Change Template");
		
		Locator NO_TASKS_FOUND_IN_THIS_VIEW = new Locator(By.xpath("//div[contains(text(),'No tasks found in this view')]"), "No tasks found in tihis view");
		
		Locator NOTIFICAITON_POPUP = new Locator(By.xpath("//a[@id='notif_popup_open']"), "Click Notification Popup");
		
	}
	
	public final static class ValidationMessage {
		
		public static final Function<String, Locator> VERIFY_VALIDATION_MESSAGE = (fieldType) -> new Locator(By.xpath("//label[@for='" + fieldType + "'] [contains(@class,'error comments-mandatory')]"), "Verify validation message");
		
	}
	
	public final static class History {
		
		public static final Locator CLICK_HERE = new Locator(By.xpath("//a[contains(text(),'Click here')]"), "click here link from history");
		
		public static final Locator VERIFY_NOTE_DETAIL_IN_HISTORY = new Locator(By.xpath("//div[contains(@class,'ui-dialog ui-widget')]/descendant::div[@class='history-resolution-diff-content']"), "verify note details history");
		
		public static final Function<String, Locator> DESCRIPTION = (OperationName) -> new Locator(By.xpath("//div[contains(text(), '" + OperationName + "')]/following-sibling::div/div"), "");
		
	}
	
	public final static class GLOBAL_SEARCH {
		
		public static final Locator VERIFY_GLOBAL_SEARCH_POPUP = new Locator(By.xpath("//div[@sdp-divid='search-suggestions']"), "verify global search popup");
		
		public static final Locator VERIFY_CHANGE_MATCH_TEXT = new Locator(By.xpath("//*[@id='gss-change-details']/descendant::*[contains(text(),'Change matching your search')]"), "verify global search popup");
		
		public static final Function<String, Locator> CHANGE_TITLE = (changeTitle) -> new Locator(By.xpath("//*[@id='gss-change-details']/descendant::*[@id='rss-title'][contains(text(),'" + changeTitle + "')]"), "Change title");
		
		public static final Function<String, Locator> CHANGE_DISPLAY_VALUE = (changeDisplayValue) -> new Locator(By.xpath("//*[@id='gss-change-details']/descendant::*[@class='ss-label'][contains(text(),'Change ID : ')]/following-sibling::*[@class='ss-value'][contains(text(),'" + changeDisplayValue + "')]"), "Change display value");
		
		public static final Function<String, Locator> CHANGE_TITLE_IN_GLOBAL_SEARCH = (changeTitle) -> new Locator(By.xpath("//*[@id='gss-change-details']/descendant::*[@id='rss-title'][contains(text(),'" + changeTitle + "')]"), "Change title");
		
		public static final Locator CLOSE_ICON = new Locator(By.xpath("//*[@title='Close Search']"), "close icon in global search popup");
		
		public static final Locator CHANGE_ASSOCIATION_GLOBALSEARCH = new Locator(By.xpath("(//span[@class='fleft tableTopSearchColumn']//span[@data-sdp-table-id='search-btn'])[2]"), "search icon in global search popup");
		
	}
	
}
