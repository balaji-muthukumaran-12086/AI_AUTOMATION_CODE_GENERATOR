# Scenario ID Audit Report

**Generated:** Feb 27, 2026  |  **Project:** SDPLIVE_LATEST_AUTOMATER_SELENIUM

---

## Summary

| Metric | Count |
|--------|-------|
| Unique duplicate IDs | 1461 |
| Total occurrences of duplicate IDs | 4021 |
| Empty ID scenarios | 1372 |

---

## Part 1 — Duplicate Scenario IDs

> These IDs appear in more than one `@AutomaterScenario` annotation. ChromaDB collapses them to 1 vector, losing the additional entries.


### `SDPOD_AUTO_NOTIFICATION_014` — ×152 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyEditorAwaiting()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestTechnicianOnRequestAssigned()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyRequesterMovedToAnotherInstance()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyRequesterSLAChangedForRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechOnRequestClose()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyUserOnTechReply()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyRequesterOnRequestUpdate()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyRequesterOnApproval()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestSubmitForApproval()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyRequestWhenPublicNoteAdded()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechOnCreateRequest()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyOldEditorOnReassign()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechWhenRequestCanceled()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestSubmitForApprovalForRequester()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechOnRequesterReply()` |
| 16 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechOnRequesterReopen()` |
| 17 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechWhenApprovalWFOrgRolesEmpty()` |
| 18 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechWhenRequesterEdit()` |
| 19 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyGroupMembWhenGroupRequestUpdated()` |
| 20 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyGroupMembWhenGroupRequestUnpicked()` |
| 21 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyGroupMembWhenGroupRequestAdded()` |
| 22 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestNotifyTechWhenRequestUpdatedByEditor()` |
| 23 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestSLAEsclation()` |
| 24 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestFirstResponseEsclation()` |
| 25 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestRequesterReply()` |
| 26 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestForwarding()` |
| 27 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestEmaiToTechnician()` |
| 28 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestApprovalEmail()` |
| 29 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `requestAddNotesEmail()` |
| 30 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechWhenAssigned()` |
| 31 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechWhenCreated()` |
| 32 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechWhenIncidentAssociated()` |
| 33 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechWhenIncidentDetached()` |
| 34 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechWhenProblemClosed()` |
| 35 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyGroupMemberWhenProblemAdded()` |
| 36 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemNotifyTechOnResponseReceived()` |
| 37 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemClosureEmailToTechnican()` |
| 38 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemClosureEmailToRequester()` |
| 39 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemEmailUserToNoteAttachment()` |
| 40 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `problemEmailToTechOrReq()` |
| 41 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeAssigned()` |
| 42 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeCreated()` |
| 43 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenRemovedFromRole()` |
| 44 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenProblemAssociated()` |
| 45 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenProblemDetached()` |
| 46 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenIndicentAttached()` |
| 47 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenIndicentDetached()` |
| 48 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenProjectAttached()` |
| 49 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenProjectDetached()` |
| 50 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenDowntimeAssociated()` |
| 51 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenChangeClosed()` |
| 52 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenDowntimeCanceled()` |
| 53 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenApprovalStateEdited()` |
| 54 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotification()` |
| 55 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotesAddition()` |
| 56 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `changeNotifyWhenStatusChanged()` |
| 57 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectAssigned()` |
| 58 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyChangeOwnerWhenAssociatedProjectClosed()` |
| 59 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyUserWhenMilestoneAssigned()` |
| 60 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyUserWhenMilestoneReAssigned()` |
| 61 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyUserWhenMilestoneClosed()` |
| 62 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyUserWhenAllMilestoneClosed()` |
| 63 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyProjectOwnerWhenMilestoneRescheduled()` |
| 64 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyOwnerWhenMilestoneRescheduled()` |
| 65 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `projectNotifyUserWhenMilestoneProjectedDateUpdated()` |
| 66 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseApproveAction()` |
| 67 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyRequesterOnReleaseCreate()` |
| 68 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyOwnerWhenAssigned()` |
| 69 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyReleaseManagerWhenAssigned()` |
| 70 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyUserWhenNewRoleAssigned()` |
| 71 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyUserWhenRoleRemoved()` |
| 72 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyEngineerWhenChangeAttached()` |
| 73 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyEngineerWhenChangeDetached()` |
| 74 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyChangeOwnerWhenDowntimeInChangeApprovedInAssociatedRelease()` |
| 75 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyEngineerWhenProjectAttached()` |
| 76 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyEngineerWhenProjectDetached()` |
| 77 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyReleaseEngineerWhenDeploymentInProgress()` |
| 78 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyReleaseEngineerWhenDeploymentCompleted()` |
| 79 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotifyWhenAssociatedReleasesUpdated()` |
| 80 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseNotificationEmail()` |
| 81 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseEMailUsersOnNoteAttachment()` |
| 82 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `releaseStatusChangeNotification()` |
| 83 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `solutionAcknUserOnSolutionApproval()` |
| 84 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `solutionApproved()` |
| 85 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `solutionNotifyWhenCreatedOrUpdated()` |
| 86 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `solutionNotifyTechWhenCommentAddedOrEdited()` |
| 87 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `solutionSubmitForApproval()` |
| 88 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetExpiryNotification()` |
| 89 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetProibitedSoftwareInstallation()` |
| 90 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetProibitedSoftwareInstallationToUser()` |
| 91 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetUserAssignedNotification()` |
| 92 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetUserRemovedNotification()` |
| 93 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyDepartmentHeadWhenAssetAssigned()` |
| 94 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyDepartmentHeadWhenAssetRemoved()` |
| 95 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyUserOnLoan()` |
| 96 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyDepartmentHeadOnLoan()` |
| 97 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyUserOnLoanReturned()` |
| 98 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyDeptOnLoanReturned()` |
| 99 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyUserOnLoanExtended()` |
| 100 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyDeptOnLoanExpiry()` |
| 101 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNotifyTechnicianWhenQuantityFallsBelowThreshold()` |
| 102 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNoftifyConsumableAllocated()` |
| 103 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetWarrentyExpiryNotification()` |
| 104 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNoftifyUserConsumableAllocationChanged()` |
| 105 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNoftifyDeptConsumableAllocated()` |
| 106 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `assetNoftifyDeptConsumableAllocationChanged()` |
| 107 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `cmdbNotifyWhenDowntimeScheduled()` |
| 108 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `cmdbNotifyWhenDowntimeStarted()` |
| 109 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseOverdue()` |
| 110 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseNotifyTechnicianWhenPORejected()` |
| 111 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseNotifyTechnicianWhenPOItemReceived()` |
| 112 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseNotifyTechnicianWhenPOItemPartiallyReceived()` |
| 113 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseNotifyTechnicianWhenPOCanceled()` |
| 114 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseInvoiceRecieved()` |
| 115 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseEmailOwner()` |
| 116 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `purchaseEmailVendor()` |
| 117 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractExpiry()` |
| 118 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractOwner()` |
| 119 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractVendor()` |
| 120 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractCanceled()` |
| 121 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractNotesAttached()` |
| 122 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `contractAutoRenewed()` |
| 123 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskAssign()` |
| 124 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskReAssign()` |
| 125 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskReScheduled()` |
| 126 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyCreatorWhenTaskClosed()` |
| 127 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskWorklogAdded()` |
| 128 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyOwnerWhenTaskNotCompletedInSchedule()` |
| 129 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskGroupAssign()` |
| 130 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyTechnicianWhenAllTasksCompleted()` |
| 131 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyAssociatedEntityOwnerWhenRescheduled()` |
| 132 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyAssociatedEntityOwnerWhenClosed()` |
| 133 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyAssociatedEntityOwnerWhenAllTaskClosed()` |
| 134 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyassocentityTasksoverdue()` |
| 135 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `taskNotifyOwnerWhenAllTasksCompleted()` |
| 136 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyGroupOnTechUnavailablity()` |
| 137 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyTechOnTechUnavailablity()` |
| 138 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyGroupOnTechUnavailablityCanceled()` |
| 139 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyTechOnUnavailablityCanceled()` |
| 140 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyOfflineUseronLeaveEdit()` |
| 141 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyOfflineUserWhenBackupConfigured()` |
| 142 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyBachupApproverOnDelegationConfigured()` |
| 143 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyOfflineUserOnApprovalSent()` |
| 144 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyBackupApproverOnAction()` |
| 145 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersNotifyBackUpApproverOnDelegationRevoked()` |
| 146 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersAnnouncementEmail()` |
| 147 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersReminderEmail()` |
| 148 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersAssetLicenseUpgrade()` |
| 149 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersTechLimitIncreased()` |
| 150 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersReplyAdd()` |
| 151 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersReplyEdited()` |
| 152 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `othersAutomaticApprovalEnabled()` |

### `NoPreprocess` — ×42 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyExportIconInChange()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 3 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 4 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 5 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyExportIconPresentInTrashChange()` |
| 6 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyAllDataExportOptionsPresentInTrashChange()` |
| 7 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInTrashChange()` |
| 8 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInTrashChange()` |
| 9 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyExportIconInCmdb()` |
| 10 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 11 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 12 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 13 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `verifyExportIconInCmdb()` |
| 14 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 15 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 16 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 17 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyExportIconInProblem()` |
| 18 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 19 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 20 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 21 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyExportIconPresentInTrashProblem()` |
| 22 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAllDataExportOptionsPresentInTrashProblem()` |
| 23 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInTrashProblem()` |
| 24 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInTrashProblem()` |
| 25 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdmin.java` | `verifyExportIconShouldNotPresentInProblemForSDSiteAdmin()` |
| 26 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 27 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 28 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 29 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyExportIconPresentInTrashProblem()` |
| 30 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyAllDataExportOptionsPresentInTrashProblem()` |
| 31 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInTrashProblem()` |
| 32 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInTrashProblem()` |
| 33 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyExportIconPurchase()` |
| 34 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 35 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 36 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 37 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyExportIconPresentInTrashPurchase()` |
| 38 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyExportIconInRelease()` |
| 39 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 40 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 41 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 42 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyExportIconPresentInTrashRelease()` |

### `SDPOD_AUTO_REQ_TRIGGER_324` — ×36 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsAllWorklogInEdit()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsAllWorklogInDelete()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsChangeWorklogInCreate()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsChangeWorklogInEdit()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsChangeWorklogInDelete()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskWorklogInCreate()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskWorklogInEdit()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskWorklogInDelete()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsNotesInCreate()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsNotesInEdit()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsNotesInDelete()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalLevelInCreate()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalLevelInEdit()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalLevelInDelete()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalInCreate()` |
| 16 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalInEdit()` |
| 17 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsApprovalInDelete()` |
| 18 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsDowntimeInCreate()` |
| 19 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsDowntimeInEdit()` |
| 20 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsDowntimeInDelete()` |
| 21 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsAllWorklogInCreate()` |
| 22 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskWorklogInCreate()` |
| 23 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskWorklogInEdit()` |
| 24 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskWorklogInDelete()` |
| 25 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsNotesInCreate()` |
| 26 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsNotesInEdit()` |
| 27 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsNotesInDelete()` |
| 28 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalLevelInCreate()` |
| 29 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalLevelInEdit()` |
| 30 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalLevelInDelete()` |
| 31 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalInCreate()` |
| 32 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalInEdit()` |
| 33 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsApprovalInDelete()` |
| 34 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsDowntimeInCreate()` |
| 35 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsDowntimeInEdit()` |
| 36 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsDowntimeInDelete()` |

### `SDPOD_ZIA_028` — ×36 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose4()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose6()` |
| 3 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose7()` |
| 4 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose8()` |
| 5 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose9()` |
| 6 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose10()` |
| 7 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose11()` |
| 8 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose12()` |
| 9 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose13()` |
| 10 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose14()` |
| 11 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose15()` |
| 12 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose16()` |
| 13 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose17()` |
| 14 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose18()` |
| 15 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose19()` |
| 16 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose20()` |
| 17 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose21()` |
| 18 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose22()` |
| 19 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose26()` |
| 20 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose28()` |
| 21 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose29()` |
| 22 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose30()` |
| 23 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose31()` |
| 24 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose32()` |
| 25 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose33()` |
| 26 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose34()` |
| 27 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose35()` |
| 28 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose36()` |
| 29 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose37()` |
| 30 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose38()` |
| 31 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose39()` |
| 32 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose40()` |
| 33 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose41()` |
| 34 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose42()` |
| 35 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose43()` |
| 36 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose44()` |

### `SDPOD_Custum_Report_048, SDPOD_Custom_Report_043` — ×29 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentsTasksEditComment()` |
| 2 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesTasksEditComment()` |
| 3 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemsTasksEditComment()` |
| 4 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectsTasksEditComment()` |
| 5 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeTasksEditComment()` |
| 6 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseTasksEditComment()` |
| 7 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralTasksEditComment()` |
| 8 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentEditWorklog()` |
| 9 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServiceEditWorklog()` |
| 10 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemEditWorklog()` |
| 11 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeEditWorklog()` |
| 12 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseEditWorklog()` |
| 13 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectEditWorklog()` |
| 14 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForEditProjectsDescription()` |
| 15 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentWithEditTasksDesc()` |
| 16 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesWithEditTasksDesc()` |
| 17 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemWithEditTasksDesc()` |
| 18 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectWithEditTasksDesc()` |
| 19 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectWithMilestonesEditTasksDesc()` |
| 20 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeWithEditTasksDesc()` |
| 21 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseWithEditTasksDesc()` |
| 22 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralWithEditTasksDesc()` |
| 23 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentEditTaskWorklogDesc()` |
| 24 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesEditTaskWorklogDesc()` |
| 25 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemEditTaskWorklogDesc()` |
| 26 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectEditTaskWorklogDesc()` |
| 27 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeEditTaskWorklogDesc()` |
| 28 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseEditTaskWorklogDesc()` |
| 29 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralEditTaskWorklogDesc()` |

### `SDPOD_AUTO_id` — ×26 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/CustomActions.java` | `createCustomActions()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/changemanagement/changetype/ChangeType.java` | `addChangeType()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/helpdesk/category/Category.java` | `test()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `siteLookupData()` |
| 5 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `createServiceCategory()` |
| 6 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `createMultipleServiceCategory()` |
| 7 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `moveServiceCategory()` |
| 8 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `editServiceCategory()` |
| 9 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `disableParentServiceCategoryAndVerifyAllChildsDisabled()` |
| 10 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `disableChildServiceCategoryAndVerifyAllChildsDisabled()` |
| 11 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `disableChildServiceCategoryAndVerifyAllParentsEnabled()` |
| 12 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyServiceTemplatesAssociatedIntoAllServiceCategory()` |
| 13 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyIncidentTemplatesAssociatedIntoAllServiceCategory()` |
| 14 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyCannotCreateMoreThanFiveLevelofServiceCategories()` |
| 15 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyAbleToUpdateServiceCategoryWithoutDescription()` |
| 16 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `createServiceCategory()` |
| 17 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createSolution()` |
| 18 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `brHardWareDispatch()` |
| 19 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `brNetworkInternet()` |
| 20 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `brNetworkRouters()` |
| 21 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `brNetworkSwitches()` |
| 22 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `brPrinterRequests()` |
| 23 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifySiteLookupFieldIsPresentInListview()` |
| 24 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `attachFileNewRequest()` |
| 25 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addImage()` |
| 26 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `attachFileRHS()` |

### `SDPOD_AUTO_REQUEST_NOTIFY_002` — ×26 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestEdited()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestResolved()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestClosed()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestAssigned()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestCanceled()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestCancellationIsRejected()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestApprovedOrRejected()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestNoteAdded()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestSLAChanged()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestAutoApproved()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestAssigned()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestClosed()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestCanceled()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestCancellationIsRaised()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenApproverActsonRequest()` |
| 16 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestSLAChanged()` |
| 17 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `slaEscalationMail()` |
| 18 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `firstResponseSlaEscalationMail()` |
| 19 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `requesterReply()` |
| 20 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `forwardRequest()` |
| 21 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `emailToTechhnician()` |
| 22 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `sumbitForApproval()` |
| 23 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `emailTechnicianForNotesAddition()` |
| 24 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestAddedToGroup()` |
| 25 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestInGroupUnpicked()` |
| 26 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenGroupRequestUpdated()` |

### `SDPOD_ORG_ROLE_129` — ×26 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromRegionforRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromRegionforRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromRegionforTechnician()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromRegionforRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromRegionforRequester()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromRegionforTechnician()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromOrganization()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromOrganization()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromOrganization()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromOrganization()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromSiteforRequest()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromSiteforRequester()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromSiteforTechnician()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromSiteforRequest()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromSiteforRequester()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromSiteforTechnician()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromDepartmentForRequest()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromDepartmentForTechnician()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromDepartmentForRequest()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromDepartmentForTechnician()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromGroupForRequest()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromGroupForRequest()` |
| 23 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromUserForRequester()` |
| 24 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforRequestFromUserForTechnician()` |
| 25 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromUserForRequester()` |
| 26 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforRequestFromUserForTechnician()` |

### `SDPOD_ORG_ROLE_160` — ×23 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromRegionForRelease()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromRegionForReleaseRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromRegionForReleaseEngineer()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseeFromRegionForReleaseRequester()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseeFromRegionForReleaseEngineer()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseeFromRegionforRelease()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromOrganization()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromOrganization()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromSiteForReleaseRequester()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromSiteForReleaseEngineer()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromSiteForRelease()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromSiteForReleaseForReleaseRequester()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromSiteForReleaseForReleaseEngineer()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromDepartmentForReleaseRequester()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromDepartmentForReleaseEngineer()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromDepartmentForReleaseRequester()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromDepartmentForReleaseEngineer()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromGroupForRelease()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromGroupForRelease()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromUserForReleaseRequester()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforReleaseFromUserForReleaseEngineer()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromUserForReleaseRequester()` |
| 23 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforReleaseFromUserForReleaseEngineer()` |

### `SDPOD_ORG_ROLE_130` — ×23 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromRegionForRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromRegionForRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromRegionForTechnician()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromRegionForRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromRegionForRequester()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromRegionForTechnician()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromOrganization()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromOrganization()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromSiteforRequest()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromSiteForRequester()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromSiteForTechnician()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromSiteForRequest()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromSiteForRequester()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromSiteForTechnician()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromDepartmentForTechnician()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromDepartmentForRequest()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromDepartmentForTechnician()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromGroupForRequest()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromGroupForRequest()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromUserForRequester()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromUserForTechnician()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromUserForRequester()` |
| 23 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyWorkflowforRequestFromUserForTechnician()` |

### `SDPOD_ORG_ROLE_030` — ×22 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromRegionforRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromRegionforRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromRegionforTechnician()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromRegionforRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromRegionforRequester()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromRegionforTechnician()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromSiteForRequest()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromSiteForRequester()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromSiteForTechnician()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromSiteForRequest()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromSiteForRequester()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromSiteForTechnician()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromDepartmentForRequest()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromDepartmentForTechnician()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromDepartmentForRequest()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromDepartmentForTechnician()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforRequestFromGroupForRequest()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforRequestFromGroupForRequest()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforRequestFromUserforRequester()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforRequestFromUserforTechnician()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforRequestFromUserForRequester()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforRequestFromUserForTechnician()` |

### `SDPOD_ORG_ROLE_062` — ×22 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromRegionforRelease()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromRegionForReleaseRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromRegionForReleaseEngineer()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromRegionForRelease()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromRegionForReleaseRequester()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromRegionForReleaseEngineer()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromOrganization()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromOrganization()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromSiteForRelease()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromSiteForReleaseRequester()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromSiteForReleaseEngineer()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromSiteForRelease()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromSiteForReleaseRequester()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromSiteForReleaseEngineer()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromDepartmentForReleaseRequester()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromDepartmentForReleaseEngineer()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromDepartmentForReleaseRequester()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromDepartmentForReleaseEngineer()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforReleaseFromGroupForRelease()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforReleaseFromGroupForRelease()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforReleaseFromUserForReleaseRequester()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforReleaseFromUserForReleaseEngineer()` |

### `SDPOD_ORG_ROLE_031` — ×22 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromRegionforRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromRegionforRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromRegionforTechnician()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromOrganization()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromSiteForRequest()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromSiteForRequester()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromSiteForTechnician()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromSiteForRequest()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromSiteForRequester()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromSiteForTechnician()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyWorkflowforRequestFromDepartmentForRequest()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromDepartmentForRequest()` |
| 14 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromDepartmentForTechnician()` |
| 15 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromDepartmentForRequest()` |
| 16 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromDepartmentForTechnician()` |
| 17 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyWorkflowforRequestFromGroupForRequest()` |
| 18 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromGroupForRequest()` |
| 19 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyWorkflowforRequestFromUserForRequester()` |
| 20 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyWorkflowforRequestFromUserForTechnician()` |
| 21 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromUserForRequester()` |
| 22 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyWorkflowforRequestFromUserForTechnician()` |

### `SDPOD_Release_TPT_2564` — ×20 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `deleteTaskFromCustomStage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUdfInSubmissionStage()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUdfInPlanningStage()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `VerifyUDFInDevelopmentStage()` |
| 5 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUDFInTestingStage()` |
| 6 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUDFInUATStage()` |
| 7 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUDFInDeploymentStage()` |
| 8 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUDFInTrainingStage()` |
| 9 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyUDFInReviewStage()` |
| 10 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `addUDFInCustomStage()` |
| 11 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveSingleUDFFromSubmissionToPlanning()` |
| 12 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromPlanningToDevelopment()` |
| 13 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromDevelopmentToTesting()` |
| 14 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromTestingToUAT()` |
| 15 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromUATToDeployment()` |
| 16 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromDeploymentoTraining()` |
| 17 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromTrainingToReview()` |
| 18 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromReviewToClosure()` |
| 19 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `moveUDFFromClosureToPlanning()` |
| 20 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyFieldEditInMovedStage()` |

### `SDPOD_AUTO_PURCHASE_54` — ×19 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithGlCode()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithCostUDF()` |
| 3 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithSingleLineUDF()` |
| 4 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithMultiLineUDF()` |
| 5 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithPickListUDF()` |
| 6 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithNumericUDF()` |
| 7 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithDateTimeUDF()` |
| 8 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithEmailUDF()` |
| 9 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithPhoneUDF()` |
| 10 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithWebUrlUDF()` |
| 11 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithMultiSelectUDF()` |
| 12 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithCurrencyUDF()` |
| 13 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithDecimalUDF()` |
| 14 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithPercentageUDF()` |
| 15 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithAutoNumberUDF()` |
| 16 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithCheckBoxUDF()` |
| 17 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithRadioButtonUDF()` |
| 18 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithDecisonBoxUDF()` |
| 19 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createPOwithAllUDF()` |

### `SDPOD_AUTO_REQ_TRIGGER_` — ×18 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `checkChangeTriggerInCreate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `checkChangeTriggerInEdit()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskInCreate()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskInEdit()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsTaskInDelete()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createChangeTriggerWithSubentityIsAllWorklogInCreate()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalLevelInCreate()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalLevelInEdit()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalLevelInDelete()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalInCreate()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalInEdit()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsApprovalInDelete()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsNotesInCreate()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsNotesInEdit()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsNotesInDelete()` |
| 16 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsWorkLogTimerInCreate()` |
| 17 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsWorkLogTimerInEdit()` |
| 18 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createRequestTriggerWithSubentityIsWorkLogTimerInDelete()` |

### `ZIA_AI` — ×18 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/artificialintelligence/GenAIFeatures.java` | `enableDisableAllGenAicards()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/artificialintelligence/PredictiveFeatures.java` | `enableDisableAllRequestcards()` |
| 3 | `com/zoho/automater/selenium/modules/admin/zia/artificialintelligence/PredictiveFeatures.java` | `enableDisableAllProblemcards()` |
| 4 | `com/zoho/automater/selenium/modules/admin/zia/artificialintelligence/PredictiveFeatures.java` | `enableDisableAllChangecards()` |
| 5 | `com/zoho/automater/selenium/modules/admin/zia/artificialintelligence/PredictiveFeatures.java` | `enableDisableAllSolutioncards()` |
| 6 | `com/zoho/automater/selenium/modules/admin/zia/ziachatbot/Ziachatbot.java` | `enableDisableClassicChatbot()` |
| 7 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `createAnIncidentbyAskZia()` |
| 8 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `createServiceRequestbyAskZia()` |
| 9 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `searchSolutionbyAskZia()` |
| 10 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `myOverDueRequestsbyAskZia()` |
| 11 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `myOpenTasksbyAskZia()` |
| 12 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `mergeRequestsbyAskZia()` |
| 13 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `linkRequestsbyAskZia()` |
| 14 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `myPendingApprovalRequestsbyAskZia()` |
| 15 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `myAssetsbyAskZia()` |
| 16 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `pickUpRequestbyAskZia()` |
| 17 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `assignTechnicianbyAskZia()` |
| 18 | `com/zoho/automater/selenium/modules/askzia/askzia/Askzia.java` | `addTaskToRequestbyAskZia()` |

### `SDPOD_CH_MINOR_ENH_001` — ×15 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyUserWhenAssignedAnyChangeRolesLMForPushNotifications()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verfiyChangeDetailsPageNaviagtionViaViewDetailsIcon()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `selectTechToNotifyWhenNewChangeCreatedForPushNotifications()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyTechWhenRemovedForChangeRoleForPushNotifications()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyChangeOwnerWhenNewProblemAssociateToChangeForPushNotifications()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyChangeOwnerWhenNewProblemDetachedFromChangeForPushNotifications()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyChangeOwnerAndIncRequesterWhenNewIncAssociateToChangeForPN()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyChangeOwnerAndIncRequesterWhenNewIncDetachedToChangeForPN()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyProjectOwnerWhenProjectAssociateToChangeForPN()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyProjectOwnerWhenProjectDetachedFromChangeForPN()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifySelectCMDBUsersToNotifyWhenDowntimeScheduledForCIFromChangeForPN()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifySelectCMDBUsersToNotifyWhenCIScheduledDowntimeIsCanceledFromChangeForPN()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifySelectTechToNotifyWhenChangeClosedFromChangeForPN()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyCMCOCAAndCABMembersWhenApprovalActionTakenOnChangeFromChangeForPN()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifySelectedChangeRolesWhenChangeIsEditedDuringOrAfterCABApprovalFromChangeForPN()` |

### `SDPOD_CH_MINOR_ENH_006` — ×14 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyUsersAssignedWithChangeRolesFromChangeForPN()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForSelectTechNotifyWhenNewChangeCreatedFromChangeForPN()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyTechWhenRemovedChangeRoledFromChangeForPN()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyChangeOwnerWhenNewPblmAssociatedToChangeFromChangeForPN()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyChangeOwnerWhenNewProblemDetachFromChangeForPN()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNewIncidentAssociateToChangeFromChangePN()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyCOAndIncReqDetachedFromChangeForChangePN()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyProjectOwnerWhenProjectAssociateToChangeForChangePN()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForNotifyProjectOwnerWhenProjectDetachedFromChangeForChangePN()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForSelectCMDBUsersWhenDowntimeScheduledForCIForChangePN()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForSelectCMDBUsersWhenCIScheduledDowntimeIsCancelledForChangePN()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentForSelectTechToNotifyWhenChangeClosedForChangePN()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentToNotifyCmCOCaCABWhenApprovalTakeChangeForChangePN()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `verifyCNTContentToNotifyChangeRolesWhenChangeEditedDuringChangeApprovaleForChangePN()` |

### `SDP_CHGPM_LS_AAA001` — ×14 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `createScheduleDaily()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `createScheduleWeekly()` |
| 3 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `createScheduleMonthly()` |
| 4 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `createSchedulePeriodic()` |
| 5 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `createScheduleOnce()` |
| 6 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `activeMaintenanceFilter()` |
| 7 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `suspendedMaintenanceFilter()` |
| 8 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `createScheduleDaily()` |
| 9 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `createScheduleWeekly()` |
| 10 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `createScheduleMonthly()` |
| 11 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `createSchedulePeriodic()` |
| 12 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `createScheduleOnce()` |
| 13 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `activeMaintenanceFilter()` |
| 14 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `suspendedMaintenanceFilter()` |

### `SDPOD_ORG_ROLE_148` — ×13 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforProblemFromUserForTechnician()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromRegionForChange()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromRegionForChange()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromOrganization()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromSite()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromSiteForChange()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromGroupForChange()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromGroupForChange()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromUserForChangeRequester()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforChangeFromUserForChangeOwner()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromUserForChangeRequester()` |
| 13 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforChangeFromUserForChangeOwner()` |

### `SDPOD_Quartz_video_fb_0053,SDPOD_Quartz_video_fb_0054,SDPOD_Quartz_video_fb_0055,SDPOD_Quartz_video_fb_0056,SDPOD_Quartz_video_fb_0057,SDPOD_Quartz_video_fb_0058` — ×13 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createRequest()` |
| 2 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createAsset()` |
| 3 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createChange()` |
| 4 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createProblem()` |
| 5 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createProject()` |
| 6 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createContract()` |
| 7 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createRelease()` |
| 8 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createPurchase()` |
| 9 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createRequestMaintenance()` |
| 10 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createCategory()` |
| 11 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createCmdb()` |
| 12 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createReport()` |
| 13 | `com/zoho/automater/selenium/modules/general/feedback/Feedback.java` | `createTaskActivity()` |

### `SDPOD_ORG_ROLE_011` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinOrganization()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinRegion()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinRegion()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinDepartment()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinDepartment()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinSite()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinSite()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinGroup()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinGroup()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleSingleTransferUserinUser()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `OrgRoleMultipleTransferUserinUser()` |

### `SDPOD_ORG_ROLE_010` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinOrganization()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinRegion()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinRegion()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinDepartment()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinDepartment()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinSite()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinSite()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinGroup()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinGroup()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleSingleDissociateinUser()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleMultipleDissociateinUser()` |

### `SDPOD_ORG_ROLE_172` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromRegionforProblem()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromRegionForProblem()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromOrganization()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromSiteForProblem()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromSiteForProblem()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromGroupForProblem()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromGroupForProblem()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromUserForReportedBy()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersApprovalbyTriggerforProblemFromUserforTechnician()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromUserForReportedBy()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersApprovalbyTriggerforProblemFromUserForTechnician()` |

### `SDPOD_ORG_ROLE_051` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforChangeFromRegionForChange()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforChangeFromRegionForChange()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforChangeFromOrganization()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforChangeFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforChangeFromSiteForChange()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforChangeFromSiteForChange()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforChangeFromGroupForChange()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforChangeFromGroupForChange()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforChangeFromUserForChangeRequester()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforChangeFromUserForChangeOwner()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforChangeFromUserForChangeRequester()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforChangeFromUserForChangeOwner()` |

### `SDPOD_ORG_ROLE_038` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromRegionForRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromRegionForRequester()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromRegionForTechnician()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromSiteForRequest()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromSiteForRequester()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromSiteForTechnician()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromDepartmentForRequest()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromDepartmentForTechnician()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationSLAforRequestFromGroupForRequest()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromUserForRequester()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbySLAforRequestFromUserForTechnician()` |

### `SDPOD_ORG_ROLE_195` — ×12 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForOrgaization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForRegionofRequest()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForRegionofRequester()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForRegionofTechnician()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForSiteofRequest()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForSiteofRequester()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForSiteofTechnician()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForGroupofRequest()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForDepartmentofRequest()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForDepartmentofTechnician()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForUsertofRequester()` |
| 12 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUserfornotesAndmentionForUserofTechnician()` |

### `SDPOD_ORG_ROLE_073` — ×11 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforProblemFromRegionForProblem()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforProblemFromRegionForProblem()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforProblemFromOrganization()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforProblemFromOrganization()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforProblemFromSiteForProblem()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforProblemFromSiteForProblem()` |
| 7 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforProblemFromGroupForProblem()` |
| 8 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforProblemFromGroupForProblem()` |
| 9 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforProblemFromUserForReportedBy()` |
| 10 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationbyTriggerforProblemFromUserForTechnician()` |
| 11 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationbyTriggerforProblemFromUserForTechnicianForReportedBy()` |

### `SDPOD_AUTO_CH_WORKFLOW_00` — ×10 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsIFForRelease()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsWaitForForRelease()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeisSwitchForRelease()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsNotificationForRelease()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `ccreateSingleNodeIsApprovalForRelease()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `ccreateSingleNodeIsFieldUpdateForRelease()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsTaskForRelease()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsForkForRelease()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createSingleNodeIsJoinForRelease()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `checkInvalidWorkflowForRelease()` |

### `SDPOD_AUTO_SR_WORKFLOW_00` — ×10 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsIFForServiceRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsWaitForForServiceRequest()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsSwitchForServiceRequest()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsNotificationForServiceRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsApprovalForServiceRequest()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsFieldUpdateForServiceRequest()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsTaskForServiceRequest()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsForkForServiceRequest()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createSingleNodeIsJoinForServiceRequest()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `serviceRequestEditWorkflow()` |

### `CH1753_REQUEST_LV_PERFORMANCE` — ×10 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `linkRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyOnholdFilter()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `noCancellationFlagCheck()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `kanbanViewCheckWithProjectID()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `wokflowIconCheckInColumnChooser()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `linkRequest()` |
| 7 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyOnholdFilter()` |
| 8 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `noCancellationFlagCheck()` |
| 9 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `kanbanViewCheckWithProjectID()` |
| 10 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `wokflowIconCheckInColumnChooser()` |

### `SDPOD_AUTO_SOL_DV_158` — ×10 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPublicSolutionFromdetailView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPublicSolutionFromdetailView()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPublicSolutionWithTechGroup()` |
| 4 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPrivSolutionWithTechGroup()` |
| 5 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteUnAppPublicSolutionWithTechGroup()` |
| 6 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteUnAppPrivSolutionWithTechGroup()` |
| 7 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreTrashDeleteAppPublicSolutionWithTechGroup()` |
| 8 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreTrashDeleteUnAppPublicSolutionWithTechGroup()` |
| 9 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreTrashDeleteAppPrivSolutionWithTechGroup()` |
| 10 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreTrashDeleteUnAppPrivSolutionWithTechGroup()` |

### `SDPOD_AUTO_IR_WORKFLOW_00` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsIFForIncidentRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsWaitForForIncidentRequest()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsSwitchForIncidentRequest()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsNotificationForIncidentRequest()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsFieldUpdateForIncidentRequest()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsTaskForIncidentRequest()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsForkForIncidentRequest()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createSingleNodeIsJoinForIncidentRequest()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `incidentRequestEditWorkflow()` |

### `SDPOD_Release_TPT_1813` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `deleteTaskFromListViewPlanningStage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleasePlanningStage()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseDevelopmentStage()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseTestingStage()` |
| 5 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseUATStage()` |
| 6 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseDeploymentStage()` |
| 7 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseTrainingStage()` |
| 8 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseReviewStage()` |
| 9 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `verifyTaskInReleaseClosureStage()` |

### `SDPOD_PR_Trash_095_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `openTaskDetailsFromProblemTrash()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `openTaskDetailsFromProblemTrash()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `openTaskDetailsFromProblemTrash()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `openTaskDetailsFromProblemTrash()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `openTaskDetailsFromProblemTrash()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `openTaskDetailsFromProblemTrash()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `openTaskDetailsFromProblemTrash()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `openTaskDetailsFromProblemTrash()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `openTaskDetailsFromProblemTrash()` |

### `SDPOD_PR_Trash_096_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTaskActionsProblemTrash()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyTaskActionsProblemTrash()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyTaskActionsProblemTrash()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyTaskActionsProblemTrash()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyTaskActionsProblemTrash()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyTaskActionsProblemTrash()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyTaskActionsProblemTrash()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyTaskActionsProblemTrash()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyTaskActionsProblemTrash()` |

### `SDPOD_PR_Trash_097_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTaskNotPresentInHome()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyTaskNotPresentInHome()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyTaskNotPresentInHome()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyTaskNotPresentInHome()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyTaskNotPresentInHome()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyTaskNotPresentInHome()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyTaskNotPresentInHome()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyTaskNotPresentInHome()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyTaskNotPresentInHome()` |

### `SDPOD_PR_Trash_098_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTaskPresentInHome()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyTaskPresentInHome()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyTaskPresentInHome()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyTaskPresentInHome()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyTaskPresentInHome()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyTaskPresentInHome()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyTaskPresentInHome()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyTaskPresentInHome()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyTaskPresentInHome()` |

### `SDPOD_PR_Trash_099_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTaskFiltersProblemTrash()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyTaskFiltersProblemTrash()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyTaskFiltersProblemTrash()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyTaskFiltersProblemTrash()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyTaskFiltersProblemTrash()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyTaskFiltersProblemTrash()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyTaskFiltersProblemTrash()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyTaskFiltersProblemTrash()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyTaskFiltersProblemTrash()` |

### `SDPOD_PR_Trash_037_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTrashedProblemInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyTrashedProblemInDashboard()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyTrashedProblemInDashboard()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyTrashedProblemInDashboard()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyTrashedProblemInDashboard()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyTrashedProblemInDashboard()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyTrashedProblemInDashboard()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyTrashedProblemInDashboard()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyTrashedProblemInDashboard()` |

### `SDPOD_PR_Trash_041_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyRestoredProblemInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyRestoredProblemInDashboard()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyRestoredProblemInDashboard()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyRestoredProblemInDashboard()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyRestoredProblemInDashboard()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyRestoredProblemInDashboard()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyRestoredProblemInDashboard()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyRestoredProblemInDashboard()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyRestoredProblemInDashboard()` |

### `SDPOD_PR_Trash_071_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyCopiedProblemInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyCopiedProblemInDashboard()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyCopiedProblemInDashboard()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyCopiedProblemInDashboard()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyCopiedProblemInDashboard()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyCopiedProblemInDashboard()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyCopiedProblemInDashboard()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyCopiedProblemInDashboard()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyCopiedProblemInDashboard()` |

### `SDPOD_PR_Trash_168_1_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `globalSearchTrashedProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `globalSearchTrashedProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `globalSearchTrashedProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `globalSearchTrashedProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `globalSearchTrashedProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `globalSearchTrashedProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `globalSearchTrashedProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `globalSearchTrashedProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `globalSearchTrashedProblem()` |

### `SDPOD_PR_Trash_168_2_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `globalSearchRestoredProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `globalSearchRestoredProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `globalSearchRestoredProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `globalSearchRestoredProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `globalSearchRestoredProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `globalSearchRestoredProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `globalSearchRestoredProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `globalSearchRestoredProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `globalSearchRestoredProblem()` |

### `SDPOD_PR_Trash_138_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyPLCinCopyProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyPLCinCopyProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyPLCinCopyProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyPLCinCopyProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyPLCinCopyProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyPLCinCopyProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyPLCinCopyProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyPLCinCopyProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyPLCinCopyProblem()` |

### `SDPOD_PR_Trash_139_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyPLCinRestoredProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyPLCinRestoredProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyPLCinRestoredProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyPLCinRestoredProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyPLCinRestoredProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyPLCinRestoredProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyPLCinRestoredProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyPLCinRestoredProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyPLCinRestoredProblem()` |

### `SDPOD_PR_Trash_140_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyRevokedPLCinCopyProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyRevokedPLCinCopyProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyRevokedPLCinCopyProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyRevokedPLCinCopyProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyRevokedPLCinCopyProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyRevokedPLCinCopyProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyRevokedPLCinCopyProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyRevokedPLCinCopyProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyRevokedPLCinCopyProblem()` |

### `SDPOD_PR_Trash_141_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyRevokedPLCinRestoredProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyRevokedPLCinRestoredProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyRevokedPLCinRestoredProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyRevokedPLCinRestoredProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyRevokedPLCinRestoredProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyRevokedPLCinRestoredProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyRevokedPLCinRestoredProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyRevokedPLCinRestoredProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyRevokedPLCinRestoredProblem()` |

### `SDPOD_PR_Trash_142_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyPLCinCopyProblemRHS()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyPLCinCopyProblemRHS()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyPLCinCopyProblemRHS()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyPLCinCopyProblemRHS()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyPLCinCopyProblemRHS()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyPLCinCopyProblemRHS()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyPLCinCopyProblemRHS()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyPLCinCopyProblemRHS()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyPLCinCopyProblemRHS()` |

### `SDPOD_PR_Trash_160_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyCustomerCopyProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyCustomerCopyProblem()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyCustomerCopyProblem()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyCustomerCopyProblem()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyCustomerCopyProblem()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyCustomerCopyProblem()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyCustomerCopyProblem()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyCustomerCopyProblem()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyCustomerCopyProblem()` |

### `SDPOD_PR_Trash_161_PB` — ×9 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyCustomerFilterProblemTrash()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyCustomerFilterProblemTrash()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyCustomerFilterProblemTrash()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `verifyCustomerFilterProblemTrash()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyCustomerFilterProblemTrash()` |
| 6 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyCustomerFilterProblemTrash()` |
| 7 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `verifyCustomerFilterProblemTrash()` |
| 8 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewEdit.java` | `verifyCustomerFilterProblemTrash()` |
| 9 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewOnly.java` | `verifyCustomerFilterProblemTrash()` |

### `SDPOD_AUTO_RL_TRIGGER_` — ×8 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `checkReleaseTriggerInCreate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `checkReleaseTriggerInEdit()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskInCreate()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskInEdit()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsTaskInDelete()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsAllWorklogInCreate()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsAllWorklogInEdit()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsAllWorklogInDelete()` |

### `SDPOD_ChatGPT_Generating Custom Function _041` — ×8 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeDisabled()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeEnabled()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeDisabledBRActions()` |
| 4 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeEnabledBRActions()` |
| 5 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeDisabledTriggerLCTimer()` |
| 6 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeEnabledTriggerLCTimer()` |
| 7 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeDisabledCustomMenu()` |
| 8 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCopyCodeEnabledCustomMenu()` |

### `SDPOD_Custum_Report_048, SDPOD_Custum_Report_034` — ×8 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentWithTasksDesc()` |
| 2 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesWithTasksDesc()` |
| 3 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemWithTasksDesc()` |
| 4 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectWithTasksDesc()` |
| 5 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectWithMilestonesTasksDesc()` |
| 6 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeWithTasksDesc()` |
| 7 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseWithTasksDesc()` |
| 8 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralWithTasksDesc()` |

### `SDPOD_REQUEST_SDGT_PERF_011` — ×8 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requesterHeadPickerRequestCreation()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requesterHeadPickerRequestEdit()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `requesterHeadPickerRequestCreation()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `requesterHeadPickerRequestEdit()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `requesterHeadPickerRequestCreation()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `requesterHeadPickerRequestEdit()` |
| 7 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requesterHeadPickerRequestCreation()` |
| 8 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requesterHeadPickerRequestEdit()` |

### `SDPOD_ChatGPT_Generating Custom Function _001` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `codeGenPopupInApplyConditionChatGPT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `copyCodeEnabledInApplyConditionChatGPT()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `isCodeGeneratedInApplyConditionChatGPT()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `codeGenPopupInActionsCFChatGPT()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `copyCodeEnabledInActionsCFChatGPT()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `isCodeGeneratedInActionsCFChatGPT()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/Timer.java` | `checkForPromptSuggestedSection()` |

### `SDPOD_ChatGPT_Generating Custom Function _044` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCodeGenerated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `checkForPromptSuggestedSection()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCodeGeneratedBRActions()` |
| 4 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `checkForPromptSuggestedSectionBRActions()` |
| 5 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `checkForPromptSuggestedSectionTriggerLCTimer()` |
| 6 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `isCodeGeneratedCustomMenu()` |
| 7 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `checkForPromptSuggestedSectionCustomMenu()` |

### `SDPOD_HEADER_TAB_011` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkResetInNavigationAndFooterSettingsPageRequesterHeader()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkResetInNavigationAndFooterSettingsPageRequesterFooter()` |
| 3 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkLockAndHideOrShowIconInNavigationAndFooterSettingsPageRequesterHeader()` |
| 4 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `hideOrShowIconInNavigationAndFooterSettingsPageRequesterFooter()` |
| 5 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSaveAndCancelInNavigationAndFooterSettingsPageRequesterFooter()` |
| 6 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSortableAndMoreTabsInNavigationAndFooterSettingsPageRequesterHeader()` |
| 7 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSortableAndMoreTabsInNavigationAndFooterSettingsPageRequesterFooter()` |

### `SDPOD_ASSET_CUS_FIL_001` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInComputer()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInMobileDevices()` |
| 3 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInPrinters()` |
| 4 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInRouters()` |
| 5 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInSwitches()` |
| 6 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInProjector()` |
| 7 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `presenceOfCustomFilterInScanner()` |

### `SDPOD_PO_Contract_Enhancements_430` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `createLookUpForContractWithSite()` |
| 2 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `createLookUpForContractWithTechnician()` |
| 3 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `createLookUpForContractWithVendor()` |
| 4 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createLookupWithDepartmentForPO()` |
| 5 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createLookupWithSiteForPO()` |
| 6 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createLookupWithTechnicianForPO()` |
| 7 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createLookupWithVendorForPO()` |

### `SDPOD_Custum_Report_048, SDPOD_Custum_Report_011` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralTasksCommentAndReply()` |
| 2 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentWorklog()` |
| 3 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServiceWorklog()` |
| 4 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemWorklog()` |
| 5 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeWorklog()` |
| 6 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseWorklog()` |
| 7 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectWorklog()` |

### `SDPOD_Custum_Report_048, SDPOD_Custum_Report_005, SDPOD_Custum_Report_037` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentTaskWorklogDesc()` |
| 2 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesTaskWorklogDesc()` |
| 3 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProblemTaskWorklogDesc()` |
| 4 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForProjectTaskWorklogDesc()` |
| 5 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForChangeTaskWorklogDesc()` |
| 6 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseTaskWorklogDesc()` |
| 7 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralTaskWorklogDesc()` |

### `SDPOD_COLLECTION_FIELDS_INFO_TC021` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAssociatedAssetsPresentInViewDetailsPopup()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `disassociateAssetFromAssetFieldViaPopup()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `disassociateAssetFromAssetFieldViaIcon()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAssociatedCIPresentInViewDetailsPopup()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `disassociateAssetFromAssetFieldViaPopup()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `disassociateAssetFromAssetFieldViaIcon()` |
| 7 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyAssetNavigateToAssetDetailsPageViaViewAssetDetailsIconInPopup()` |

### `SDPOD_SOL_VERSION_CTRL_016` — ×7 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToRejectDraft()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToSendDraft()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToDeleteDraft()` |
| 4 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToUpdateSolutionViaDraftMerge()` |
| 5 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToRestoreVersion()` |
| 6 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToRestoreButUnapprovedVersion()` |
| 7 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToRestoreAndapprovedVersion()` |

### `SDPOD_ORG_ROLE_001, SDPOD_ORG_ROLE_002, SDPOD_ORG_ROLE_004` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinOrgLevel()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinRegionLevel()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinDepartmentLevel()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinSiteLevel()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinGroupLevel()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormCreateValidationinUserLevel()` |

### `SDPOD_ORG_ROLE_005, SDPOD_ORG_ROLE_006, SDPOD_ORG_ROLE_007, SDPOD_ORG_ROLE_013, SDPOD_ORG_ROLE_014` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinRegion()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinDepartment()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinSite()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinGroup()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `orgRoleFormEditValidationinUser()` |

### `SDPOD_ORG_ROLE_008` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinRegion()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinDepartment()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinSite()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinGroup()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumSingleUserAssociationinUser()` |

### `SDPOD_ORG_ROLE_009` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinRegion()` |
| 3 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinDepartment()` |
| 4 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinSite()` |
| 5 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinGroup()` |
| 6 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `maximumMultipleUserAssociationinUser()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_051` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `editAnnouncementTemplateInAdmin()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `deleteAnnouncementTemplateInAdmin()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `disableAnnouncementTemplateInAdmin()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `copyAnnouncementTemplateInAdmin()` |
| 5 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `makeAsDefaultAnnouncementTemplateInAdmin()` |
| 6 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `announcementTemplateSystemLogTrace()` |

### `SDPLIVE_IH_5` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/changetask/ImplementationTask.java` | `verifyValidationMessageInImplementationTaskName()` |
| 2 | `com/zoho/automater/selenium/modules/changes/changetask/PlanningTask.java` | `verifyValidationMessageInPlanningTaskName()` |
| 3 | `com/zoho/automater/selenium/modules/changes/changetask/ReleaseTask.java` | `verifyValidationMessageInReleaseTaskName()` |
| 4 | `com/zoho/automater/selenium/modules/changes/changetask/ReviewTask.java` | `verifyValidationMessageInReviewTaskName()` |
| 5 | `com/zoho/automater/selenium/modules/changes/changetask/SubmissionTask.java` | `verifyValidationMessageInSubmissionTaskName()` |
| 6 | `com/zoho/automater/selenium/modules/changes/changetask/UATTask.java` | `verifyValidationMessageInUATTaskName()` |

### `SDPOD_AUTO_PROJ_LV_004` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `createUsingDefaultProjectTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `verifyAbleToSelectProjectRequesterViaIcon()` |
| 3 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `verifyDeleteButtonNotPresentInProjectListview()` |
| 4 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `verifyImportProjectsButtonNotPresentInProjectListview()` |
| 5 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `verifyListviewIconNotPresentInProjectListview()` |
| 6 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `verifyDetailviewIconNotPresentInProjectListview()` |

### `SDP_REQ_LS_AAA101` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/Request.java` | `favorite_Unpin_toScreen()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `spotEditStatusInDetailView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterPinFavorite()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `favoritePinToScreen()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterPinFavorite()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `favoritePinToScreen()` |

### `SDP_REQ_DV_AAA149` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `changeInitiatedRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `changeInitiatedRequest()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `changeCausedByRequest()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `changeInitiatedRequest()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `changeCausedByRequest()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `changeInitiatedRequest()` |

### `SDPOD_Req_Sol_049, SDPOD_Req_Sol_013` — ×6 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForApprovedSolutionDetach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForUnApprovedSolutionDetach()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForApprovalPendingSolutionDetach()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForApprovedSolutionDetach()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForUnApprovedSolutionDetach()` |
| 6 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForApprovalPendingSolutionDetach()` |

### `SDPOD_AUTO_AP_LV_0003` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `createProductTypeandVerify()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `createProductTypeinUIandVerifyinUI()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkDeletButtonisPresentinDefaultProductType()` |
| 4 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteAccessPointAsset()` |
| 5 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteAccessPointAsset()` |

### `SDPOD_AUTO_SYNCRULE_1` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `organizeSyncRules()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeAssetSyncRuleCreateAccessPointsfromCIs()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeAssetSyncRuleDeleteCI()` |
| 4 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeAssetSyncRuleDeleteAccessPoints()` |
| 5 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeAssetSyncRuleWithCreateRelationship()` |

### `SDPOD_ChatGPT_Generating Custom Function _030` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `codeGeneratorPopup()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `codeGeneratorPopupBRActions()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `codeGeneratorCustomMenu()` |
| 4 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `CodeGeneratorBtnCustomMenu()` |
| 5 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `codeGeneratorPopupCustomMenu()` |

### `SDPOD_HEADER_TAB_010` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkResetInNavigationAndFooterSettingsPageTechnicianFooter()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkLockAndHideOrShowIconInNavigationAndFooterSettingsPageTechnicianHeader()` |
| 3 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSaveAndCancelInNavigationAndFooterSettingsPageTechnicianHeader()` |
| 4 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSortableAndMoreTabsInNavigationAndFooterSettingsPageTechnicianHeader()` |
| 5 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSortableAndMoreTabsInNavigationAndFooterSettingsPageTechnicianFooter()` |

### `SDPOD_Test_Credentials_005` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `validateWindowsCredential()` |
| 2 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `validateVMwareCredential()` |
| 3 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `validateSSHCredential()` |
| 4 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `validateSNMPCredential()` |
| 5 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `validateSNMPV3Credential()` |

### `SDP_REQ_DV_AAA036` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/replytemplate/ReplyTemplate.java` | `checkEmailSignautureInTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/replytemplate/ReplyTemplate.java` | `checkEmailSignautureInReply()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editResolution()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `checkEmailSignautureInReply()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editResolution()` |

### `SDPOD_SERVICE_CATEGORY_015,SDPOD_SERVICE_CATEGORY_017` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyTemplatesDisplayedInSearchTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyServiceCategoriesAndTemplatesDisplayedInAssetDetailviewSearchTemplate()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyIncidentTemplatesDisplayedInSearchTemplateInReportAnIssuePopup()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyServiceTemplatesDisplayedInSearchTemplateInRequestAServicePopup()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyDotIconAndBreadcrumpDropdownListForServiceCategory()` |

### `SDPOD_AUTO_AUDIT_LV_0008` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkAuditSubtabinUserSelf()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `markAsMissingViaPendingSubtab()` |
| 3 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `markAsMissingViaAuditedSubtab()` |
| 4 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkInProgressandCancelFilter()` |
| 5 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkUnderReviewandEndFilter()` |

### `SDPOD_AUTO_PB_LV_013` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `closedProblemsFilterListview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyClosedProblemExport()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyCompletedProblemExport()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyClosedProblemExport()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyCompletedProblemExport()` |

### `SDPOD_PR_Trash_107_PB` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `deleteProblemInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `deleteProblemInDashboard()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditDelete.java` | `deleteProblemInDashboard()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `deleteProblemInDashboard()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewDelete.java` | `deleteProblemInDashboard()` |

### `SDPOD_PR_Trash_108_PB` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `copyProblemInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `copyProblemInDashboard()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `copyProblemInDashboard()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `copyProblemInDashboard()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `copyProblemInDashboard()` |

### `SDPOD_PR_Trash_159_PBROLES_VIEWADD` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyCustomerdataCopyProblemPopup()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddDelete.java` | `verifyCustomerdataCopyProblemPopup()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddEdit.java` | `verifyCustomerdataCopyProblemPopup()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyCustomerdataCopyProblemPopup()` |
| 5 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsViewAdd.java` | `verifyCustomerdataCopyProblemPopup()` |

### `SDPOD_CART2502_PO_1` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyEmailInPoForm()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyEmailInPoDetailPage()` |
| 3 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyEmailInPoEditPage()` |
| 4 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyEmailInPoTemplateAdd()` |
| 5 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyEmailInPoTemplateEdit()` |

### `SDP_CHECK_016` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `importUserFromZohoOrg()` |
| 2 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `importUserFromCSV()` |
| 3 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `importProjectFromMpp()` |
| 4 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `customWidgetCheck()` |
| 5 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `jiraIntegration()` |

### `SDP_REQ_LS_AAA010` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `duplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `submitForApprovalActionsInDetailView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `submitForApprovalActionsInDetailView()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `duplicateRequest()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `submitForApprovalActionsInDetailView()` |

### `SDP_REQ_LS_AAA104` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `startedTimerListview()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `stoppedTimerListview()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addTaskInDetailView()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `startedTimerListview()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `stoppedTimerListview()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_025` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedBySplitRequestSDSiteadmin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByCopiedTemplate()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedBySplitRequestSDSiteadmin()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyLastupdatedByCopiedTemplate()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedByCopiedTemplate()` |

### `SDPOD_Req_Sol_049, SDPOD_Req_Sol_018` — ×5 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForApprovedSolutionAttach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForUnApprovedSolutionAttach()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForApprovalPendingSolutionAttach()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForApprovedSolutionAttach()` |
| 5 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForUnApprovedSolutionAttach()` |

### `SDPOD_Elango_Testcase_001` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `enableZohoFlowIntegrations()` |
| 2 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `verifyZapierLogoInDarkMode()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/customactions/CustomActions.java` | `ZohoFlowCustomAction()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `ZohoFlowActionTrigger()` |

### `SDPOD_CH_CD_360` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/cdetection/FreezeWindow.java` | `createChangeFreezeWindowAllChanges()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/cdetection/FreezeWindow.java` | `createChangeFreezeWindowChangeCreation()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/cdetection/FreezeWindow.java` | `createChangeFreezeWindowCodeCoverageCase()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/cdetection/FreezeWindow.java` | `createChangeMantenanceWindowCodeCoverageCase()` |

### `SPOD_Request_UDF_Enhancement_092` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAbleToCloseMultipleRequestAssetLookup()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAbleToAssignMultipleRequestAssetLookup()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/roles/RequestSDAdminWithSDCordinator.java` | `verifyAbleToAssignMultipleRequestAssetLookup()` |
| 4 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/roles/RequestSDAdminWithSDCordinator.java` | `verifyAbleToCloseMultipleRequestAssetLookup()` |

### `SDPOD_ChatGPT_Generating Custom Function _039` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `presenceOfGenerateBtn()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `presenceOfGenerateBtnBRActions()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `presenceOfGenerateBtnTriggerLCTimer()` |
| 4 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `presenceOfGenerateBtnCustomMenu()` |

### `SDPOD_SUBFORM_UDF_REQUEST_105` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `attachmnetUDFWithImageInCustomModules()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `attachmentUDFWithXlsxInCustomModules()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `attachmentUDFWithPdfInCustomModules()` |
| 4 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `attachmentUDFWithVideoInCustomModules()` |

### `CreatorDashboardValidator.java` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `requesterPortalCustomizationCodeCoverageCase()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `requesterPortalCustomizationCodeCoverageCaseNewTemplate()` |
| 3 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/roles/RequesterPortalCustomizationRequester.java` | `requesterPortalCustomizationCodeCoverageCase()` |
| 4 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/roles/RequesterPortalCustomizationRequester.java` | `requesterPortalCustomizationCodeCoverageCaseNewTemplate()` |

### `SDPOD_AUTO_IT_001` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `createRequesttemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `createIncidentTemplateWithImage()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/roles/Requester.java` | `verifyTemplatePresentWithImageInReportAnIssue()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/roles/Requester.java` | `verifyTemplatePresentWithImageInRequesterPortalSearch()` |

### `SDPOD_TLHCA_022` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkRequestFormButtonInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkRequestDetailsButtonInReqView()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `checkRequestFormButtonInReqView()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `checkRequestDetailsButtonInReqView()` |

### `SDPOD_TLHCA_141` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardContentPresentInRequesterRequestForm()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardContentPresentInRequesterRequestDetailsPage()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardContentPresentInRequesterSRForm()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardContentPresentInRequesterSRDetailsPage()` |

### `SDPOD_Problem_Layouts_064` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `addAttachmentForImpactDetails()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `addAttachmentForRolloutPlan()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `addAttachmentForBackoutPlan()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `addAttachmentForChecklist()` |

### `SDP_REQ_DV_AAA035` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/replytemplate/ReplyTemplate.java` | `addReplyfromTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/resolutiontemplate/ResolutionTemplate.java` | `addResolutionfromTemplate()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addResolution()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addResolution()` |

### `SDPOD_SERVICE_CATALOG_CUSTOMIZATION_002` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `createServiceCategoryWithImage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `createServiceCategoryWithUploadImage()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `editServiceCategoryWithUploadImage()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `createServiceTemplateNameWithUploadImage()` |

### `SDPOD_SERVICE_CATALOG_CUSTOMIZATION_023` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `createServiceCategoryWithImage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `createServiceCategoryWithUploadImage()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `editServiceCategoryWithUploadImage()` |
| 4 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `createServiceTemplateNameWithUploadImage()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_005,SDPOD_ANNOUNCEMENT_PHASE2_006` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInBannerTechnicianLogin()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInPushNotificationTechnicianLogin()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInDetailsPageTechnicianLogin()` |
| 4 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInActionTechnicianLogin()` |

### `SDPOD_DASHBOARD_WIDGET_PEEK_VIEW_338_1` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `sendApprovalInSmartView()` |
| 2 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `checkNeedMoreInfo()` |
| 3 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `checkApproverRequest()` |
| 4 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `checkRejectRequest()` |

### `SDPLIVE_SDC_TAC_0038` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `verifyTechDetailsSDCoordinator()` |
| 2 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `techDeatilsSectioSDCoordinatorn()` |
| 3 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `verifyTechDetailsSDAdmin()` |
| 4 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `verifyTechDetailsSDSiteAdmin()` |

### `SDPOD_AUTO_PB_DV_022` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `addAttachmentsDetailsTabDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editKnownErrorToNoRHSDetailview()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `methodName()` |
| 4 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `addImpactDetailsDetailview()` |

### `SDPOD_Custum_Report_048, SDPOD_Custum_Report_011, SDPOD_Custum_Report_017, SDPOD_Custum_Report_018, SDPOD_Custum_Report_019, SDPOD_Custum_Report_020, SDPOD_Custum_Report_021, SDPOD_Custum_Report_022, SDPOD_Custum_Report_023, SDPOD_Custum_Report_024, SDPOD_Custum_Report_025, SDPOD_Custum_Report_026, SDPOD_Custum_Report_038, SDPOD_Custum_Report_051, SDPOD_Custum_Report_052, SDPOD_Custum_Report_061` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForIncidentsTasksComment()` |
| 2 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForServicesTasksComment()` |
| 3 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForReleaseTasksComment()` |
| 4 | `com/zoho/automater/selenium/modules/reports/report/Report.java` | `customReportForGeneralTasksComment()` |

### `SDP_REQ_LS_AAA069` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `completedRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `myCompletedRequestFilters()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `completedRequestFilters()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `myCompletedRequestFilters()` |

### `SDP_REQ_LS_AAA031` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `pickupRequestInListView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `bulkPickupRequestInListView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `pickupRequestInListView()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `bulkPickupRequestInListView()` |

### `SDP_REQ_DV_AAA048` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `reminderPopupverify()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `cancelinReminder()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `reminderPopupverify()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `cancelinReminder()` |

### `SDP_REQ_DV_AAA110` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `updateAssetHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `updateAssetHistoryVerification()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `updateAssetHistoryVerification()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `updateAssetHistoryVerification()` |

### `57242-issueid` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyChangeDetailviewInChangeCausedByRequestPopupWindow()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyChangeDetailviewInChangeInitiatedRequestPopupWindow()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyChangeDetailviewInChangeInitiatedRequestPopupWindow()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyChangeDetailviewInChangeCausedByRequestPopupWindow()` |

### `SDP_REQ_DV_AAA158` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `iconReplyRequestInDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `iconReplyAllRequestInDetailView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `iconReplyRequestInDetailView()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `iconReplyAllRequestInDetailView()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_022` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByEditBulkrequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByEditBulkrequest()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyLastupdatedBySplitRequest()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedBySplitRequest()` |

### `SDPOD_COLLECTION_FIELDS_INFO_TC001` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `assignMultipleAssetsInSpotEditAssetField()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `checkViewDetailsPresentInAssetField()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `assignMultipleCIInRequestSpotEditCIField()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `checkViewDetailsPresentInCIField()` |

### `SDPOD_COLLECTION_FIELDS_INFO_TC026` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `assignMultipleAssetsInRequesterFormInAssetField()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyDisassociateButtonNotPresentInAssetPopupInRequesterLogin()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `assignMultipleCIInRequesterFormInCIField()` |
| 4 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyDisassociateButtonNotPresentInCIPopupInRequesterLogin()` |

### `SDPOD_Req_Sol_068, SDPOD_Req_Sol_069, SDPOD_Req_Sol_070, SDPOD_Req_Sol_071, SDPOD_Req_Sol_072, SDPOD_Req_Sol_073` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `ReferredInRequestsuiteviewforapprovedSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `ReferredInRequestsuiteviewforunapprovedSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `ReferredInRequestsuiteviewforapprovalpendingSolution()` |
| 4 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `ReferredInRequestsuiteviewforrejectsolution()` |

### `SDPOD_KB_Article_010` — ×4 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `isSolutionGeneratorbuttonPresent()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `solutionGeneratorInNewSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `isSolutionGeneratorbuttonPresent()` |
| 4 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `solutionGeneratorInNewSolution()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_032` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/BusinessRules.java` | `verifylastUpdatedByFieldinIncidentBR()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/CustomerIssuesinBusinessRule.java` | `verifylastUpdatedByFieldinIncidentBR()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `verifylastUpdatedByFieldinIncidentBR()` |

### `SDPOD_QEvent_001` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `notificationStatusCriteriaCheckInIncidentBR()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `notificationStatusCriteriaCheckInServiceBR()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `notificationStatusCriteriaCheckInTrigger()` |

### `SDPOD_AUTO_RL_TRIGGER_324` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsReleaseWorklogInCreate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsReleaseWorklogInEdit()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createReleaseTriggerWithSubentityIsReleaseWorklogInDelete()` |

### `SDPOD_SYNC_RULE_ENC_009,SDPOD_SYNC_RULE_ENC_028,SDPOD_SYNC_RULE_ENC_033-040,` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `newUserSyncRuleForRequesterWithAllActions()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `newUserSyncRuleForTechnicianWithAllActions()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `newUserSyncRuleForAllUserWithAllActions()` |

### `SDPOD_SERVICE_CATEGORY_022` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/contractmanagement/contractconfiguration/ContractConfiguration.java` | `verifyServiceTemplateintoContractExpiryRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/contractmanagement/contractconfiguration/ContractConfiguration.java` | `verifyIncidentTemplateintoContractExpiryRequest()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/contractmanagement/contractconfiguration/ContractConfiguration.java` | `verifyServiceCategoryAndTemplatesDisplayedInContractExpirySearchTemplate()` |

### `SDPOD_Request_Mode_1.4.1_009` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/helpdesk/mode/Mode.java` | `verifyMobileApplicationModeIsPresent()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/helpdesk/mode/Mode.java` | `verifyDeleteOptionShouldNotPresentInMobileApplicationMode()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/helpdesk/mode/Mode.java` | `verifyEmailModePopupShouldOpen()` |

### `SDPOD_RM_STATUS_EN_056` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `verifyClosedReleaseNotDisplayedForAssociationInChange()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `approvalOptionShoudlNotbeDisplayedForClosedReleaseCompleted()` |
| 3 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `approvalOptionShoudlNotbeDisplayedForClosedReleaseFailed()` |

### `SDPOD_SUBFORM_UDF_REQUEST_050` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `ipAddressUDFWithDottedDecimalNotationInCustomModules()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `ipAddressUDFWithCanonicalNotationInCustomModules()` |
| 3 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `ipAddressUDFWithExpandedNotationInCustomModules()` |

### `SDPOD_HEADER_TAB_009` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkResetAndCloseInOrganizeNavigationTabs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkSaveAndCancelInOrganizeNavigationTabs()` |
| 3 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkLockAndHideOrShowIconInOrganizeNavigationTabs()` |

### `SDPOD_DEDUPLICATION_004` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `addNewProbe()` |
| 2 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `addDomainScan()` |
| 3 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `addNetworkScan()` |

### `SDPOD_TLHCA_068` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardNotPresentInRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardNotPresentInRequestdetails()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardNotPresentInRequestdetails()` |

### `SDPOD_OT_014` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `verifyAlertWhileMoveUpInOrganizeMilestoneTaskInProjectTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `assignSingleTaskToMilestoneInProjectTemplate()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `assignMultipleTaskToMilestoneInProjectTemplate()` |

### `SDPOD_SERVICE_CATEGORY_006` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyServiceCategoryAndTemplatesAreSeparateView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `showIncidentTemplatesExpandCollapse()` |
| 3 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `showIncidentTemplatesOnTopAndBelow()` |

### `SDPOD_FGA_059,SDPOD_FGA_199` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/finegrainedaccess/AssetFGA.java` | `assetFGAWithSDAssetManagerPermission()` |
| 2 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/finegrainedaccess/AssetFGA.java` | `assetFGAWithAssetConfigPermission()` |
| 3 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/finegrainedaccess/AssetFGA.java` | `assetFGAWithSDAdminPermission()` |

### `SDPOD_AUTO_AP_LV_0002` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editAccessPointAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchAssetProductviaGlobalSearchBox()` |
| 3 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editAccessPointAsset()` |

### `SDPOD_SERVICE_CATEGORY_023` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createIncidentFromAssetActionsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createServiceRequestFromAssetActionsDetailview()` |
| 3 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyServiceCategoriesAndTemplatesDisplayedInCMDBDetailviewSearchTemplate()` |

### `SDP-CHG-MOD-1242` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/CABEvaluationStage.java` | `verifyCABApprovalButtonPresentInViewPopupFromListview()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/CABEvaluationStage.java` | `approveCABApprovalInDetailview()` |
| 3 | `com/zoho/automater/selenium/modules/changes/change/CABEvaluationStage.java` | `rejectCABApprovalInDetailview()` |

### `SDPOD_AUTO_CH_LV_001` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `createUsingGeneralTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyAbleToSelectChangeRequesterViaIcon()` |
| 3 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyAbleToSelectReleaseRequesterViaIcon()` |

### `SDPOD_CH_CD_781` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `frozenConflictInChange()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `frozenConflictReleaseInCausedByRequest()` |
| 3 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `frozenConflictReleaseInInitiatedRequest()` |

### `SDPOD_AUTO_CMDB_142` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyAddRelationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `checkRelationshipMapInsideButtonFunctionality()` |
| 3 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `createChangeviaComputerCIDV()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_037,SDPOD_ANNOUNCEMENT_PHASE2_038,SDPOD_ANNOUNCEMENT_PHASE2_039,SDPOD_ANNOUNCEMENT_PHASE2_040` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/AddAndEditRoleInAnnouncement.java` | `addAnnouncementInHome()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/AddAndEditRoleInAnnouncement.java` | `editAnnouncementInHome()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/AddAndEditRoleInAnnouncement.java` | `deleteAnnouncementInHome()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_003,SDPOD_ANNOUNCEMENT_PHASE2_004` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInBannerRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInPushNotificationRequesterLogin()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `followAnnouncementInDetailsPageRequesterLogin()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_122,SDPOD_ANNOUNCEMENT_PHASE2_123` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `addAnnouncementInRequest()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `editAnnouncementInRequest()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `deleteAnnouncementInRequest()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_124,SDPOD_ANNOUNCEMENT_PHASE2_125` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `addAnnouncementInChange()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `editAnnouncementInChange()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `deleteAnnouncementInChange()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_126,SDPOD_ANNOUNCEMENT_PHASE2_127` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `addAnnouncementInRelease()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `editAnnouncementInRelease()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `deleteAnnouncementInRelease()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_128,SDPOD_ANNOUNCEMENT_PHASE2_129` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `addAnnouncementInProblem()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `editAnnouncementInProblem()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `deleteAnnouncementInProblem()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_036` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/AnnouncementConfig.java` | `addAnnouncementInHome()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/AnnouncementConfig.java` | `editAnnouncementInHome()` |
| 3 | `com/zoho/automater/selenium/modules/general/announcement/AnnouncementConfig.java` | `deleteAnnouncementInHome()` |

### `SDPOD_CH_MINOR_ENH_041` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `verifyOpenChangesAssignedToMeWidgetPresent()` |
| 2 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `verifyChangePresentInOpenChangesAssignedToMeWidgetWithPrivate()` |
| 3 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `verifyChangePresentInOpenChangesAssignedToMeWidgetWithPublic()` |

### `SDPOD_RM_STATUS_EN_033` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `openReleasesByCategory()` |
| 2 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `openReleasesByRisk()` |
| 3 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `openReleasesByGroup()` |

### `SDPLIVE_SDC_TAC_0037` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `CopyTechEmailSDCoordinator()` |
| 2 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `CopyTechDetailsSDAdmin()` |
| 3 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `CopyTechDetailsSDSiteAdmin()` |

### `SDPOD_AUTO_PB_DV_038` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `deleteTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `addingProblemTaskNotAllowedInThisRole()` |
| 3 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `addImpactDetailsNotAllowed()` |

### `SDPOD_RM_ASSOCIATION_142` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyAttachDetachButtonNotFoundInTrashedProjects()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyUserAbleToAssociateReleaseInMilestones()` |
| 3 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyUserAbleToDissociateReleaseInMilestones()` |

### `SDPOD_AUTO_PROJ_DV_081` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachChangeCausedByProjectInRHS()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachMultipleChangeCausedByProjectInRHS()` |
| 3 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `attachDetachAssociateChangesInRHSInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_085` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `editProjectindetailview()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `editProjectInDetailviewInDefaultProjectManagerRole()` |
| 3 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `editProjectindetailviewInDefaultProjectManagerRole()` |

### `SDPD_PRJ_MIL_TASK_HIST_058` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/projectmilestonetask/ProjectMilestoneTask.java` | `verifyAscendingDescendingIconInMilestoneTaskHistory()` |
| 2 | `com/zoho/automater/selenium/modules/projects/projectmilestonetask/ProjectMilestoneTask.java` | `verifyHistoryDateIconInMilestoneTaskHistory()` |
| 3 | `com/zoho/automater/selenium/modules/projects/projectmilestonetask/ProjectMilestoneTask.java` | `verifyHistoryTimePickerInMilestoneTaskHistory()` |

### `SDPOD_AUTO_PURCHASE_1` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `createBasicPOTest()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderadd/PurchaseOrderAdd.java` | `createBasicPOTest()` |
| 3 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderfullcontrol/PurchaseOrderFullControl.java` | `createBasicPOTest()` |

### `SDP_CHECK_014` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `checkSurvey()` |
| 2 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `convertTechnicianAsRequester()` |
| 3 | `com/zoho/automater/selenium/modules/releasechecklist/releasechecklist/ReleaseChecklist.java` | `liveChat()` |

### `SDPOD_LINKING_RL_029` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyHistoryForParentAssociation()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyHistoryForParentDisassociation()` |
| 3 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyHistoryForSubReleaseAssociation()` |

### `SDPOD_LINKING_RL_045` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyIndirectLinks()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyValidDependency()` |
| 3 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyHistoryWhenDependencyAdded()` |

### `SDPLIVE_RELEASE_STAGETASK_692` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/CloseTask.java` | `selectColumnFromColumnChooserInTaskTemplatePopupInClosureStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/PlanningTask.java` | `selectColumnFromColumnChooserInTaskTemplatePopupInPlanningStage()` |
| 3 | `com/zoho/automater/selenium/modules/releases/releasetask/UATTask.java` | `verifyCancelBtnInColumnChooserInTaskTemplatePopupInUATStage()` |

### `SDPLIVE_RELEASE_STAGETASK_332` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/PlanningTask.java` | `verifyCancelBtnInColumnChooserInTaskTemplatePopupInPlanningStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `selectColumnFromColumnChooserInTaskTemplatePopupInSubmissionStage()` |
| 3 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `verifyCancelBtnInColumnChooserInTaskTemplatePopupInSubmissionStage()` |

### `SDP_REQ_LS_AAA100` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `reset()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterRemoveFavouriteCloseButton()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterRemoveFavouriteCloseButton()` |

### `SDP_REQ_LS_AAA008` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `technicianQuickCreate()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `quickRequestIR()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `technicianQuickCreate()` |

### `SDP_REQ_DV_AAA128` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `priorityHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `priorityHistoryVerificationRHS()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `priorityHistoryVerificationRHS()` |

### `SDP_REQ_LS_AAA105` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `recentItems()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `replyRequestInDetailView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `recentItems()` |

### `SDP_REQ_LS_AAA106` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `recentItemsDelete()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `forwardRequestInDetailView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `recentItemsDelete()` |

### `SDP_REQ_LS_AAA071` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `defaultFiltersinListView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `defaultFiltersinListView()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `defaultFiltersinListView()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_023` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedBySplitRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyLastupdatedByRequestertemplate()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedByRequestertemplate()` |

### `SDPOD_ReqTags_141` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/IncidentRequestTags.java` | `editBusinessRule()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `editBusinessRule()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `editBusinessRule()` |

### `SDPOD_ReqTags_145` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/IncidentRequestTags.java` | `checkSLAExecuted()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkSLAExecuted()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `checkSLAExecuted()` |

### `SDPOD_ReqTags_175` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/IncidentRequestTags.java` | `convertServiceRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkTagNameInHistory()` |
| 3 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `convertIncidentRequest()` |

### `SDP-SR-DP-0314` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/servicerequest/resource/Resource.java` | `changeCheckBoxOption()` |
| 2 | `com/zoho/automater/selenium/modules/requests/servicerequest/resource/Resource.java` | `addNewOptionInCheckBox()` |
| 3 | `com/zoho/automater/selenium/modules/requests/servicerequest/resource/Resource.java` | `deleteCheckBoxOption()` |

### `SDPOD_AUTO_SOL_LV_164` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteMultiplePubAppSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteMultiplePubAppSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreDeleteMultiplePubAppSolution()` |

### `SDPOD_AUTO_SOL_LV_165` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteMultiplePubUnAppSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteMultiplePubUnAppSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreDeleteMultiplePubUnAppSolution()` |

### `SDPOD_AUTO_SOL_LV_166` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteMultiplePrivUnAppSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteMultiplePrivUnAppSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreDeleteMultiplePrivUnAppSolution()` |

### `SDPOD_AUTO_SOL_LV_167` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteMultiplePrivAppSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteMultiplePrivAppSolution()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `restoreDeleteMultiplePrivAppSolution()` |

### `SDPOD_SOLUTIONS_SG_37` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `checkforShareOptionUndersubTopic()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `checkforShareOptionUndersubTopic1()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `checkSharedTopicTechnician()` |

### `SDPOD_SOLUTIONS_SG_45` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyShareTopicWindowDefaultTechGroup_HW()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyShareTopicWindowDefaultTechGroup_Printer()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyShareTopicWindowDefaultTechGroup_Network()` |

### `SDPOD_SOL_VERSION_CTRL_037,SDPOD_SOL_VERSION_CTRL_038` — ×3 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifySolutionVersionCreation()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyNotAbleToDeleteCurrentVersion()` |
| 3 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyNotAbleToRestoreCurrentVersion()` |

### `SDPOD_ChatGPT_Asset Ack _003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `isCodeGenEnabledByDefault()` |
| 2 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `isAssetAckEnabledByDefault()` |

### `SDPOD_ChatGPT_Asset Ack _004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `canCodeGenBeDisabled()` |
| 2 | `com/zoho/automater/selenium/modules/admin/appaddons/integrations/Integrations.java` | `canAssetAckBeDisabled()` |

### `SDPOD_CBR_004,SDPOD_CH_BR_034,SDPOD_CH_BR_035,SDPOD_CH_BR_036` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brWithInOperationalHoursCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brWithInOperationalHoursEdited()` |

### `SDPOD_CBR_084,SDPOD_CH_BR_084,SDPOD_CH_BR_085,SDPOD_CH_BR_086,SDPOD_CH_BR_087,SDPOD_CH_BR_088,SDPOD_CH_BR_089,SDPOD_CH_BR_090,SDPOD_CH_BR_091` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brWithInOperationalHoursDeletedSubModuleAttachments()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brWithInOperationalHoursDeletedSubModuleWorklogs()` |

### `SDPOD_CH_BR_162,SDPOD_CH_BR_163,SDPOD_CH_BR_166,SDPOD_CH_BR_167,SDPOD_CH_BR_170,SDPOD_CH_BR_171,SDPOD_CH_BR_172,SDPOD_CH_BR_173,SDPOD_CH_BR_177,SDPOD_CH_BR_178,SDPOD_CH_BR_179` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brOutSideOperationalHoursCreatedSubModuleWorklogs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/changes/ChangeBusinessRules.java` | `brWithInOperationalHoursCreatedSubModuleChangeWorklogs()` |

### `SDPOD_BR_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brWithInOperationalHoursCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brWithInOperationalHoursEdited()` |

### `SDPOD_BR_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brStatusOperHoursCreated_Is()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brStatusNonOperHoursCreated_Is()` |

### `SDPOD_AUTO_BR_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brGroupCriteriaAbortWhenEdited()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brStatusOperHoursEdited_IsNotEmpty()` |

### `SDPOD_AUTO_BR_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brGroupCriteriaAbortWhenDeleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brStatusNonOperHoursEdited_IsNotEmpty()` |

### `SDPOD_AUTO_BR_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brLevelCriteriaAbortWhenCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brGroupCriteriaAbortWhenCreated()` |

### `SDPOD_AUTO_BR_022` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brLevelCriteriaAbortWhenEdited()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brGroupCriteriaAbortWhenEdited()` |

### `SDPOD_AUTO_BR_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brLevelCriteriaAbortWhenDeleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brGroupCriteriaAbortWhenDeleted()` |

### `SDPOD_AUTO_BR_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brModeCriteriaAbortWhenCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brPriorityCriteriaAbortWhenCreated()` |

### `SDPOD_AUTO_BR_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brModeCriteriaAbortWhenEdited()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brPriorityCriteriaAbortWhenEdited()` |

### `SDPOD_AUTO_BR_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brModeCriteriaAbortWhenDeleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brPriorityCriteriaAbortWhenDeleted()` |

### `SDPOD_AUTO_BR_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brImpactCriteriaAbortWhenCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brAssetCriteriaAbortWhenCreated()` |

### `SDPOD_AUTO_BR_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brImpactCriteriaAbortWhenEdited()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brAssetCriteriaAbortWhenEdited()` |

### `SDPOD_AUTO_BR_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `brImpactCriteriaAbortWhenDeleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `brAssetCriteriaAbortWhenDeleted()` |

### `SDP_AUTO_REQ_CART2402_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/IncidentBusinessRules.java` | `lookupFieldCriteriaCheckOnBREdit()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/HelpDeskConfig.java` | `createLookup()` |

### `SDPOD_ChatGPT_CF_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `isCodeGeneratedApplyConditionChatGPT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `isCodeGeneratedInActionsCFChatGPT()` |

### `SDPOD_REQUEST_RESOURCE_ENHANCEMENT_051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `taskBrWithCustomResourceInCriteriaViaUi()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `verifyServiceSlaWithResourceEnhancementViaUi()` |

### `SDPOD_REQUEST_RESOURCE_ENHANCEMENT_052` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/ServiceBusinessRules.java` | `taskBrWithExistingResourceInCriteriaFieldUpdateViaUi()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `verifyServiceSlaWithCustomResourceEnhancementViaUi()` |

### `SDPOD_CHANGE_CLOSURE_RULES_55` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/ChangeClosureRules.java` | `violatedErrorsShouldNotShownWhileApproverApproved()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/ChangeClosureRules.java` | `violatedErrorShouldShownWhenOneApproverApprovedRemainingPendingApproval()` |

### `SDPOD_CHANGE_CLOSURE_RULES_63` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/ChangeClosureRules.java` | `stageShouldChangeWhenAllApprovalsCompleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/ChangeClosureRules.java` | `verifyViolateErrorWhenStageShouldNotChangeWhenAllApprovalsNotApproved()` |

### `SDP-NR-864` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/CustomActions.java` | `releaseApprovalPLaceholderNotListedMessage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/customactions/CustomActions.java` | `releaseApprovalPLaceholderNotListedSubject()` |

### `SDPOD_CH_MINOR_ENH_102` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `verifyChangeRolesDropdownValuesInApproversField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `verifyChangeUsersDropdownValuesInApproversField()` |

### `SDPOD_PR_Approval_156` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ProblemApprovals.java` | `editProblemApprovalAllFields()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ProblemApprovals.java` | `editProblemApprovalApprovers()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_036` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/Notification.java` | `verifyLastUpdatedNotifications()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastUpdatedNotifications()` |

### `SDPOD_AUTO_REQUEST_NOTIFY_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenRequestCreated()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyTechnicianWhenRequestCreated()` |

### `SDPOD_AUTO_SLA_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `create()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `create()` |

### `SDPOD_AUTO_SLA_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `checkforSLAViolationNoCriteria()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `checkforSLAViolationNoCriteria()` |

### `SDPOD_AUTO_SLA_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `checkforSLAViolationCriteria_Impact()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `checkforSLAViolationCriteria_Priority()` |

### `SDPOD_AUTO_SLA_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `checkforSLAViolationCriteria_Priority()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/ServiceSla.java` | `deleteSLAfromListViewActions()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifylastUpdatedByFieldinServiceSLA()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastUpdatedByreplyrequest()` |

### `SPOD_Request_UDF_Enhancement_247` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyCMDBLookupExecutedViaSLA()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyCMDBLookupPresentInSLA()` |

### `SPOD_Request_UDF_Enhancement_241` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyCMDBLookupShouldNotPresentInSLAAfterCIDeleted()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyAssetLookupShouldNotPresentInSLAAfterAssetDeleted()` |

### `SPOD_Request_UDF_Enhancement_237` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyAssetLookupPresentInSLA()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/sla/IncidentSla.java` | `verifyAssetLookupSLADisabledAndNotExecute()` |

### `SDPOD_AUTO_REQ_TRIGGER_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssetIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssetIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_007` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssetISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssetISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssetISEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssetISEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssetISNOTEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssetISNOTEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCategoryIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCategoryIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCategoryISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCategoryISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCategoryISEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCategoryISEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCategoryISNOTEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCategoryISNOTEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCategoryISCHANGED()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCategoryISCHANGED()` |

### `SDPOD_AUTO_REQ_TRIGGER_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCIsIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCIsIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCIsISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCIsISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCIsISEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCIsISEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCIsISNOTEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCIsISNOTEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCISEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCISEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_022` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCISNOTEMPTY()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCISNOTEMPTY()` |

### `SDPOD_AUTO_REQ_TRIGGER_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCDoesNotContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCDoesNotContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCCEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCCEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDepartmentIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDepartmentIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDepartmentISNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDepartmentISNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDepartmentISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDepartmentISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDepartmentISNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDepartmentISNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDepartmentISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDepartmentISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_036` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_037` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionDoesNotContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionDoesNotContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_038` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDescriptionISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDescriptionISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_039` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithGroupIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithGroupIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_040` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithGroupISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithGroupISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_041` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithGroupISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithGroupISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithGroupISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithGroupISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_043` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithGroupISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithGroupISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_044` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithImpactIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithImpactIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithImpactISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithImpactISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithImpactISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithImpactISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithImpactISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithImpactISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_048` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithImpactISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithImpactISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_049` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithIsMaintenanceIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithIsMaintenanceIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithIsMaintenanceIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithIsMaintenanceIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_052` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithItemIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithItemIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_053` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithItemISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithItemISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_054` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithItemISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithItemISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_055` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithItemISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithItemISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithItemISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithItemISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithLevelIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithLevelIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_058` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithLevelISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithLevelISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_059` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithLevelISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithLevelISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_060` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithLevelISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithLevelISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_061` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithLevelISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithLevelISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_062` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithModeIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithModeIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithModeISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithModeISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_064` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithModeISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithModeISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_065` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithModeISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithModeISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_066` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithModeISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithModeISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithPriorityIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithPriorityIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_073` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithPriorityISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithPriorityISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_074` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithPriorityISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithPriorityISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithPriorityISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithPriorityISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_076` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithPriorityISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithPriorityISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_077` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequestTypeIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequestTypeIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_078` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequestTypeISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequestTypeISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_079` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequestTypeISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequestTypeISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_080` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequestTypeISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequestTypeISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequestTypeISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequestTypeISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_082` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequesterIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequesterIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_083` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequesterISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequesterISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequesterISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequesterISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_085` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRequesterISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRequesterISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_100` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithStatusIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithStatusIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_101` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithStatusISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithStatusISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_102` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithStatusISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithStatusISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_103` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithStatusISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithStatusISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_104` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubCategoryIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubCategoryIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_105` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubCategoryISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubCategoryISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_106` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubCategoryISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubCategoryISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_107` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubCategoryISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubCategoryISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_108` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubCategoryISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubCategoryISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_109` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_110` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_111` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_112` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_113` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_114` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_115` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_116` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSubjectISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSubjectISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_117` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTechnicianIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTechnicianIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_118` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTechnicianISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTechnicianISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_119` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTechnicianISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTechnicianISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_120` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTechnicianISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTechnicianISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_121` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTechnicianChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTechnicianChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_122` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTemplateIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTemplateIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_123` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTemplateISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTemplateISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_124` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTemplateISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTemplateISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_134` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithTemplateISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithTemplateISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_135` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithUrgencyIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithUrgencyIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_136` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithUrgencyISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithUrgencyISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_137` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithUrgencyISEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithUrgencyISEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_138` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithUrgencyISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithUrgencyISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_139` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithUrgencyISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithUrgencyISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_140` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_141` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_142` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_143` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_144` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_145` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_146` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_147` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFAutoNumberIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_148` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_149` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxAre()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxAre()` |

### `SDPOD_AUTO_REQ_TRIGGER_150` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_151` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_152` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFCheckBoxIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_153` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_154` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_155` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_156` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_157` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_158` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_159` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_364` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_365` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_160` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_161` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecimalIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_162` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_163` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_164` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDecisionBoxIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_165` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_166` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_167` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_168` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_169` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_170` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_171` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_172` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_173` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFEmailIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFEmailIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_174` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_175` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_176` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_177` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_178` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_179` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_180` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_181` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_182` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiLineIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_183` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_184` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_185` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_186` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFMultiSelectIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_187` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_188` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_189` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_190` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_191` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_192` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_193` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_194` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_366` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_367` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_195` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFNumericIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFNumericIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_196` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_197` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_198` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_199` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_200` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_201` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_202` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_203` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_204` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPhoneIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_205` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPickListIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPickListIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_206` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPickListIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPickListIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_207` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPickListIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPickListIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_208` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPickListIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPickListIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_209` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFPickListIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFPickListIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_210` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_211` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_212` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_213` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_214` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFRadioButtonIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_215` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_216` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_217` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_218` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_219` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_220` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_221` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_222` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_223` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFSingleLineIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_224` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_225` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_226` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_227` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_228` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLContains()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLContains()` |

### `SDPOD_AUTO_REQ_TRIGGER_229` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLDoesNotContain()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLDoesNotContain()` |

### `SDPOD_AUTO_REQ_TRIGGER_230` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLBeginsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLBeginsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_231` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLEndsWith()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLEndsWith()` |

### `SDPOD_AUTO_REQ_TRIGGER_232` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFURLIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFURLIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_233` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_234` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_235` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_236` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_237` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_238` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_239` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_240` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_241` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_368` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_369` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAFDateTimeNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAFDateTimeNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_242` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSiteIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSiteIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_243` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSiteISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSiteISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_244` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSiteISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSiteISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_245` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateIS()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateIS()` |

### `SDPOD_AUTO_REQ_TRIGGER_246` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateISNOT()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateISNOT()` |

### `SDPOD_AUTO_REQ_TRIGGER_247` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_248` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateISNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateISNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_249` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateGreaterthan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateGreaterthan()` |

### `SDPOD_AUTO_REQ_TRIGGER_250` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateLesserthan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateLesserthan()` |

### `SDPOD_AUTO_REQ_TRIGGER_251` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_252` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateLesserOREqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateLesserOREqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_370` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_371` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCreatedDateNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCreatedDateNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_253` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_254` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_255` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_256` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_257` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTIsNOTEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTIsNOTEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_258` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_259` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_260` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_261` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_372` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_373` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSSTNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSSTNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_262` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_263` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_264` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETISChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETISChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_265` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_266` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_267` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_268` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_269` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_270` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_374` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_375` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithSETNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithSETNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_271` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_272` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_273` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_274` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_275` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_276` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_277` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDLesserrThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDLesserrThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_278` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_279` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDLesserrOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDLesserrOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_376` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_377` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithRDDNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithRDDNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_280` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_281` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_282` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_283` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_284` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_285` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_286` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_287` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_288` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_378` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_379` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithDBDNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithDBDNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_289` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_290` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_291` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_292` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_293` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_294` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_295` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_296` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_297` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_380` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_381` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithAssignedTimeNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithAssignedTimeNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_298` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_299` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_300` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_301` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_302` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_303` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_304` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_305` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_306` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_382` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_383` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithResolvedTimeNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithResolvedTimeNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_307` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIs()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIs()` |

### `SDPOD_AUTO_REQ_TRIGGER_308` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsNot()` |

### `SDPOD_AUTO_REQ_TRIGGER_309` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsChanged()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsChanged()` |

### `SDPOD_AUTO_REQ_TRIGGER_310` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_311` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsNotEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeIsNotEmpty()` |

### `SDPOD_AUTO_REQ_TRIGGER_312` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeGreaterThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeGreaterThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_313` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeLesserThan()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeLesserThan()` |

### `SDPOD_AUTO_REQ_TRIGGER_314` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeGreaterOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeGreaterOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_315` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeLesserOrEqual()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeLesserOrEqual()` |

### `SDPOD_AUTO_REQ_TRIGGER_384` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER_385` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkFunctunalityWithCompletedTimeNotBetween()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ServiceRequestTrigger.java` | `checkFunctunalityWithCompletedTimeNotBetween()` |

### `SDPOD_AUTO_REQ_TRIGGER` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createTriggerIsChangedCreiteriaConditionInUI()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `verifyTriggerExecutedForMobileApplicationMode()` |

### `SDPOD_PROBLEM_MULTISELECT_LOOKUP_062` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createTriggerWithMultiLookupDateUDF()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `executeTriggerWithMultiLookupDateUDF()` |

### `SDPOD_PROBLEM_MULTISELECT_LOOKUP_270` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createTriggerWithMultiLookupDateUDF()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `executeTriggerWithMultiLookupDateUDF()` |

### `SDPOD_CHANGE_WORKFLOW_TRANSITION_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `verifyMandatoryFieldsUDF()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `verifyTransitionwithUDFCriteria()` |

### `SDPOD_INCIDENT_WORKFLOW_TRANSITION_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `verifyTransitionAfterWorkLogAdded()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `editTransition()` |

### `SDPOD_INCIDENT_WORKFLOW_TRANSITION_010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `verifyTransitionwithUDFCriteria()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `verifyTransitionwithCriteria()` |

### `SDPOD_PR_Approval_521` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createProblemWorkflowAndVerifyApprovalByCEOrole()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createProblemWorkflowAndVerifyApprovalByCFOrole()` |

### `SDPOD_SERVICE_WORKFLOW_TRANSITION_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `verifyTransitionwithUDFCriteria()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `verifyTransitionwithCriteria()` |

### `SPOD_Request_UDF_Enhancement_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyCMDBEntityDropdownValuesinRequestLookup()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAssetEntityDropdownValuesinRequestLookup()` |

### `SPOD_Request_UDF_Enhancement_073` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyRequestAssetLookupIsPresentInColumnChooser()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyExistingAddedReqAssetLookupShouldDisplayinCurrentAssetLookup()` |

### `SPOD_Request_UDF_Enhancement_090` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAbleToPickupMultipleRequestAssetLookup()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/roles/RequestSDAdminWithSDCordinator.java` | `verifyAbleToPickupMultipleRequestAssetLookup()` |

### `SPOD_Request_UDF_Enhancement_093` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAbleToCloseMultipleRequestCMDBLookup()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `verifyAbleToAssignMultipleRequestCMDBLookup()` |

### `SDPOD_SYNC_RULE_ENC_009,SDPOD_SYNC_RULE_ENC_028,SDPOD_SYNC_RULE_ENC_033-040,SDPOD_DEDUPLICATION_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeUserSyncRuleForRequesterWithAllActions()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeUserSyncRuleForTechnicianWithAllActions()` |

### `SDPOD_SYNC_RULE_ENC_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationOfNameField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationOfCITypeField()` |

### `SDPOD_SYNC_RULE_ENC_093,` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `userSyncRuleCreationInUI()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `assetSyncRuleExecutionInUI()` |

### `SDPOD_RM_STATUS_EN_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `editNewStatusInProgressToCompletion()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `verifyColurCodeAterEditStatus()` |

### `SDPOD_RM_STATUS_EN_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `failedReleaseFilterFunctionality()` |
| 2 | `com/zoho/automater/selenium/modules/admin/customization/releasemanagement/releasestage/ReleaseStage.java` | `closedReleaseFilterFunctionality()` |

### `SDPOD_AUTO_CUSTOM_MODULE_03` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithMultiLineField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithNumericField()` |

### `SDPOD_AUTO_CUSTOM_MODULE_04` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithPicklistField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithDateField()` |

### `SDPOD_AUTO_CUSTOM_MODULE_11` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithCurrencyField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `addCustomModuleWithDecimalField()` |

### `SDPOD_AUTO_CUSTOM_MODULE_43` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `spotEditCustomModuleEntityMultiSelectLookupFieldAssetIsNot()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModuleUDF.java` | `addMultilookupWithDepartmentCriteriaIS()` |

### `SDPOD_SUBFORM_UDF_REQUEST_016,SDPOD_SUBFORM_UDF_REQUEST_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `ipAddressUDFInCustomModulesLV()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `customModuleTrashInCM()` |

### `SDPOD_SUBFORM_UDF_REQUEST_112` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `attachmentUDFDeleteCustomModules()` |
| 2 | `com/zoho/automater/selenium/modules/admin/developerspace/custommodule/CustomModule.java` | `disableSpotEditCustomModules()` |

### `SDPOD_HEADER_TAB_010,SDPOD_DEDUPLICATION_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `checkResetInNavigationAndFooterSettingsPageTechnicianHeader()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `hideOrShowIconInNavigationAndFooterSettingsPageTechnicianFooter()` |

### `SDPOD_HEADER_TAB_107,SDPOD_HEADER_TAB_111` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `functionalityOfReorderSupportInNavigationAndFooterSettingsPageTechnicianFooter()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/navigationandfootersettings/NavigationAndFooterSettings.java` | `functionalityOfReorderDiscoverProductInNavigationAndFooterSettingsPageRequesterFooter()` |

### `SDPOD_SSP_SC_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `verifySearchSettingsAlignmentCanbeModified()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `verifySearchSettingsAlignmentInRequesterPortal()` |

### `SDPOD_SSP_SC_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `verifySearchFunctionalityInTechnicianLogin()` |
| 2 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalcustomization/RequesterPortalCustomization.java` | `verifySearchFunctionalityInRequesterLogin()` |

### `SDPOD_REQUEST_SDGT_PERF_001 , SDPOD_REQUEST_SDGT_PERF_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `siteCheckAddDept()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `siteCheckEditDept()` |

### `SDPOD_REQUEST_SDGT_PERF_003 , SDPOD_REQUEST_SDGT_PERF_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `referSiteCheckAddDept()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `referSiteCheckEditDept()` |

### `SDPOD_ORG_ROLE_094, SDPOD_ORG_ROLE_095` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `singleUsersNotificationlbyTriggerforContractFromOrganization()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `multipleUsersNotificationTriggerforContractFromOrganization()` |

### `SDPOD_ORG_ROLE_106,SDPOD_ORG_ROLE_025,SDPOD_ORG_ROLE_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `fieldUpdatebyBrforRequestFromOrganizationofTechnicianAdditionalField()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `fieldUpdatebyBrforRequestFromOrganizationofRequesterAdditionalField()` |

### `SDPOD_ORG_ROLE_185` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `SingleUserforDelegateofServiceRequestforUser()` |
| 2 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/orgrole/OrgRole.java` | `SingleUserforDelegateofIncidentRequestforUser()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_045,SDPOD_ANNOUNCEMENT_PHASE2_048` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/announcementtemplate/AnnouncementTemplate.java` | `presenceOfAnnouncementTemplateInAdmin()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `announcementBannerUntilItsViewedOnce()` |

### `SDPOD_AU_PB_CS_063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ProblemCustomScript.java` | `unknown()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ProblemCustomScript.java` | `unknown()` |

### `SDPOD_AU_PB_CS_091` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ProblemCustomScript.java` | `checkCSShowTasksActionInFAFROnFieldChange()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ProblemCustomScript.java` | `checkCSHideTasksActionInFAFROnFieldChange()` |

### `SDPOD_SERVICE_CATALOG_CUSTOMIZATION_057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyDefaultRequestImageIsPresentInPrintPreview()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyTemplateNameDisplayingWhileSearchWithCommentsInRequesterLogin()` |

### `SDPOD_TLHCA_001, SDPOD_TLHCA_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `formCustomizationIsPresent()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `formCustomizationIsPresent()` |

### `SDPOD_TLHCA_003,SDPOD_TLHCA_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addContentInHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addContentInHelpcard()` |

### `SDPOD_TLHCA_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addContentInHelpcardWithNumbers()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addContentInHelpcardWithNumbers()` |

### `SDPOD_TLHCA_005` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addContentInHelpcardWithSpecialChar()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addContentInHelpcardWithSpecialChar()` |

### `SDPOD_TLHCA_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addAttcahmentinHelpCard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addAttcahmentinHelpCard()` |

### `SDPOD_TLHCA_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `saveTemplateWithEmptyHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `saveTemplateWithEmptyHelpcard()` |

### `SDPOD_TLHCA_011,SDPOD_TLHCA_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkRequestFormButtonIsPresent()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `checkRequestFormButtonIsPresent()` |

### `SDPOD_TLHCA_011,SDPOD_TLHCA_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkRequestDetailsPageButtonIsPresent()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `checkRequestDetailsPageButtonIsPresent()` |

### `SDPOD_TLHCA_010,SDPOD_TLHCA_011,SDPOD_TLHCA_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyCopyHelpcardToRequesterView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyCopyHelpcardToRequesterView()` |

### `SDPOD_TLHCA_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkEditHelpcardAndSave()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `checkEditHelpcardAndSave()` |

### `SDPOD_TLHCA_018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addHelpcardContentInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addHelpcardContentInReqView()` |

### `SDPOD_TLHCA_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addHelpcardContentWithNumbersInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addHelpcardContentWithNumbersInReqView()` |

### `SDPOD_TLHCA_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addHelpcardContentWithSpecialCharInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addHelpcardContentWithSpecialCharInReqView()` |

### `SDPOD_TLHCA_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyAddedHelpcardPresentInTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyAddedHelpcardPresentInTemp()` |

### `SDPOD_TLHCA_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditHelpcard()` |

### `SDPOD_TLHCA_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditNumbersInHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditNumbersInHelpcard()` |

### `SDPOD_TLHCA_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditSpecialCharInHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditSpecialCharInHelpcard()` |

### `SDPOD_TLHCA_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditEmptyHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditEmptyHelpcard()` |

### `SDPOD_TLHCA_037` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditRequestForm()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditRequestForm()` |

### `SDPOD_TLHCA_038` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditRequestDetailsPage()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditRequestDetailsPage()` |

### `SDPOD_TLHCA_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditHelpcardInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditHelpcardInReqView()` |

### `SDPOD_TLHCA_050` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditEmptyHelpcardInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditEmptyHelpcardInReqView()` |

### `SDPOD_TLHCA_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditRequestFormInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditRequestFormInReqView()` |

### `SDPOD_TLHCA_048` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEditRequestDetailsPageInReqView()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEditRequestDetailsPageInReqView()` |

### `SDPOD_TLHCA_039` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyCopyHelpcardToRequesterViewInEdit()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyCopyHelpcardToRequesterViewInEdit()` |

### `SDPOD_TLHCA_044` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyAlertWhenEnableCopyToRequester()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyAlertWhenEnableCopyToRequester()` |

### `SDPOD_TLHCA_052` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyCopiedHelpcardContent()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyCopiedHelpcardContent()` |

### `SDPOD_TLHCA_054` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEnabledRequestFormInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEnabledRequestFormInCopyTemp()` |

### `SDPOD_TLHCA_055` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyDisabledRequestFormInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledRequestFormInCopyTemp()` |

### `SDPOD_TLHCA_056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEnabledRequestDetailsInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEnabledRequestDetailsInCopyTemp()` |

### `SDPOD_TLHCA_057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyDisabledRequestDetailsInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledRequestDetailsInCopyTemp()` |

### `SDPOD_TLHCA_058` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyEmptyHelpCardInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyEmptyHelpCardInCopyTemp()` |

### `SDPOD_TLHCA_061` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `addHelpCardInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `addHelpCardInCopyTemp()` |

### `SDPOD_TLHCA_062` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `editHelpCardInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `editHelpCardInCopyTemp()` |

### `SDPOD_TLHCA_063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `deleteHelpCardInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `deleteHelpCardInCopyTemp()` |

### `SDPOD_TLHCA_065` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyRequesterHelpcardInCopyTemp()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyRequesterHelpcardInCopyTemp()` |

### `SDPOD_TLHCA_067` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardPresentInRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardPresentInRequest()` |

### `SDPOD_TLHCA_069_70_71_80_81` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardContentPresentInRequestForm()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardContentPresentInRequestForm()` |

### `SDPOD_TLHCA_075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyRequestCreatedWithHelpcard()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyRequestCreatedWithHelpcard()` |

### `SDPOD_TLHCA_079` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardPresentWhenHelpcardIsEmpty()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardPresentWhenHelpcardIsEmpty()` |

### `SDPOD_TLHCA_084_085_086_090_095_096` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardContentPresentInRequestDetails()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardContentPresentInRequestDetails()` |

### `SDPOD_TLHCA_097_098` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardInTrashedRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardInTrashedRequest()` |

### `SDPOD_TLHCA_101` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardInRestoredRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardInRestoredRequest()` |

### `SDPOD_TLHCA_107` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardPresentInDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardPresentInDuplicateRequest()` |

### `SDPOD_TLHCA_109` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardNotPresentInDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardNotPresentInDuplicateRequest()` |

### `SDPOD_TLHCA_128` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyHelpcardInTemplatePreview()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyHelpcardInTemplatePreview()` |

### `SDPOD_OM_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `organizeBtnNotPresentInProjectTemplateForViewEditRole()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `organizeBtnNotPresentForViewEditRole()` |

### `SDPOD_PROJECT_UDF_LOOKUP_TC157` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `createProjectWithUserLookup()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `checkProjectUserLookupWithLoggedInUserAsCriteriaValue()` |

### `SPDOD_AUTO_RT_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `copyReleaseTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/releasetemplate/ReleaseTemplate.java` | `CreateReleaseTemplate()` |

### `SDPOD_SERVICE_CATALOG_CUSTOMIZATION_003,SDPOD_SERVICE_CATALOG_CUSTOMIZATION_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `copyTemplateForServiceTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `copyTemplateForIncidentTemplate()` |

### `SDPOD_AUTO_SC_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyAllCategoriesListedInCardViewLayout()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyAllCategoriesListedInListViewLayout()` |

### `SDPOD_AUTO_SC_002,SDPOD_SERVICE_CATALOG_CUSTOMIZATION_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyOnHoverDescriptionInListViewLayout()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `verifyOnHoverDescriptionInListViewLayout()` |

### `SDPOD_SERVICE_CATALOG_CUSTOMIZATION_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyServiceTemplateImagePresentWhileCreatingRequest()` |
| 2 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `verifyServiceTemplateImagePresentWhileCreatingRequest()` |

### `SDPOD_CMDB_FGA_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/finegrainedaccess/AssetFGA.java` | `searchAssetFineGrainedAccess()` |
| 2 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/finegrainedaccess/CMDBFGA.java` | `searchCMDBFineGrainedAccess()` |

### `SDPOD_ZIA_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen1()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen25()` |

### `SDPOD_ZIA_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen2()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen26()` |

### `SDPOD_ZIA_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen3()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen27()` |

### `SDPOD_ZIA_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen4()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen28()` |

### `SDPOD_ZIA_005` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen5()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen29()` |

### `SDPOD_ZIA_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen6()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen30()` |

### `SDPOD_ZIA_007` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen7()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen31()` |

### `SDPOD_ZIA_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen8()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen32()` |

### `SDPOD_ZIA_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen9()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen33()` |

### `SDPOD_ZIA_010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen10()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen34()` |

### `SDPOD_ZIA_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen11()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen35()` |

### `SDPOD_ZIA_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen12()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen36()` |

### `SDPOD_ZIA_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen13()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen37()` |

### `SDPOD_ZIA_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen14()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen38()` |

### `SDPOD_ZIA_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen15()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen39()` |

### `SDPOD_ZIA_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen16()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen40()` |

### `SDPOD_ZIA_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen17()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen41()` |

### `SDPOD_ZIA_018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen18()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen42()` |

### `SDPOD_ZIA_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen19()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen43()` |

### `SDPOD_ZIA_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen20()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen44()` |

### `SDPOD_ZIA_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen21()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen45()` |

### `SDPOD_ZIA_022` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen22()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen46()` |

### `SDPOD_ZIA_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen23()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen47()` |

### `SDPOD_ZIA_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen24()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoOpen48()` |

### `SDPOD_ZIA_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose1()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose23()` |

### `SDPOD_ZIA_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose2()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose24()` |

### `SDPOD_ZIA_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose3()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose25()` |

### `SDPOD_ZIA_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose5()` |
| 2 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `autoClose27()` |

### `SDPOD_AUTO_AP_LV_0001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createAccessPointAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createAccessPoinAsset()` |

### `SDPOD_AUTO_AP_LV_0004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addAccessPointToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addAccessPointToGroup()` |

### `SDPOD_AUTO_PRINTER_LV_0018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createPrinterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createPrinterAsset()` |

### `SDPOD_AUTO_PRINTER_LV_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editPrinterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editPrinterAsset()` |

### `SDPOD_AUTO_PRINTER_LV_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deletePrinterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deletePrinterAsset()` |

### `SDPOD_AUTO_PRINTER_LV_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addPrinterToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addPrinterToGroup()` |

### `SDPOD_AUTO_ROUTER_LV_036` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createRouterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createRouterAsset()` |

### `SDPOD_AUTO_ROUTER_LV_039` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editRouterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editRouterAsset()` |

### `SDPOD_AUTO_ROUTER_LV_040,SDPOD_AUTO_ROUTER_LV_046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteCiscoRouterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteCiscoRouterAsset()` |

### `SDPOD_AUTO_ROUTER_LV_037` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addRouterToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addRouterToGroup()` |

### `SDPOD_AUTO_SERVER_LV_121,SDPOD_AUTO_SERVER_LV_122,SDPOD_AUTO_SERVER_DV_436` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createandVerifyHistoryinServerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createServerAsset()` |

### `SDPOD_AUTO_SERVER_LV_125,SDPOD_AUTO_SERVER_DV_438` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editandVerifyHistoryinServerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editandVerifyHistoryinServerAsset()` |

### `SDPOD_AUTO_SERVER_LV_126,SDPOD_AUTO_SERVER_LV_132` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteServerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteServerAsset()` |

### `SDPOD_AUTO_SERVER_LV_127` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addServerToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addServerToGroup()` |

### `SDPOD_AUTO_WS_LV_069,SDPOD_AUTO_WS_LV_097,SDPOD_AUTO_WS_LV_112` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createWorkstationAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createWorkstationAsset()` |

### `SDPOD_AUTO_WS_LV_076,SDPOD_AUTO_WS_LV_148,SDPOD_AUTO_WS_LV_149,SDPOD_AUTO_WS_LV_317,SDPOD_AUTO_WS_DV_378` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editWorkstationAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editWorkstationAsset()` |

### `SDPOD_AUTO_WS_LV_077,SDPOD_AUTO_WS_LV_083` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteWorkstationAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteWorkstationAsset()` |

### `SDPOD_AUTO_WS_LV_078` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addWorkstationToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addWorkstationToGroup()` |

### `SDPOD_AUTO_SP_LV_280` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createSmartPhoneAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createSmartPhoneAsset()` |

### `SDPOD_AUTO_SP_LV_283` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editSmartphoneAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editSmartphoneAsset()` |

### `SDPOD_AUTO_SP_LV_284,SDPOD_AUTO_SP_LV_290` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteSmartphoneAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteSmartphoneAsset()` |

### `SDPOD_AUTO_SP_LV_282,SDPOD_AUTO_SP_LV_286` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addSmartphoneToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addSmartphoneToGroup()` |

### `SDPOD_AUTO_SWITCHES_LV_056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createSwitchAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createSwitchAsset()` |

### `SDPOD_AUTO_SWITCHES_LV_057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editSwitchAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editSwitchAsset()` |

### `SDPOD_AUTO_SWITCHES_LV_058` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteSCiscowitchAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteSCiscowitchAsset()` |

### `SDPOD_AUTO_TAB_LV_331,SDPOD_AUTO_TAB_LV_332` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createTabletAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createTabletAsset()` |

### `SDPOD_AUTO_TAB_LV_333` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editTabletAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editTabletAsset()` |

### `SDPOD_AUTO_TAB_LV_334,SDPOD_AUTO_TAB_LV_341` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteTabletAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteTabletAsset()` |

### `SDPOD_AUTO_TAB_LV_335` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addTabletToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addTabletToGroup()` |

### `SDPOD_AUTO_PR_LV_059,SDPOD_AUTO_PR_LV_203,SDPOD_AUTO_PR_LV_204` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createProjectorAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createProjectorAsset()` |

### `SDPOD_AUTO_PROJECTOR_LV_060` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editProjectorAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editProjectorAsset()` |

### `SDPOD_AUTO_PR_LV_061,SDPOD_AUTO_PR_LV_212` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteProjectorAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteProjectorAsset()` |

### `SDPOD_AUTO_PR_LV_206,SDPOD_AUTO_PR_LV_205,SDPOD_AUTO_PR_LV_116` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addProjectorToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addProjectorToGroup()` |

### `SDPOD_AUTO_SCANNER_LV_062,SDPOD_AUTO_SCANNER_LV_222,SDPOD_AUTO_SCANNER_LV_223` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createScannerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createScannerAsset()` |

### `SDPOD_AUTO_PROJECTOR_LV_063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editScannerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editScannerAsset()` |

### `SDPOD_AUTO_SCANNER_LV_064,SDPOD_AUTO_SCANNER_LV_231` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteScannerAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteScannerAsset()` |

### `SDPOD_AUTO_SCANNER_LV_224,SDPOD_AUTO_SCANNER_LV_225` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addScannerToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addScannerToGroup()` |

### `SDPOD_AUTO_KB_LV_142,SDPOD_AUTO_KB_LV_143,SDPOD_AUTO_KB_LV_241` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createKeyboardAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createKeyboardAsset()` |

### `SDPOD_AUTO_KB_LV_147` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editKeyboardAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editKeyboardAsset()` |

### `SDPOD_AUTO_KB_LV_249` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteKeyboardAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteKeyboardAsset()` |

### `SDPOD_AUTO_KB_LV_118,SDPOD_AUTO_KB_LV_145,SDPOD_AUTO_KB_LV_146,SDPOD_AUTO_KB_LV_242,SDPOD_AUTO_KB_LV_243` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addKeyboardToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addKeyboardToGroup()` |

### `SDPOD_AUTO_VH_LV_158,SDPOD_AUTO_VH_LV_162,SDPOD_AUTO_VH_LV_114` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addVirtualHostToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addVirtualHostToGroup()` |

### `SDPOD_AUTO_VM_LV_187,SDPOD_AUTO_VM_LV_115` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addVirtualMachineToGroup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addVirtualMachineToGroup()` |

### `SDPOD_AUTO_VH_LV_157,SDPOD_AUTO_VH_LV_181,SDPOD_AUTO_VH_DV_460,SDPOD_AUTO_VH_DV_483` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createVirtualHostsAssetinUI()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createVirtualHostsAssetinUI()` |

### `SDPOD_AUTO_VH_LV_161,SDPOD_AUTO_VH_LV_168` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteVirtualHostinListviewUsingActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteVirtualHostinListviewUsingActions()` |

### `SDPOD_AUTO_VM_DV_484,SDPOD_AUTO_VM_DV_485` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createVirtualMachineAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createVirtualMachineAsset()` |

### `SDPOD_AUTO_VM_LV_186` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteVirtualMachineinLvUsingActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteVirtualMachineinLvUsingActions()` |

### `SDPOD_AUTO_VM_LV_185` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editVMinListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editVMinListview()` |

### `SDPOD_AUTO_VH_LV_160` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editVHinListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editVHinListview()` |

### `SDPOD_AUTO_VH_LV_169` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinVHListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinVHListview()` |

### `SDPOD_AUTO_VH_LV_170` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinVHLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinVHLv()` |

### `SDPOD_AUTO_VH_LV_171` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_172` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_173` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_174` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_175` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeorQRcodeinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeorQRcodeinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_176` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteVirtualHostinListviewinVirtualHosts()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteVirtualHostinListviewinVirtualHosts()` |

### `SDPOD_AUTO_VH_LV_177` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteBulkVirutalhostfromListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteBulkVirutalhostfromListview()` |

### `SDPOD_AUTO_VM_LV_194` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinVMlistview()` |

### `SDPOD_AUTO_VM_LV_195` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinVMlistview()` |

### `SDPOD_AUTO_VM_LV_196` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinVMlistview()` |

### `SDPOD_AUTO_VM_LV_197` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinVMlistview()` |

### `SDPOD_AUTO_VM_LV_198` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStatesinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStatesinVMlistview()` |

### `SDPOD_AUTO_VM_LV_199` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinVMlistview()` |

### `SDPOD_AUTO_VM_LV_200` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeorQRcodeinVMlistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeorQRcodeinVMlistview()` |

### `SDPOD_AUTO_VM_LV_201` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinVmListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinVmListview()` |

### `SDPOD_AUTO_VM_LV_202` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinVmListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinVmListview()` |

### `SDPOD_AUTO_VM_LV_193` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `deleteVirtualMachineinListviewUsingDeleteButton()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `deleteVirtualMachineinListviewUsingDeleteButton()` |

### `SDPOD_AUTO_VH_LV_178` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchVirtualHostbyNamefromListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `searchVirtualHostbyNamefromListview()` |

### `SDPOD_AUTO_SP_LV_291` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinSpLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinSpLv()` |

### `SDPOD_AUTO_SP_LV_292` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinSmartphoneListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinSmartphoneListview()` |

### `SDPOD_AUTO_SP_LV_293` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinSmartphoneLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinSmartphoneLv()` |

### `SDPOD_AUTO_SP_LV_620` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinSmartphoneLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinSmartphoneLv()` |

### `SDPOD_AUTO_SP_LV_294` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinSmartphoneListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinSmartphoneListview()` |

### `SDPOD_AUTO_SP_LV_295` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodesinSmartphoneLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodesinSmartphoneLv()` |

### `SDPOD_AUTO_SP_LV_296` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinSmartphoneLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinSmartphoneLv()` |

### `SDPOD_AUTO_SP_LV_297` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinSpLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinSpLv()` |

### `SDPOD_AUTO_AP_LV_0005` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinApLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinApLvActions()` |

### `SDPOD_AUTO_PRINTER_LV_0022` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinPrintersLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinPrintersLvActions()` |

### `SDPOD_AUTO_ROUTER_LV_042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinCiscoRoutersLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinCiscoRoutersLvActions()` |

### `SDPOD_AUTO_SERVER_LV_128` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinServersListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinServersListviewActions()` |

### `SDPOD_AUTO_SP_LV_287` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinsmartphoneListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinsmartphoneListviewActions()` |

### `SDPOD_AUTO_TAB_LV_336` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinTabletsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinTabletsListviewActions()` |

### `SDPOD_AUTO_WS_LV_079` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinWorkstationsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinWorkstationsListviewActions()` |

### `SDPOD_AUTO_VH_LV_163` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinVirtualHostsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinVirtualHostsListviewActions()` |

### `SDPOD_AUTO_VM_LV_188` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinVMLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinVMLvActions()` |

### `SDPOD_AUTO_PR_LV_207` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinProjectorListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinProjectorListviewActions()` |

### `SDPOD_AUTO_SCANNER_LV_226` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinScannersListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinScannersListviewActions()` |

### `SDPOD_AUTO_KB_LV_244` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinKeyboardListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinKeyboardListviewActions()` |

### `SDPOD_AUTO_AST_LV_0008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinApinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinApinLvActions()` |

### `SDPOD_AUTO_PRINTER_LV_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinPrintersLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinPrintersLvActions()` |

### `SDPOD_AUTO_ROUTER_LV_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinRoutersLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinRoutersLvActions()` |

### `SDPOD_AUTO_SERVER_LV_131` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinServersListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinServersListviewActions()` |

### `SDPOD_AUTO_SP_LV_289` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinSmartphonessListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinSmartphonessListviewActions()` |

### `SDPOD_AUTO_TAB_LV_339` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinTabletsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinTabletsListviewActions()` |

### `SDPOD_AUTO_WS_LV_082,SDPOD_AUTO_WS_LV_074` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinWorkstationsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinWorkstationsListviewActions()` |

### `SDPOD_AUTO_VH_LV_166` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinVirtualhostListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinVirtualhostListviewActions()` |

### `SDPOD_AUTO_VM_LV_191` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinVirtualmachineListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinVirtualmachineListviewActions()` |

### `SDPOD_AUTO_PR_LV_210` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinProjectorsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinProjectorsListviewActions()` |

### `SDPOD_AUTO_SCANNER_LV_229` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinScannersListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinScannersListviewActions()` |

### `SDPOD_AUTO_KB_LV_247` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyStatesinKeyboardsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyStatesinKeyboardsListviewActions()` |

### `SDPOD_AUTO_AST_LV_0006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinAccessPointsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinAccessPointsinListviewActions()` |

### `SDPOD_AUTO_PRINTER_LV_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinPrintersinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinPrintersinLvActions()` |

### `SDPOD_AUTO_ROUTER_LV_043` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinRoutersinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinRoutersinLvActions()` |

### `SDPOD_AUTO_SERVER_LV_129` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinServersinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinServersinListviewActions()` |

### `SDPOD_AUTO_SP_LV_288` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinSpinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinSpinLvActions()` |

### `SDPOD_AUTO_TAB_LV_337` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinTabletsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinTabletsinListviewActions()` |

### `SDPOD_AUTO_WS_LV_080` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinWorkstationsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinWorkstationsinListviewActions()` |

### `SDPOD_AUTO_VH_LV_164` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinVHinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinVHinListviewActions()` |

### `SDPOD_AUTO_VM_LV_189` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinVMinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinVMinListviewActions()` |

### `SDPOD_AUTO_PR_LV_208` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinProjectorsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinProjectorsinListviewActions()` |

### `SDPOD_AUTO_SCANNER_LV_227` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinScannersinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinScannersinListviewActions()` |

### `SDPOD_AUTO_KB_LV_245` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoDepartmentinKeyboardsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoDepartmentinKeyboardsinListviewActions()` |

### `SDPOD_AUTO_AST_LV_0007` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinApinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinApinLvActions()` |

### `SDPOD_AUTO_PRINTER_LV_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinPrintersinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinPrintersinLvActions()` |

### `SDPOD_AUTO_ROUTER_LV_044` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinRoutersinLvActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinRoutersinLvActions()` |

### `SDPOD_AUTO_SERVER_LV_130` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinServersinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinServersinListviewActions()` |

### `SDPOD_AUTO_TAB_LV_338` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinTabletsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinTabletsinListviewActions()` |

### `SDPOD_AUTO_WS_LV_081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinWorkstationsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinWorkstationsinListviewActions()` |

### `SDPOD_AUTO_VH_LV_165` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinVirtualhostsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinVirtualhostsinListviewActions()` |

### `SDPOD_AUTO_VM_LV_190` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinVirtualmachinesinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinVirtualmachinesinListviewActions()` |

### `SDPOD_AUTO_PR_LV_209` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinProjectorsinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinProjectorsinListviewActions()` |

### `SDPOD_AUTO_SCANNER_LV_228` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinScannersinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinScannersinListviewActions()` |

### `SDPOD_AUTO_KB_LV_246` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assigntoSiteinKeyboardinListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assigntoSiteinKeyboardinListviewActions()` |

### `SDPOD_AUTO_AST_LV_0009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinAPLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinAPLv()` |

### `SDPOD_AUTO_AST_LV_0010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `CancelButtoninConfigureDepreciationinApLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `CancelButtoninConfigureDepreciationinApLv()` |

### `SDPOD_AUTO_AST_LV_0011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinApinLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinApinLv()` |

### `SDPOD_AUTO_AST_LV_0012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinApinLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinApinLv()` |

### `SDPOD_AUTO_AST_LV_0013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonininModifyStateApLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonininModifyStateApLv()` |

### `SDPOD_AUTO_AST_LV_0014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodesApLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodesApLv()` |

### `SDPOD_AUTO_AST_LV_0016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `CancelButtonwhileBulkDeleteApLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `CancelButtonwhileBulkDeleteApLv()` |

### `SDPOD_AUTO_SP_LV_298` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonfromAddSmartphoneform()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonfromAddSmartphoneform()` |

### `SDPOD_AUTO_PRINTER_LV_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinPrinterslv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinPrinterslv()` |

### `SDPOD_AUTO_PRINTER_LV_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `CancelButtoninConfigureDepreciationinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `CancelButtoninConfigureDepreciationinPrintersLv()` |

### `SDPOD_AUTO_PRINTER_LV_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinPrintersLv()` |

### `SDPOD_AUTO_PRINTER_LV_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinPrintersLV()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinPrintersLV()` |

### `SDPOD_AUTO_PRINTER_LV_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinPrintersLv()` |

### `SDPOD_AUTO_PRINTER_LV_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodesinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodesinPrintersLv()` |

### `SDPOD_AUTO_PRINTER_LV_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinPrintersLv()` |

### `SDPOD_AUTO_PRINTER_LV_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinPrintersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinPrintersLv()` |

### `SDPOD_AUTO_ROUTER_LV_048` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinRoutersListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinRoutersListview()` |

### `SDPOD_AUTO_ROUTER_LV_049` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinRoutersLv()` |

### `SDPOD_AUTO_ROUTER_LV_050` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinRoutersLv()` |

### `SDPOD_AUTO_ROUTER_LV_051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinRoutersLv()` |

### `SDPOD_AUTO_ROUTER_LV_052` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinRoutersLv()` |

### `SDPOD_AUTO_ROUTER_LV_053` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinRouterslistview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinRouterslistview()` |

### `SDPOD_AUTO_ROUTER_LV_054` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinRoutersLv()` |

### `SDPOD_AUTO_ROUTER_LV_055` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinRoutersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinRoutersLv()` |

### `SDPOD_AUTO_SERVER_LV_134` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinServersLv()` |

### `SDPOD_AUTO_SERVER_LV_135` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinServersLv()` |

### `SDPOD_AUTO_SERVER_LV_136` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinServersLv()` |

### `SDPOD_AUTO_SERVER_LV_137` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinServersLv()` |

### `SDPOD_AUTO_SERVER_LV_138` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateServerLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateServerLv()` |

### `SDPOD_AUTO_SERVER_LV_139` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeServersLv()` |

### `SDPOD_AUTO_SERVER_LV_140` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteServersLv()` |

### `SDPOD_AUTO_SERVER_LV_141` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteServersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteServersLv()` |

### `SDPOD_AUTO_TAB_LV_342` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_343` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_344` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_345` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_346` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_348` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_347` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_349` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinTabletsLv()` |

### `SDPOD_AUTO_TAB_LV_350` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinTabletsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinTabletsLv()` |

### `SDPOD_AUTO_WS_LV_084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_085` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_086` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_087` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_088` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_089` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_096` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_090` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinWorkstationsLv()` |

### `SDPOD_AUTO_WS_LV_091` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinWorkstationsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinWorkstationsLv()` |

### `SDPOD_AUTO_PR_LV_213` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_214` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_215` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_216` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_217` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_219` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_218` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_220` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinProjectorLv()` |

### `SDPOD_AUTO_PR_LV_221` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinProjectorLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinProjectorLv()` |

### `SDPOD_AUTO_SCANNER_LV_232` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_233` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_234` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_235` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_236` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_238` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_237` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_239` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinScannersLv()` |

### `SDPOD_AUTO_SCANNER_LV_240` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinScannersLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinScannersLv()` |

### `SDPOD_AUTO_KB_LV_250` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAddtoGroupinKbLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAddtoGroupinKbLv()` |

### `SDPOD_AUTO_KB_LV_251` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConfigureDepreciationinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConfigureDepreciationinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_252` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoDepartmentinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoDepartmentinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_253` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAssigntoSiteinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAssigntoSiteinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_254` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyStateinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyStateinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_256` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninReprintBarcodeinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninReprintBarcodeinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_255` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninModifyProductinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninModifyProductinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_257` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileDeleteinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileDeleteinKeyboardsLv()` |

### `SDPOD_AUTO_KB_LV_258` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtonwhileBulkDeleteinKeyboardsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtonwhileBulkDeleteinKeyboardsLv()` |

### `SDPOD_AUTO_SP_LV_302` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `markasLonableSmartphoneAssetfromDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `markasLonableSmartphoneAssetfromDetailview()` |

### `SDPOD_AUTO_SP_LV_303` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addLoanfromSmartphoneDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addLoanfromSmartphoneDetailview()` |

### `SDPOD_AUTO_SP_LV_305` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `returnLoanfromSmartphoneDetailviewusingMenu()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `returnLoanfromSmartphoneDetailviewusingMenu()` |

### `SDPOD_AUTO_AP_LV_307` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `returnLoanfromSmartphoneDetailviewUsingActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `returnLoanfromSmartphoneDetailviewUsingActions()` |

### `SDPOD_AUTO_TAB_LV_340` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinTabletsListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinTabletsListviewActions()` |

### `SDPOD_AUTO_PR_LV_211` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinProjectorListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinProjectorListviewActions()` |

### `SDPOD_AUTO_SCANNER_LV_230` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinScannersListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinScannersListviewActions()` |

### `SDPOD_AUTO_KB_LV_248` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinKeyboardListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinKeyboardListviewActions()` |

### `SDPOD_AUTO_VH_LV_167` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinVirtualHostListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinVirtualHostListviewActions()` |

### `SDPOD_AUTO_VM_LV_192` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `modifyProductinVirtualMachineListviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `modifyProductinVirtualMachineListviewActions()` |

### `SDPOD_AUTO_VM_CV_098,SDPOD_AUTO_VM_CV_099` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createVirtualMachineAssetinCardView()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createVirtualMachineAssetinCardView()` |

### `SDPOD_AUTO_VM_CV_100` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addandRemoveFavoritesinAssetsCardViewinVH()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addandRemoveFavoritesinAssetsCardViewinVH()` |

### `SDPOD_AUTO_AP_LV_101` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkColumnchooserinAccessPointsListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `checkColumnchooserinAccessPointsListview()` |

### `SDPOD_AUTO_AP_LV_102` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createApwithDisposedstatus()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createApwithDisposedstatus()` |

### `SDPOD_AUTO_AP_LV_103` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createAptwithExpiredstatus()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createAptwithExpiredstatus()` |

### `SDPOD_AUTO_AP_LV_104` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createAccessPointAssetwithInRepairstatus()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `createAccessPointAssetwithInRepairstatus()` |

### `SDPOD_AUTO_WS_LV_093` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `validationtoChangeasServerinWorkstationDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `validationtoChangeasServerinWorkstationDetailview()` |

### `SDPOD_AUTO_AP_DV_156` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinAccessPointsDetailviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinAccessPointsDetailviewActions()` |

### `SDPOD_AUTO_WS_DV_155` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinWorkstationDetailviewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinWorkstationDetailviewActions()` |

### `SDPOD_AUTO_WS_DV_075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `updateCredentialsinWorkstationDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `updateCredentialsinWorkstationDetailview()` |

### `SDPOD_AUTO_VH_DV_159` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `updateCredentialsinVirtualHostDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `updateCredentialsinVirtualHostDetailview()` |

### `SDPOD_AUTO_VM_DV_184` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `updateCredentialsinVirtualMachineDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `updateCredentialsinVirtualMachineDetailview()` |

### `SDPOD_AUTO_AP_LV_150` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchAssetbyusingAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `searchAssetbyusingAssetTag()` |

### `SDPOD_AUTO_SP_LV_304` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `extendLoanfromSpDetailviewusingMenu()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `extendLoanfromSpDetailviewusingMenu()` |

### `SDPOD_AUTO_SP_LV_306` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `extendLoanfromSpDetailviewusingActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `extendLoanfromSpDetailviewusingActions()` |

### `SDPOD_AUTO_AST_LV_0017,SDPOD_AUTO_AP_LV_107` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `formValidationinAp()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `formValidationinAp()` |

### `SDPOD_AUTO_PRINTER_LV_035,SDPOD_AUTO_PRINTER_LV_108` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `formValidationinPrinters()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `formValidationinPrinters()` |

### `SDPOD_AUTO_ROUTER_LV_047,SDPOD_AUTO_ROUTER_LV_109` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `formValidationinRouter()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `formValidationinRouter()` |

### `SDPOD_AUTO_SERVER_LV_110,SDPOD_AUTO_SERVER_LV_133` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `ServersFormValidation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `ServersFormValidation()` |

### `SDPOD_AUTO_AP_LV_309` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditstatefromInUsetoInRepair()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditstatefromInUsetoInRepair()` |

### `SDPOD_AUTO_AP_LV_310` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditstatefromInRepairtoDisposed()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditstatefromInRepairtoDisposed()` |

### `SDPOD_AUTO_AP_LV_311` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditstatefromDisposedtoExpired()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditstatefromDisposedtoExpired()` |

### `SDPOD_AUTO_AP_DV_354` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `changeAccessPointStateinRHS()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `changeAccessPointStateinRHS()` |

### `SDPOD_AUTO_AP_LV_352` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assignUserfromAccessPointListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assignUserfromAccessPointListview()` |

### `SDPOD_AUTO_AP_DV_353` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assignorAssociateinAccessPointDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assignorAssociateinAccessPointDetailview()` |

### `SDPOD_AUTO_AP_LV_299,SDPOD_AUTO_AP_LV_300` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addLoanfromLoanRegistryinAccessPoint()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addLoanfromLoanRegistryinAccessPoint()` |

### `SDPOD_AUTO_SP_LV_301` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addLoanableAssetinAccessPoints()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addLoanableAssetinAccessPoints()` |

### `SDPOD_AUTO_AP_DV_357` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `copyAccessPointAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `copyAccessPointAsset()` |

### `SDPOD_AUTO_ROUTER_DV_429` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `copyRouterAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `copyRouterAsset()` |

### `SDPOD_AUTO_WS_LV_154` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `copyWorkStationAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `copyWorkStationAsset()` |

### `SDPOD_AUTO_SCANNER_DV_563` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditScannerName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditScannerName()` |

### `SDPOD_AUTO_WS_DV_376` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationName()` |

### `SDPOD_AUTO_ROUTER_DV_428` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditRouterName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditRouterName()` |

### `SDPOD_AUTO_SERVER_DV_437,SDPOD_AUTO_SERVER_DV_439,SDPOD_AUTO_SERVER_DV_440` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerName()` |

### `SDPOD_AUTO_VH_DV_461,SDPOD_AUTO_VH_DV_462,SDPOD_AUTO_VH_DV_463,SDPOD_AUTO_VH_DV_464` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostName()` |

### `SDPOD_AUTO_VM_DV_486,SDPOD_AUTO_VM_DV_487,SDPOD_AUTO_VM_DV_488,SDPOD_AUTO_VM_DV_489` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineName()` |

### `SDPOD_AUTO_PR_DV_543` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditProjectorName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditProjectorName()` |

### `SDPOD_AUTO_KB_DV_583` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditKeyboardName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditKeyboardName()` |

### `SDPOD_AUTO_WS_DV_380,SDPOD_AUTO_WS_DV_381` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationServiceTag()` |

### `SDPOD_AUTO_SERVER_DV_441,SDPOD_AUTO_SERVER_DV_442` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerServiceTag()` |

### `SDPOD_AUTO_VH_DV_465,SDPOD_AUTO_VH_DV_466` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostServiceTag()` |

### `SDPOD_AUTO_VM_DV_490,SDPOD_AUTO_VM_DV_491` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineServiceTag()` |

### `SDPOD_AUTO_SERVER_DV_445,SDPOD_AUTO_SERVER_DV_446` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerAssetTag()` |

### `SDPOD_AUTO_VH_DV_469,SDPOD_AUTO_VH_DV_470` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostAssetTag()` |

### `SDPOD_AUTO_VM_DV_494,SDPOD_AUTO_VM_DV_495` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineAssetTag()` |

### `SDPOD_AUTO_PR_DV_545` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditProjectorAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditProjectorAssetTag()` |

### `SDPOD_AUTO_KB_DV_585` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditKeyboardAssetTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditKeyboardAssetTag()` |

### `SDPOD_AUTO_WS_DV_386,SDPOD_AUTO_WS_DV_387` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationSerialNumber()` |

### `SDPOD_AUTO_SERVER_DV_447,SDPOD_AUTO_SERVER_DV_448` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerSerialNumber()` |

### `SDPOD_AUTO_VH_DV_471,SDPOD_AUTO_VH_DV_472` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostSerialNumber()` |

### `SDPOD_AUTO_VM_DV_496,SDPOD_AUTO_VM_DV_497` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineSerialNumber()` |

### `SDPOD_AUTO_PR_DV_546` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditProjectorSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditProjectorSerialNumber()` |

### `SDPOD_AUTO_KB_DV_586` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditKeyboardSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditKeyboardSerialNumber()` |

### `SDPOD_AUTO_SCANNER_DV_566` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditScannerSerialNumber()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditScannerSerialNumber()` |

### `SDPOD_AUTO_WS_DV_382,SDPOD_AUTO_WS_DV_383,SDPOD_AUTO_WS_DV_34,SDPOD_AUTO_WS_DV_385` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationOperatingSystem()` |

### `SDPOD_AUTO_VH_DV_467,SDPOD_AUTO_VH_DV_468` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostOperatingSystem()` |

### `SDPOD_AUTO_VM_DV_492,SDPOD_AUTO_VM_DV_493` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineOperatingSystem()` |

### `SDPOD_AUTO_WS_DV_391,SDPOD_AUTO_WS_DV_392` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationLocation()` |

### `SDPOD_AUTO_SERVER_DV_451,SDPOD_AUTO_SERVER_DV_452` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerLocation()` |

### `SDPOD_AUTO_VH_DV_475,SDPOD_AUTO_VH_DV_476` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostLocation()` |

### `SDPOD_AUTO_VM_DV_500,SDPOD_AUTO_VM_DV_501` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineLocation()` |

### `SDPOD_AUTO_PR_DV_548` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditProjectorLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditProjectorLocation()` |

### `SDPOD_AUTO_KB_DV_588` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditKeyboardLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditKeyboardLocation()` |

### `SDPOD_AUTO_ROUTER_DV_433` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditRouterLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditRouterLocation()` |

### `SDPOD_AUTO_SCANNER_DV_568` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditScannerLocation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditScannerLocation()` |

### `SDPOD_AUTO_WS_DV_390` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationPurchaseCost()` |

### `SDPOD_AUTO_SERVER_DV_449,SDPOD_AUTO_SERVER_DV_450` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerPurchaseCost()` |

### `SDPOD_AUTO_VH_DV_473,SDPOD_AUTO_VH_DV_474` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostPurchaseCost()` |

### `SDPOD_AUTO_VM_DV_498,SDPOD_AUTO_VM_DV_499` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachinePurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachinePurchaseCost()` |

### `SDPOD_AUTO_PR_DV_547` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditProjectorPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditProjectorPurchaseCost()` |

### `SDPOD_AUTO_KB_DV_587` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditKeyboardPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditKeyboardPurchaseCost()` |

### `SDPOD_AUTO_ROUTER_DV_432,SDPOD_AUTO_ROUTER_DV_434` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditRouterPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditRouterPurchaseCost()` |

### `SDPOD_AUTO_SCANNER_DV_567` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditScannerPurchaseCost()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditScannerPurchaseCost()` |

### `SDPOD_AUTO_WS_DV_388` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationBarCode()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationBarCode()` |

### `SDPOD_AUTO_ROUTER_DV_431` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditRouterVendor()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditRouterVendor()` |

### `SDPOD_AUTO_WS_DV_395,SDPOD_AUTO_WS_DV_396` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationHardwareOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationHardwareOperatingSystem()` |

### `SDPOD_AUTO_SERVER_DV_443,SDPOD_AUTO_SERVER_DV_444,SDPOD_AUTO_SERVER_DV_455,SDPOD_AUTO_SERVER_DV_456` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerHardwareOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerHardwareOperatingSystem()` |

### `SDPOD_AUTO_VH_DV_479,SDPOD_AUTO_VH_DV_480` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostHardwareOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostHardwareOperatingSystem()` |

### `SDPOD_AUTO_VM_DV_504,SDPOD_AUTO_VM_DV_505` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineHardwareOperatingSystem()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineHardwareOperatingSystem()` |

### `SDPOD_AUTO_WS_DV_397` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationHardwareServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationHardwareServiceTag()` |

### `SDPOD_AUTO_SERVER_DV_457,SDPOD_AUTO_SERVER_DV_458` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerHardwareServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerHardwareServiceTag()` |

### `SDPOD_AUTO_VH_DV_481,SDPOD_AUTO_VH_DV_482` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostHardwareServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostHardwareServiceTag()` |

### `SDPOD_AUTO_VM_DV_506` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineHardwareServiceTag()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineHardwareServiceTag()` |

### `SDPOD_AUTO_WS_DV_393,SDPOD_AUTO_WS_DV_394` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditWorkstationHardwareName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditWorkstationHardwareName()` |

### `SDPOD_AUTO_SERVER_DV_453,SDPOD_AUTO_SERVER_DV_454` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditServerHardwareName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditServerHardwareName()` |

### `SDPOD_AUTO_VH_DV_477,SDPOD_AUTO_VH_DV_478` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualHostHardwareName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualHostHardwareName()` |

### `SDPOD_AUTO_VM_DV_502,SDPOD_AUTO_VM_DV_503` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `spotEditVirtualMachineHardwareName()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `spotEditVirtualMachineHardwareName()` |

### `SDPOD_AUTO_PR_DV_559,SDPOD_AUTO_PR_DV_560,SDPOD_AUTO_PR_DV_561` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `projectorFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `projectorFinancialsCrud()` |

### `SDPOD_AUTO_SCANNER_DV_579,SDPOD_AUTO_SCANNER_DV_580,SDPOD_AUTO_SCANNER_DV_581` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `scannerFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `scannerFinancialsCrud()` |

### `SDPOD_AUTO_KB_DV_590,SDPOD_AUTO_KB_DV_591,SDPOD_AUTO_KB_DV_592,SDPOD_AUTO_KB_DV_606,SDPOD_AUTO_KB_DV_607,SDPOD_AUTO_KB_DV_608,SDPOD_AUTO_KB_DV_609,SDPOD_AUTO_KB_DV_610,SDPOD_AUTO_KB_DV_611` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `keyboardFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `keyboardFinancialsCrud()` |

### `SDPOD_AUTO_WS_DV_410,SDPOD_AUTO_WS_DV_411,SDPOD_AUTO_WS_DV_412,SDPOD_AUTO_WS_DV_413,SDPOD_AUTO_WS_DV_414,SDPOD_AUTO_WS_DV_415` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `workstationFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `workstationFinancialsCrud()` |

### `SDPOD_AUTO_VH_DV_517,SDPOD_AUTO_VH_DV_518,SDPOD_AUTO_VH_DV_519,SDPOD_AUTO_VH_DV_520,SDPOD_AUTO_VH_DV_521,SDPOD_AUTO_VH_DV_522` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `virtualHostFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `virtualHostFinancialsCrud()` |

### `SDPOD_AUTO_VM_DV_535,SDPOD_AUTO_VM_DV_536,SDPOD_AUTO_VM_DV_537,SDPOD_AUTO_VM_DV_538,SDPOD_AUTO_VM_DV_539,SDPOD_AUTO_VM_DV_540` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `virtualMachineFinancialsCrud()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `virtualMachineFinancialsCrud()` |

### `SDPOD_AUTO_AP_DV_358` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinAccessPointsDetailsViewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinAccessPointsDetailsViewActions()` |

### `SDPOD_AUTO_WS_DV_416` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinWorkstationDetailsViewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinWorkstationDetailsViewActions()` |

### `SDPOD_AUTO_VH_DV_523` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinVirtualhostDetailsViewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinVirtualhostDetailsViewActions()` |

### `SDPOD_AUTO_VM_DV_541` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `configureDepreciationinVirtualmachineDetailsViewActions()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `configureDepreciationinVirtualmachineDetailsViewActions()` |

### `SDPOD_AUTO_VH_LV_179` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchVirtualHostbyVmplatformffromListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `searchVirtualHostbyVmplatformffromListview()` |

### `SDPOD_AUTO_AP_LV_180` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyAccessPointAssetListviewValidations()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyAccessPointAssetListviewValidations()` |

### `SDPOD_AUTO_AP_LV_151` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchAccessPointAssetbyUsingAssetState()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `searchAccessPointAssetbyUsingAssetState()` |

### `SDPOD_AUTO_AP_LV_105` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyAccessPointAssetTypesinFilterinListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyAccessPointAssetTypesinFilterinListview()` |

### `SDPOD_AUTO_PRINTER_LV_152` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyPrinterAssetTypesinFilterinListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyPrinterAssetTypesinFilterinListview()` |

### `SDPOD_AUTO_WS_LV_113` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `gotoUnauditedWorkstations()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `gotoUnauditedWorkstations()` |

### `SDPOD_AUTO_AP_DV_351` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyHistoryinAddedAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyHistoryinAddedAsset()` |

### `SDPOD_AUTO_WS_DV_375,SDPOD_AUTO_WS_DV_377,SDPOD_AUTO_WS_DV_379` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyHistoryinWorkstationAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyHistoryinWorkstationAsset()` |

### `SDPOD_AUTO_AP_DV_360` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyConfigureDepreciationHistoryinAccessPoint()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyConfigureDepreciationHistoryinAccessPoint()` |

### `SDPOD_AUTO_AP_DV_359` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `verifyCopyAssetHistoryinAccessPoint()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `verifyCopyAssetHistoryinAccessPoint()` |

### `SDPOD_AUTO_AP_DV_355,SDPOD_AUTO_AP_DV_356` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addCostfromAssetDetailviewinAccessPoint()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addCostfromAssetDetailviewinAccessPoint()` |

### `SDPOD_AUTO_AP_DV_361` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinAccessPoint()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinAccessPoint()` |

### `SDPOD_AUTO_ROUTER_DV_417` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinRouter()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinRouter()` |

### `SDPOD_AUTO_SCANNER_DV_569` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinScanner()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinScanner()` |

### `SDPOD_AUTO_WS_DV_398` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinWorkstation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinWorkstation()` |

### `SDPOD_AUTO_PR_DV_555` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectProjectorinAddRelationshipsinWorkstation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectProjectorinAddRelationshipsinWorkstation()` |

### `SDPOD_AUTO_SCANNER_DV_575` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectScannerinAddRelationshipsinWorkstation()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectScannerinAddRelationshipsinWorkstation()` |

### `SDPOD_AUTO_PR_DV_549` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinProjector()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinProjector()` |

### `SDPOD_AUTO_VH_DV_507` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinVH()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinVH()` |

### `SDPOD_AUTO_VH_DV_513` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectVHinWsAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectVHinWsAddRelationships()` |

### `SDPOD_AUTO_AP_DV_370` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectAssetsinApPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectAssetsinApPopup()` |

### `SDPOD_AUTO_ROUTER_DV_418` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectAssetsinRouterpopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectAssetsinRouterpopup()` |

### `SDPOD_AUTO_PR_DV_550` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectAssetsinProjectorpopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectAssetsinProjectorpopup()` |

### `SDPOD_AUTO_VH_DV_508` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectAssetsinVirutalHostpopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectAssetsinVirutalHostpopup()` |

### `SDPOD_AUTO_AP_DV_369` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsbyUsingPlusSigninAccessPointRelationshipsSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsbyUsingPlusSigninAccessPointRelationshipsSubtab()` |

### `SDPOD_AUTO_WS_DV_404` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsbyUsingPlusinWsRelationshipsSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsbyUsingPlusinWsRelationshipsSubtab()` |

### `SDPOD_AUTO_ROUTER_DV_423` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsbyUsingPlusinRouterRelationshipsSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsbyUsingPlusinRouterRelationshipsSubtab()` |

### `SDPOD_AUTO_AP_DV_362` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinApAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinApAddRelationships()` |

### `SDPOD_AUTO_WS_DV_405` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinWorkstationAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinWorkstationAddRelationships()` |

### `SDPOD_AUTO_ROUTER_DV_424` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinRouterAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinRouterAddRelationships()` |

### `SDPOD_AUTO_PR_DV_556` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinProjectorAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinProjectorAddRelationships()` |

### `SDPOD_AUTO_SCANNER_DV_576` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinScannerAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinScannerAddRelationships()` |

### `SDPOD_AUTO_VH_DV_514` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinVirutalHostAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinVirutalHostAddRelationships()` |

### `SDPOD_AUTO_AP_DV_371` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinApRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinApRelationshipsinSubtab()` |

### `SDPOD_AUTO_WS_DV_400` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinWsRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinWsRelationshipsinSubtab()` |

### `SDPOD_AUTO_ROUTER_DV_419` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBssbyUsingPlusinRouterRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBssbyUsingPlusinRouterRelationshipsinSubtab()` |

### `SDPOD_AUTO_PR_DV_551` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinProjectorRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinProjectorRelationshipsinSubtab()` |

### `SDPOD_AUTO_SCANNER_DV_571` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinScannerRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinScannerRelationshipsinSubtab()` |

### `SDPOD_AUTO_VH_DV_509` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinVHRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinVHRelationshipsinSubtab()` |

### `SDPOD_AUTO_AP_DV_372` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectBsApPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectBsApPopup()` |

### `SDPOD_AUTO_ROUTER_DV_420` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectBsRouterPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectBsRouterPopup()` |

### `SDPOD_AUTO_PR_DV_552` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectBsProjectorPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectBsProjectorPopup()` |

### `SDPOD_AUTO_SCANNER_DV_572` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectBsScannerPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectBsScannerPopup()` |

### `SDPOD_AUTO_VH_DV_510` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectBsVirtualHostPopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectBsVirtualHostPopup()` |

### `SDPOD_AUTO_AP_DV_363,SDPOD_AUTO_AP_DV_364` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinAPAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinAPAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_WS_DV_402,SDPOD_AUTO_WS_DV_406` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinWsAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinWsAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_ROUTER_DV_425` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinRoutersAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinRoutersAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_PR_DV_557` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinProjectorsAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinProjectorsAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_SCANNER_DV_577` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinScannerAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinScannerAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_VH_DV_515` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinVirtualHostAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinVirtualHostAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_AP_DV_373` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusinApRelationshipsSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusinApRelationshipsSubtabandVerifyHistory()` |

### `SDPOD_AUTO_ROUTER_DV_421` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusinRouterRelationshipsSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusinRouterRelationshipsSubtabandVerifyHistory()` |

### `SDPOD_AUTO_PR_DV_553` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusinProjectorRelationshipsSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusinProjectorRelationshipsSubtabandVerifyHistory()` |

### `SDPOD_AUTO_SCANNER_DV_573` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusinScannerRelationshipsSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusinScannerRelationshipsSubtabandVerifyHistory()` |

### `SDPOD_AUTO_VH_DV_511` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusSigninVirtualHostRelationshipsinSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusSigninVirtualHostRelationshipsinSubtabandVerifyHistory()` |

### `SDPOD_AUTO_AP_DV_374` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinApAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinApAddRelationships()` |

### `SDPOD_AUTO_ROUTER_DV_422` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinRoutersAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinRoutersAddRelationships()` |

### `SDPOD_AUTO_PR_DV_554` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinProjectorAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinProjectorAddRelationships()` |

### `SDPOD_AUTO_SCANNER_DV_574` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinScannerAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinScannerAddRelationships()` |

### `SDPOD_AUTO_VH_DV_512` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinVHAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinVHAddRelationships()` |

### `SDPOD_AUTO_AP_DV_365,SDPOD_AUTO_AP_DV_366` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinApAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinApAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_WS_DV_408,SDPOD_AUTO_WS_DV_409` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinWsAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinWsAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_ROUTER_DV_426,SDPOD_AUTO_ROUTER_DV_427` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinRouterAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinRouterAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_PR_DV_558` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinProjectorAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinProjectorAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_SCANNER_DV_578` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinScannerAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinScannerAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_VH_DV_516` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinVHAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinVHAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_AP_DV_367,SDPOD_AUTO_AP_DV_368` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachandDetachComponenetinAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachandDetachComponenetinAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_VM_DV_525` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectAssetsinAddRelationshipsinVM()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectAssetsinAddRelationshipsinVM()` |

### `SDPOD_AUTO_VM_DV_531` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectVMinWsAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectVMinWsAddRelationships()` |

### `SDPOD_AUTO_VM_DV_526` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninConnectAssetsinVMpopup()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninConnectAssetsinVMpopup()` |

### `SDPOD_AUTO_VM_DV_532` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsinVMAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsinVMAddRelationships()` |

### `SDPOD_AUTO_VM_DV_527` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `connectBsbyUsingPlusinVMRelationshipsinSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `connectBsbyUsingPlusinVMRelationshipsinSubtab()` |

### `SDPOD_AUTO_VM_DV_529` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsbyUsingPlusinVMRelationshipsinSubtabandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsbyUsingPlusinVMRelationshipsinSubtabandVerifyHistory()` |

### `SDPOD_AUTO_VM_DV_530` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `cancelButtoninAttachAssetsinVMAddRelationships()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `cancelButtoninAttachAssetsinVMAddRelationships()` |

### `SDPOD_AUTO_VM_DV_533` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `attachAssetsinVMAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `attachAssetsinVMAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_VM_DV_534` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `associateUsersinVMAddRelationshipsandVerifyHistory()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `associateUsersinVMAddRelationshipsandVerifyHistory()` |

### `SDPOD_AUTO_DB_324` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `addAssetfromDashBoard()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `addAssetfromDashBoard()` |

### `SDPOD_AUTO_DB_325` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editAccessPointAssetviaDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `editAccessPointAssetviaDashboard()` |

### `SDPOD_AUTO_AP_LV_313` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `markasLoanableAssetfromApLV()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `markasLoanableAssetfromApLV()` |

### `SDPOD_AUTO_WS_LV_321` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `markasLoanableinWsLv()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `markasLoanableinWsLv()` |

### `SDPOD_AUTO_AP_LV_308` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditAccessPointinSecondTime()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditAccessPointinSecondTime()` |

### `SDPOD_AUTO_WS_LV_316,SDPOD_AUTO_WS_LV_320,SDPOD_AUTO_WS_LV_322` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditWorkstationAssetfromListview()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditWorkstationAssetfromListview()` |

### `SDPOD_AUTO_WS_LV_318` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditWorkstationinSecondTime()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditWorkstationinSecondTime()` |

### `SDPOD_AUTO_AP_LV_314,SDPOD_AUTO_AP_LV_315` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditLoanableApAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditLoanableApAsset()` |

### `SDPOD_AUTO_WS_LV_323` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `bulkEditLoanableWsAsset()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `bulkEditLoanableWsAsset()` |

### `SDPOD_AUTO_WS_LV_319` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `assignsameVHforVMinWs()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `assignsameVHforVMinWs()` |

### `SDPOD_AUTO_AUDIT_LV_0002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkRowActionButton()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkRowActionCancelButton()` |

### `SDPOD_AUTO_AUDIT_LV_0004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkAssetsInScopeTabinSelfAudit()` |
| 2 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `checkYettoStartFilter()` |

### `AssetAuditTechnicianConfigurationValidatorAssociateTech` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/assets/asset/AssetAudit.java` | `assetAuditTechnicianConfigurationAssociateTech()` |
| 2 | `com/zoho/automater/selenium/modules/assets/roles/SDAssetAuditAdmin.java` | `assetAuditTechnicianConfigurationAssociateTech()` |

### `SDPOD_CART_ISSUE_2505` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `createFifteenApprovalsInChangeForEachStage()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `createFifteenApprovalsInChangeForSubmissionStage()` |

### `DraftValidator` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `changeReplyForwardCase()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `problemReplyForwardCase()` |

### `DraftValidator_2` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `changeReplyForwardDraftCase()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `problemReplyForwardDraftCase()` |

### `SDP-CHG-MOD-1270` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifySchedulerButtonShouldNotPresentInTrashChange()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyFieldsPresentInChangeDetailsPopupFromListview()` |

### `SDPOD_ReqSuitePerf_4.1.1_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/PlanningStage.java` | `verifyApprovalStatusIsPresentInColumnChooserInRequestsInitiatedChange()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyApprovalStatusIsPresentInColumnChooserInPreviousRequestPopup()` |

### `SDPOD_RM_ASSOCIATION_357` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/PlanningStage.java` | `verifyCreateReleaseOverideEmptyValuesFunctionality()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/PlanningStage.java` | `verifyCreateReleaseOverideExistingValuesOverideFunctionality()` |

### `SDPOD_RM_ASSOCIATION_072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/PlanningStage.java` | `verifyDowntimesDissociatedHistoryInChange()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/PlanningStage.java` | `verifyNavigationOptionsInReleaseAssociation()` |

### `SDPOD_AUTO_CH_DV_308` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/change/UATStage.java` | `addDescriptionInUATDetailsSubtab()` |
| 2 | `com/zoho/automater/selenium/modules/changes/change/UATStage.java` | `editDescriptionInUATDetailsSubtab()` |

### `SDPOD_AUTO_RL_DV_542` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/changetask/PlanningTask.java` | `taskDependencyTreeInPlanningStage()` |
| 2 | `com/zoho/automater/selenium/modules/changes/changetask/ReleaseTask.java` | `taskDependencyTreeInReleaseStage()` |

### `SDPOD_AUTO_CH_DV_379, SDPOD_AUTO_CH_DV_378` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/changetask/ReleaseTask.java` | `deleteSingleTaskFromListViewButton()` |
| 2 | `com/zoho/automater/selenium/modules/changes/changetask/ReleaseTask.java` | `deleteMultipleTaskFromListViewButton()` |

### `SDPOD_CHANGE_TDT_27` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/changetask/SubmissionTask.java` | `verifyTaskDependencyForCustomOnholdStatusInChangeSubmissionStage()` |
| 2 | `com/zoho/automater/selenium/modules/changes/changetask/SubmissionTask.java` | `verifyAlertMsgAsDependencyAddOnlyForTasksInChangeSubmissionStage()` |

### `SDP-CHG-MOD-1205` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/changes/downtime/Downtime.java` | `verifyAddDowntimeButtonIsDisabledAndErrorMessageInChangeForm()` |
| 2 | `com/zoho/automater/selenium/modules/changes/downtime/Downtime.java` | `verifyAdded20DowntimeShouldPresentPlanningDetailsview()` |

### `SDPOD_AUTO_CMDB_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `editComputerinListview()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyHistoryinComputerCI()` |

### `SDPOD_AUTO_CMDB_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyMandatoryField()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `mandatorySymbolinSourceandDestinationCI()` |

### `SDPOD_CMDB_CI_DOWNTIME_150` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `releaseDowntimeTrash()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `changeDowntimeTrash()` |

### `SDPOD_CMDB_MOD_CI_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyCISelectedInModifyCItypePopupinCloseOption()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifyCISelectedInModifyCItypePopupinCancelOption()` |

### `SDPOD_CMDB_MOD_CI_133` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeParenttoChildAndVerifyLookupUdf()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeChildToParentAndVerifyLookupUdf()` |

### `SDPOD_CMDB_MOD_CI_172` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeParentToParentVerifySuggestedReleationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeParentToParentVerifyCustomReleationship()` |

### `SDPOD_CMDB_MOD_CI_173` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeChildToParentVerifySuggestedReleationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeChildToParentVerifyCustomReleationship()` |

### `SDPOD_CMDB_MOD_CI_174` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeChildToDiffParentVerifySuggestedReleationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeChildToDiffParentVerifyCustomReleationship()` |

### `SDPOD_CMDB_MOD_CI_175` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeCustomChildtoParentVerifySuggestedReleationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeCustomChildtoParentVerifyCustomReleationship()` |

### `SDPOD_CMDB_MOD_CI_176` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeCustomParentToChildVerifySuggestedReleationship()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `modifyCitypeCustomParentToChildVerifyCustomReleationship()` |

### `SDPOD_FGA_159,SDPOD_FGA_160,SDPOD_FGA_161,SDPOD_FGA_163,SDPOD_FGA_201` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `presenceProductTypeInCI()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `absenceProductTypeInCI()` |

### `SDPOD_CMDB_CI_DOWNTIME_125` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/roles/AddandEditRoleinCmdb.java` | `checkDowntimeInCICustomRole()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/roles/SDCMDBAdmin.java` | `checkDowntimeInCI()` |

### `SDPOD_CMDB_CI_DOWNTIME_126` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/roles/AddandEditRoleinCmdb.java` | `checkAddDowntimeCustomRole()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/roles/SDCMDBAdmin.java` | `checkAddDowntime()` |

### `SDPOD_CMDB_CI_DOWNTIME_127` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/cmdb/roles/AddandEditRoleinCmdb.java` | `downtimeEditPermission()` |
| 2 | `com/zoho/automater/selenium/modules/cmdb/roles/SDCMDBAdmin.java` | `downtimeEditPermission()` |

### `SDPOD_PO_Contract_Enhancements_150` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `checkNotAbleToChangeVendorVendorForCancelContract()` |
| 2 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `checkChangeVendorHistoryVerification()` |

### `SDPOD_PO_Con_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyTrashedContractDetailViewPageFromlistView()` |
| 2 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyTrashedContractDetailViewPageFromtemplateView()` |

### `ContractAutoRenewValidator` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `contractAutoRenewalCheckAddCase()` |
| 2 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `contractAutoRenewalCheckEditCase()` |

### `SDPOD_CART2502_CONTRACT_04,SDPOD_CART2502_CONTRACT_04` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `contractDraftToActiveWhileInlineEditTest()` |
| 2 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `markAsActiveForDraftedContract()` |

### `AnnouncementAssociationValidator` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `makeAnnouncementForChange()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `makeAnnouncementForRelease()` |

### `SDPOD_ANNOUNCEMENT_PHASE2_138` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `announcementTypeInAdmin()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/HelpdeskConfig.java` | `announcementTypeInAdmin()` |

### `AnnouncementTemplateValidator` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `AnnouncementEmailValidator()` |
| 2 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `AnnouncementTemplateValidator()` |

### `SDPOD_FGA_175,SDPOD_FGA_176,SDPOD_FGA_177` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `presenceAllowedAssetInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `absenceAllowedAssetInDashboard()` |

### `SDPOD_RM_STATUS_EN_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `openReleasesByReleaseRequester()` |
| 2 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `openReleasesByPriority()` |

### `SDPOD_CART2502_ADMIN_03` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `schedularLoadTestAfterTechConversion()` |
| 2 | `com/zoho/automater/selenium/modules/general/techavailabilitychart/TechAvailabilityChart.java` | `techAvailabilityChartLoadAfterTechConversion()` |

### `SDPOD_Accessibility_Enh_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableIncreaseContrast()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableIncreaseContrast()` |

### `SDPOD_Accessibility_Enh_010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableReadingMask()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableReadingMask()` |

### `SDPOD_Accessibility_Enh_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableFocusRing()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableFocusRing()` |

### `SDPOD_Accessibility_Enh_120` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableKeyboardShortcuts()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableKeyboardShortcuts()` |

### `SDPOD_Accessibility_Enh_128` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableHoverItem()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableHoverItem()` |

### `SDPOD_Accessibility_Enh_130` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableEmphasizeFocusArea()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableEmphasizeFocusArea()` |

### `SDPOD_Accessibility_Enh_137` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableClickToDragMode()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableClickToDragMode()` |

### `SDPOD_Accessibility_Enh_140` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableCustomCursor()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableCustomCursor()` |

### `SDPOD_Accessibility_Enh_148` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableCustomScrollbar()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableCustomScrollbar()` |

### `SDPOD_Accessibility_Enh_018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableHighlightCriticalInformation()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableHighlightCriticalInformation()` |

### `SDPOD_Accessibility_Enh_149` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `enableToastMessageDuration()` |
| 2 | `com/zoho/automater/selenium/modules/general/userpanel/Userpanel.java` | `disableToastMessageDuration()` |

### `SDPOD_MAIN_SCHEDULE_265` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `verifyHistoryShownProperlyForCompletedChangeMaintenance()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyHistoryShownProperlyForCompletedChangeMaintenance()` |

### `SDPOD_MAIN_SCHEDULE_258` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `verifyDeletedChangeMaintenanceIdInSystemLog()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyDeletedRequestMaintenanceIdInSystemLog()` |

### `SDPOD_MAIN_SCHEDULE_256` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `verifyScriptValueNotEncodedInChangeHistoryWhenInTaskTitle()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `verifyScriptNotEncodedInChangeHistorySubmissionStage()` |

### `78123` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/changemaintenance/ChangeMaintenance.java` | `verifyEventsShownProperlyInCalendarOnChangemaintenanceDetailPage()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyEventsShownProperlyInCalendarOnRequestMaintenanceDetailPage()` |

### `SDPOD_TLHCA_110` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyHelpcardPresentInRequestMaintanence()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyHelpcardPresentInServiceRequestMaintanence()` |

### `SDPOD_TLHCA_114` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyHelpcardNotPresentInServiceRequestMaintanence()` |
| 2 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `verifyHelpcardPresentInGeneratedRequestMaintanence()` |

### `SDPOD_AUTO_PB_LV_038` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTrashedProblemsHeader()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyUDFvaluesInRestoredProblem()` |

### `SDPOD_AUTO_PB_DV_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditReportedByDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `addTaskDetailview()` |

### `SDPOD_AUTO_PB_DV_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditSiteDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `organizeTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditGroupDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `closeTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditTechnicianDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `triggerTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_005` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditImpactDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `addTaskFromDropdownDetailView()` |

### `SDPOD_AUTO_PB_DV_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditUrgencyDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `addTaskFromTemplateDetailView()` |

### `SDPOD_AUTO_PB_DV_007` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditPriorityDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `editInLineTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditStatusDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `addTaskDependencyDetailView()` |

### `SDPOD_AUTO_PB_DV_009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditCategoryDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `editTaskDependencyDetailView()` |

### `SDPOD_AUTO_PB_DV_010` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditSubcategoryDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `closeMultipleTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditItemDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `triggerMultipleTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditDueByDateDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `viewTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditServicesAffctedDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `deleteTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditAssetsInvlovedDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `deleteInLineTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditCisInvlovedDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `deleteMultipleTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `spotEditReportedDateDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `addWorkaroundDetailview()` |

### `SDPOD_AUTO_PB_DV_018` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editDescriptionDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `editWorkaroundDetailview()` |

### `SDPOD_AUTO_PB_DV_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editStatusRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `addResolutionDetailview()` |

### `SDPOD_AUTO_PB_DV_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editPriorityRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `viewResolutionDetailview()` |

### `SDPOD_AUTO_PB_DV_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editKnownErrorToYesRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `editResolutionDetailview()` |

### `SDPOD_AUTO_PB_DV_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editTechnicianRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `viewImpactDetailsDetailview()` |

### `SDPOD_AUTO_PB_DV_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `associateIncidentRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `addRootCauseDetailview()` |

### `SDPOD_AUTO_PB_DV_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `associateChangeRHSDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `viewRootCauseDetailview()` |

### `SDPOD_AUTO_PB_DV_027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `addImpactDetailsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `editRootCauseDetailview()` |

### `SDPOD_AUTO_PB_DV_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `viewImpactDetailsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `addSymptomsDetailview()` |

### `SDPOD_AUTO_PB_DV_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editImpactDetailsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `viewSymptomsDetailview()` |

### `SDPOD_AUTO_PB_DV_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `addRootCauseDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `editSymptomsDetailview()` |

### `SDPOD_AUTO_PB_DV_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `viewRootCauseDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditingDeletingOthersNote.java` | `editNoteDetailView()` |

### `SDPOD_AUTO_PB_DV_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editRootCauseDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditingDeletingOthersNote.java` | `deleteNoteDetailView()` |

### `SDPOD_AUTO_PB_DV_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `viewSymptomsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `deleteTaskNotAllowed()` |

### `SDPOD_AUTO_PB_DV_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editSymptomsDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsAddingEditingTasks.java` | `deleteInLineTaskDetailViewNotAllowed()` |

### `SDPOD_AUTO_PB_DV_037` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `organizeTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifyAnalysis.java` | `addWorkaroundNotAllowed()` |

### `SDPOD_AUTO_PB_DV_039` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `closeTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsModifySolution.java` | `addingProblemTaskNotAllowedInThisRole()` |

### `SDPOD_AUTO_PB_DV_040` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `triggerTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `checkDeleteTaskDetailView()` |

### `SDPOD_AUTO_PB_DV_041` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `addTaskFromDropdownDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `addingProblemTaskNotAllowedInThisRole()` |

### `SDPOD_AUTO_PB_DV_042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `addTaskFromTemplateDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsDeleteTasks.java` | `addingImpactdetailsIsNotAllowed()` |

### `SDPOD_AUTO_PB_DV_044` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `editInLineTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditingDeletingOthersNote.java` | `addWorkaroundNotAllowedInThisRole()` |

### `SDPOD_AUTO_PB_DV_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `organizeMultipleTaskDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsEditingDeletingOthersNote.java` | `addingProblemTaskNotAllowedInThisRole()` |

### `SDPOD_PR_Trash_167_PB` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyReminderInRestoredProblem()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemsFullControl.java` | `verifyReminderInRestoredProblem()` |

### `Problem_Enhancements` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyConversationInHistoryDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAssetIconsInDetailview()` |

### `SDPOD_PB_CART_2501_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyTitleAndAttachment()` |
| 2 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `unknown()` |

### `SDPOD_RM_ASSOCIATION_176` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyAttachDetachReleaseIniatedByMilestonesOptions()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyNewReleaseIniatedByMilestonesOptions()` |

### `SDPOD_RM_ASSOCIATION_209` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyAssociationOptionsAfterTrashMilestone()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyReleaseNotDissociatedAfterTrashMilestone()` |

### `SDP_ProjMulChangeAssoc_101` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `attachButtonNotDisplayedAfterAssociatingChange()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `changeRemovedInAsssociationWhenTrashed()` |

### `SDP_ProjMulChangeAssoc_120` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyFunctionalityOfCloseInChangeInitatedProject()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/Project.java` | `verifyPriorityValueCopiedFromProjectInNewChangeOption()` |

### `SDPOD_AUTO_PROJ_DV_079` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachAssociateRequestsInRHS()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `attachDetachAssociateRequestsInRHSInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_080` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachAssociateReleasesInRHS()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `attachDetachAssociateReleasesInRHSInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_069` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSStatusToOnhold()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSStatusToOnholdInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_070` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSStatusToCanceled()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSStatusToCanceledInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_071` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSStatusToClosed()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSStatusToClosedInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSPriorityToHigh()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSPriorityToHighInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_073` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSPriorityToLow()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSPriorityToLowInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_074` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSPriorityToMedium()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSPriorityToMediumInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSPriorityToNormal()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSPriorityToNormalInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_076` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSOwner()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSOwnerInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_077` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSMilestones()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSMilestonesInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_078` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewRHSTasks()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewRHSTasksInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_082` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewAddComments()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewAddCommentsInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_083` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewEditComments()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewEditCommentsInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `projectDetailviewDeleteComments()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `projectDetailviewDeleteCommentsInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_086` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `closeProjectindetailview()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `closeProjectindetailviewInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_087` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `editProjectOnceClosedInDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `editProjectOnceClosedInDetailviewInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_088` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `timesheetInDetailview()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `timesheetInDetailviewInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_096` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `copyProjectFromActionsDropdown()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `copyProjectFromActionsDropdownInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_098` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `deleteProjectFromActionsDropdown()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `deleteProjectFromActionsDropdownInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_DV_106` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `spotEditStatusToOpenAndVerifyInHistory()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `verifyAscendingDescendingIconInHistory()` |

### `SDPOD_AUTO_PROJ_LV_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `createUsingDefaultProjectTemplateAPI()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `viewProjectInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_LV_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `editProjectUsingSettingsIcon()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `editProjectUsingSettingsIconInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_LV_007` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `copyProjectTemplateUsingSettingsIcon()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `copyProjectTemplateUsingSettingsIconInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_LV_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `OnholdProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `OnholdProjectsFiltersInDefaultProjectManagementRole()` |

### `SDPOD_AUTO_PROJ_LV_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `openProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `openProjectsFiltersInDefaultProjectManagementRole()` |

### `SDPOD_AUTO_PROJ_LV_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `canceledProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `canceledProjectsFiltersInDefaultProjectManagementRole()` |

### `SDPOD_AUTO_PROJ_LV_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `closedProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `closedProjectsFiltersInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_LV_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `completedProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `completedProjectsFiltersInDefaultProjectManagerRole()` |

### `SDPOD_AUTO_PROJ_LV_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `pendingProjectsFilters()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `pendingProjectsFiltersInDefaultProjectManagerRole()` |

### `SDPOD_OM_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `organizeBtnPresentForViewEditRole()` |
| 2 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `assignOwnerBtnPresentInMilestoneForViewEditRole()` |

### `SDPOD_AUTO_PROJ_DV_040` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `quickAddTaskInProject()` |
| 2 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `quickAddTaskInProjectInDefaultProjectManagerRole()` |

### `SDPOD_Task_Com_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `addTaskCommentsAsScriptTagsInProject()` |
| 2 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `verifyUpdatedProjectTaskCommentsInHistory()` |

### `SDPOD_AUTO_PURCHASE_5` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `deletePurchaseFromDetailsTest()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderdelete/PurchaseOrderDelete.java` | `deletePurchaseFromDetailsTest()` |

### `SDPOD_AUTO_PURCHASE_6` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `deletePurchaseFromListViewTest()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderdelete/PurchaseOrderDelete.java` | `deletePurchaseFromListViewTest()` |

### `SDPOD_AUTO_PURCHASE_7` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `bulkDeletePurchaseFromListViewTest()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderdelete/PurchaseOrderDelete.java` | `bulkDeletePurchaseFromListViewTest()` |

### `SDPOD_AUTO_PURCHASE_25` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `deletePurchaseFromTrash()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderdelete/PurchaseOrderDelete.java` | `deletePurchaseFromTrash()` |

### `SDPOD_PO_Contract_Enhancements_041` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `addNoteInConversationPageInPurchase()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `addNoteInConversationPageInPurchase()` |

### `SDPOD_AUTO_PURCHASE_EDIT_1` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderdelete/PurchaseOrderDelete.java` | `verifyAbsenceofActionButtons()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderedit/PurchaseOrderEdit.java` | `verifyAbsenceofActionButtons()` |

### `SDPOD_AUTO_PURCHASE_VIEW_8` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `viewInvoicePO()` |
| 2 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `viewPaymentPO()` |

### `SDPOD_AUTO_RL_DV_562` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `editFromDetailsPageActions()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/ReviewTask.java` | `spotEditPicklistFieldFromDetailsTabinReviewStage()` |

### `SDPOD_RM_ASSOCIATION_288` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `associateProjectToReleaseInAssociationsPage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `dissociateProjectToReleaseInAssociationsPage()` |

### `SDPOD_LINKING_RL_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyParentPopupFormForOtherSiteRelease()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifySubReleasePopupFormForOtherSiteRelease()` |

### `SDPOD_LINKING_RL_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyAssociatedSubReleaseWithDifferentSite()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseAssociations.java` | `verifyAssociatedParentReleaseWithDifferentSite()` |

### `SDPOD_RM_Roles_ENH_594,SDPOD_RM_Roles_ENH_602` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInSubmissionStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInSubmissionStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_595,SDPOD_RM_Roles_ENH_603` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInPlanningStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInPlanningStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_596,SDPOD_RM_Roles_ENH_604` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInDevelopmentStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInDevelopmentStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_597,SDPOD_RM_Roles_ENH_605` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInTestingStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInTestingStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_598,SDPOD_RM_Roles_ENH_606` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInUATStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInUATStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_599,SDPOD_RM_Roles_ENH_607` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInDeploymentStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInDeploymentStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_600,SDPOD_RM_Roles_ENH_608` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInTrainingStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInTrainingStageFromRequesterLogin()` |

### `SDPOD_RM_Roles_ENH_601,SDPOD_RM_Roles_ENH_609` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditProminentRolesInReviewStageFromRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `notAllowsToAddOrEditNonProminentRolesInReviewStageFromRequesterLogin()` |

### `SDPOD_RM_WORKFLOW_ENC_067` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/release/ReleaseWorkflow.java` | `addTaskInCustomStageWhenAllStageIsApplied()` |
| 2 | `com/zoho/automater/selenium/modules/releases/release/ReleaseWorkflow.java` | `triggerTaskInCustomStageWhenAllStageIsApplied()` |

### `SDPLIVE_RELEASE_STAGETASK_056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/DeploymentTask.java` | `verifyMandatoryFieldForTitleInAddTaskPopupInDeploymentStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `verifyMandatoryFieldForTitleInAddTaskPopupInSubmissionStage()` |

### `SDPLIVE_RELEASE_STAGETASK_416` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/PlanningTask.java` | `verifyCancelBtnInAddTaskPopupInPlanningStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/ReviewTask.java` | `verifyCancelBtnInAddTaskPopupInReviewStage()` |

### `SDPLIVE_RELEASE_STAGETASK_169` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/PlanningTask.java` | `verifyMandatoryFieldForTitleInEditTaskPopupInPlanningStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `verifyMandatoryFieldForTitleInEditTaskPopupInSubmissionStage()` |

### `SDPOD_Release_TDT_30` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `verifyAlertMessageAsCircularDependencyInSubmissionStage()` |
| 2 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `deleteTaskDependencyInSubmissionStage()` |

### `SDPOD_LINKING_RL_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/roles/FullControlAssociatedSites.java` | `verifyUnauthorisedParentReleaseNotDisplayed()` |
| 2 | `com/zoho/automater/selenium/modules/releases/roles/FullControlAssociatedSites.java` | `verifyUnauthorisedSubReleaseNotDisplayed()` |

### `SDPOD_LINKING_RL_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/releases/roles/FullControlAssociatedSites.java` | `verifyUnauthorisedParentReleaseDisplayedCount()` |
| 2 | `com/zoho/automater/selenium/modules/releases/roles/FullControlAssociatedSites.java` | `verifyUnauthorisedSubReleaseDisplayedCount()` |

### `8617937` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkRequestisDisplayedIfRequesterisDeleteed()` |
| 2 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkRequestisDisplayedinKanbanViewIfRequesterisDeleteed()` |

### `53242` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkConversionTabMsginArchivedRequestsFilter()` |
| 2 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkUnknownErrorisDisplayedinRequesterDetails()` |

### `SDPOD_REQCANCEL_089` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentRequestCancel.java` | `CheckDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/ServiceRequestCancel.java` | `CheckDuplicateRequest()` |

### `SDPOD_REQCANCEL_090` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentRequestCancel.java` | `CheckStatusDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/ServiceRequestCancel.java` | `CheckStatusDuplicateRequest()` |

### `SDPOD_REQCANCEL_091` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentRequestCancel.java` | `CheckStatusFunctionDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/ServiceRequestCancel.java` | `CheckStatusFunctionDuplicateRequest()` |

### `SDPOD_REQCANCEL_259` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentRequestCancel.java` | `CheckDisplayApprovedAndRejectetButton()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/ServiceRequestCancel.java` | `CheckDisplayedApprovalTechnicinNoEditPermission()` |

### `SDPOD_Date_UDF_Request_361` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentRequestDateUdf.java` | `checkAddMoreUdf()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestDateUdf.java` | `checkAddMoreUdf()` |

### `SDPOD_ShareRequest_TC001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/IncidentShareRequest.java` | `checkSharerequestPermission()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/IncidentShareRequest.java` | `checkSharerequestPer()` |

### `SDPOD_REQCANCEL_239` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestCancel.java` | `checkBRRuleDisabled()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestCancel.java` | `checkBRRuleExecuted()` |

### `SDPOD_CHECKLIST_REQ_46` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkEditAvailabeItemsTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkEditAvailabeItemsTemp()` |

### `SDPOD_CHECKLIST_REQ_47` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkEditNewItemstemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkEditNewItemstemp()` |

### `SDPOD_CHECKLIST_REQ_49` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkDeleteAvailabeItemsWithTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkDeleteAvailabeItemsWithTemp()` |

### `SDPOD_CHECKLIST_REQ_50` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkDeleteNewItemsTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkDeleteNewItemsTemp()` |

### `SDPOD_CHECKLIST_REQ_74_2` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkEditCheckListCustomTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkEditCheckList()` |

### `SDPOD_CHECKLIST_REQ_76_2` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkNewCheckListButtonInSDSiteAdminRoleExistTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkNewCheckListButtonInSDSiteAdminRoleExistTemp()` |

### `SDPOD_CHECKLIST_REQ_76_3` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkDisAssociateInSDSiteAdminRoleExistTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkDisAssociateInSDSiteAdminRoleExistTemp()` |

### `SDPOD_CHECKLIST_REQ_77_3` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkAddCheckListInSDCoordinatorRoleExistTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkAddCheckListInSDCoordinatorRoleExistTemp()` |

### `SDPOD_CHECKLIST_REQ_77_4` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkDisAssociateInSDCoordinatorRoleExistTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkDisAssociateInSDCoordinatorRoleExistTemp()` |

### `SDPOD_CHECKLIST_REQ_107` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkDuplicate()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkDuplicateService()` |

### `SDPOD_CHECKLIST_REQ_108` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkSplitRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkSplitRequest()` |

### `SDPOD_CHECKLIST_REQ_109` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkChangeTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkChangeTemplate()` |

### `SDPOD_CHECKLIST_REQ_139` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/RequestCheckList.java` | `checkCheckListFromChangeTemplate()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestChecklist/ServiceRequestCheckList.java` | `checkChecklistFromChangeTemplate()` |

### `SDP-FILTER-0001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestCustomFilter.java` | `checkNewCustomView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestCustomFilter.java` | `checkNewCustomView1()` |

### `SDPOD_REQUEST_UDF_LOOKUP_457` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequestLookupFieldFunctionality.java` | `checkUserUdfReq()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequestLookupFieldFunctionality.java` | `checkDesdepartmentHeadGenerics()` |

### `SDP-SR-DP-1468` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequesterDetailsInRDP.java` | `updateServiceRequestWithContactNumber()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequesterDetailsInRDP.java` | `updateServiceRequestWithAlphebetInContactNumber()` |

### `TC_SDPOD_REQUESTER_EDIT_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `checkEditListView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `checkTechnicianGroupAndStatusFieldArePresent()` |

### `TC_SDPOD_REQUESTER_EDIT_023_4` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `checkEditSla()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `editMode()` |

### `TC_SDPOD_REQUESTER_EDIT_106_1` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `checkEditBothReq()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/RequesterEdit.java` | `checkSpotEditWithService()` |

### `SDP-SR-DP-0387` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/details/IncidentRequestDetailsPage.java` | `updateStatusToOnHold()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/details/ServiceRequestDetailsPage.java` | `updateStatusToOnHold()` |

### `SDP-SR-DP-0364` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/details/IncidentRequestDetailsPage.java` | `checkSiteDetailsIcon()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/details/ServiceRequestDetailsPage.java` | `checkSiteDetailsIcon()` |

### `SDP-SR-DP-1132` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/details/RequestDetailsPage.java` | `checkCreateDateAlertMessage()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/details/RequestDetailsPage.java` | `checkDueDateAlertMessage()` |

### `SDP_REQ_LS_AAA001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `create()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `create()` |

### `SDP_REQ_LS_AAA020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `createRequestAPI()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `createRequestAPI()` |

### `SDP_REQ_LS_AAA009` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `splitRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `splitRequest()` |

### `SDP_REQ_LS_AAA030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `bulkDelete()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `bulkDelete()` |

### `SDP_REQ_LS_AAA089` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `goToRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `goToRequest()` |

### `SDP_REQ_DV_AAA114` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `spotEditHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `spotEditHistoryVerification()` |

### `SDP_REQ_LS_AAA016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `createIncidentFromAsset()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `createIncidentFromAsset()` |

### `SDP_REQ_LS_AAA053` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `openRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `openRequestFilters()` |

### `SDP_REQ_LS_AAA067` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `onHoldRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `onHoldRequestFilters()` |

### `SDP_REQ_LS_AAA068` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `myOnHoldRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `myOnHoldRequestFilters()` |

### `SDP_REQ_LS_AAA063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `myPendingRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `myPendingRequestFilters()` |

### `SDP_REQ_LS_AAA066` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `myOpenUnassignedRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `myOpenUnassignedRequestFilters()` |

### `SDP_REQ_LS_AAA107` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `myOpenRequestFilters()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `myOpenRequestFilters()` |

### `SDP_REQ_DV_AAA069` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `subjectHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `subjectHistoryVerification()` |

### `SDP_REQ_LS_AAA023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `trashRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `trashRequest()` |

### `SDP_REQ_LS_AAA021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `restoreTrashedRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `restoreTrashedRequest()` |

### `SDP_REQ_LS_AAA028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `assignRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `assignRequest()` |

### `SDP_REQ_LS_AAA073` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `archiveRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `archiveRequest()` |

### `SDP_REQ_LS_AAA075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteArchiveRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteArchiveRequest()` |

### `SDP_REQ_LS_AAA026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequest()` |

### `SDPOD_MERGE_REQUEST_INFO_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequestinformationTag()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequestinformationTag()` |

### `SDPOD_MERGE_REQUEST_INFO_002` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequestinformationTagSDAdmin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequestinformationTagSDAdmin()` |

### `SDPOD_MERGE_REQUEST_INFO_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequestinformationTagSDAdminViewPermission()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequestinformationTagSDAdminViewPermission()` |

### `SDPOD_MERGE_REQUEST_INFO_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequestinformationTagFullPermission()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequestinformationTagFullPermission()` |

### `SDPOD_MERGE_REQUEST_INFO_005` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeRequestinformationTagOwnRequestPermissionInRequester()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeRequestinformationTagEditor()` |

### `SDP_REQ_LS_AAA027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `link2Request()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `link2Request()` |

### `SDP_REQ_LS_AAA042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editFromListViewActions()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editFromListViewActions()` |

### `SDP_REQ_LS_AAA091` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addNotesFromListView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addNotesFromListView()` |

### `SDP_REQ_DV_AAA154` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verificationOfNotesinConversation()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verificationOfNotesinConversation()` |

### `SDP_REQ_LS_AAA095` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteTrashedRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteTrashedRequest()` |

### `SDP_REQ_LS_AAA040` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `conversationsFromListview()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `conversationsFromListview()` |

### `SDP_REQ_DV_AAA072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `statusHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `statusHistoryVerification()` |

### `SDP_REQ_DV_AAA077` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `priorityHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `priorityHistoryVerification()` |

### `SDP_REQ_DV_AAA079` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `groupHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `groupHistoryVerification()` |

### `SDP_REQ_DV_AAA082` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `markFCRHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `markFCRHistoryVerification()` |

### `SDP_REQ_DV_AAA084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addNotesHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addNotesHistoryVerification()` |

### `SDP_REQ_DV_AAA127` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `statusHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `statusHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA129` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `technicianHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `technicianHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA085` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteNotesHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteNotesHistoryVerification()` |

### `SDP_REQ_DV_AAA130` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `worklogStartHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `worklogStartHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA132` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `worklogStopHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `worklogStopHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA131` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `worklogAddHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `worklogAddHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA133` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `resolveHistoryVerificationRHS()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `resolveHistoryVerificationRHS()` |

### `SDP_REQ_DV_AAA057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteworklog()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteworklog()` |

### `SDP_REQ_DV_AAA037` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `saveAndAddResolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `saveAndAddResolution()` |

### `SDP_REQ_DV_AAA041` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addReminder()` |

### `SDP_REQ_DV_AAA042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editReminder()` |

### `SDP_REQ_DV_AAA043` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteReminder()` |

### `SDP_REQ_DV_AAA045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteAlertReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteAlertReminder()` |

### `SDP_REQ_DV_AAA047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `reqIdinReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `reqIdinReminder()` |

### `SDP_REQ_DV_AAA049` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `closeReminderPopup()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `closeReminderPopup()` |

### `SDP_REQ_DV_AAA046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addReminderValidation()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addReminderValidation()` |

### `SDP_REQ_DV_AAA050` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `markasCompletedReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `markasCompletedReminder()` |

### `SDP_REQ_DV_AAA051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `markasOpenReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `markasOpenReminder()` |

### `SDP_REQ_DV_AAA052` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `statusPopupReminder()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `statusPopupReminder()` |

### `SDP_REQ_DV_AAA087` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteTaskHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteTaskHistoryVerification()` |

### `SDP_REQ_DV_AAA095` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `assignRequestHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `assignRequestHistoryVerification()` |

### `SDP_REQ_DV_AAA096` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `linkRequestHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `linkRequestHistoryVerification()` |

### `SDP_REQ_DV_AAA026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `organizeTask()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `organizeTask()` |

### `SDP_REQ_DV_AAA097` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deLinkRequestHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deLinkRequestHistoryVerification()` |

### `SDP_REQ_DV_AAA088` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addResolutionHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addResolutionHistoryVerification()` |

### `SDP_REQ_DV_AAA089` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editResolutionHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editResolutionHistoryVerification()` |

### `SDP_REQ_DV_AAA038` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `copyFromSolutions()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `copyFromSolutions()` |

### `SDP_REQ_DV_AAA027` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `triggerTask()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `triggerTask()` |

### `SDP_REQ_DV_AAA029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addTaskCancelandClose()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addTaskCancelandClose()` |

### `SDP_REQ_DV_AAA155` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editNotesFromDP()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editNotesFromDP()` |

### `SDP_REQ_DV_AAA116` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `timePickerhistoryTab()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `timePickerhistoryTab()` |

### `SDP_REQ_DV_AAA150` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `changeCausedByRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `changeCausedByRequest()` |

### `SDP_REQ_DV_AAA063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `saveDraftinReply()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `saveDraftinReply()` |

### `SDP_REQ_DV_AAA064` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteDraftinReply()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteDraftinReply()` |

### `SDP_REQ_LS_AAA056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestCreatedToday()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requestCreatedToday()` |

### `SDP_REQ_LS_AAA029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `editMultipleRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `editMultipleRequest()` |

### `SDP_REQ_LS_AAA025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `closeRequestListview()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `closeRequestListview()` |

### `SDP_REQ_LS_AAA032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `bulkcloseRequestListview()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `bulkcloseRequestListview()` |

### `SDP_REQ_LS_AAA033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `bulkmergeRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `bulkmergeRequest()` |

### `SDP_REQ_LS_AAA034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `bulkRequestLink()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `bulkRequestLink()` |

### `SDP_REQ_DV_AAA083` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `unMarkFCRHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `unMarkFCRHistoryVerification()` |

### `SDP_REQ_DV_AAA086` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addTaskHistoryVerification()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addTaskHistoryVerification()` |

### `SDP_REQ_LS_AAA044` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `createCustomViewFilter()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `createCustomViewFilter()` |

### `SDP_REQ_LS_AAA090` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterDeleteHeader()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterDeleteHeader()` |

### `SDP_REQ_LS_AAA093` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterHeaders()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterHeaders()` |

### `SDP_REQ_LS_AAA046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterDeleteDropdown()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterDeleteDropdown()` |

### `SDP_REQ_LS_AAA098` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterAddFavourite()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterAddFavourite()` |

### `SDP_REQ_LS_AAA099` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterRemoveFavourite()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterRemoveFavourite()` |

### `SDP_REQ_LS_AAA102` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `customViewFilterUnPinFavorite()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `customViewFilterUnPinFavorite()` |

### `SDP_REQ_LS_AAA081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteAlert()` |

### `SDP_REQ_LS_AAA082` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `pickUpAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `pickUpAlert()` |

### `SDP_REQ_LS_AAA083` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `closeAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `closeAlert()` |

### `SDP_REQ_LS_AAA084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `mergeAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `mergeAlert()` |

### `SDP_REQ_LS_AAA085` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `linkAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `linkAlert()` |

### `SDP_REQ_LS_AAA086` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `assignAlert()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `assignAlert()` |

### `SDP_REQ_LS_AAA096` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestTypeHeaderInArchivedList()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requestTypeHeaderInArchivedList()` |

### `SDP_REQ_LS_AAA097` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestTypeHeaderInRequestListview()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requestTypeHeaderInRequestListview()` |

### `SDP_REQ_LS_AAA076` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestTypeIncidentArchivedFilter()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requestTypeIncidentArchivedFilter()` |

### `SDP_REQ_LS_AAA077` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestTypeServiceArchivedFilter()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `requestTypeServiceArchivedFilter()` |

### `SDP_REQ_DV_AAA068` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `historyTab()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `historyTab()` |

### `SDP_REQ_DV_AAA156` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `historyTabHeaders()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `historyTabHeaders()` |

### `SDPOD_ReqSuitePerf_4.1.1_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyNoteFromPreviousRequestPopup()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyNoteFromPreviousRequestPopup()` |

### `SDP_REQ_DV_AAA157` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `replyAllRequestInDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `replyAllRequestInDetailView()` |

### `SDP_REQ_DV_AAA159` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `iconForwardRequestInDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `iconForwardRequestInDetailView()` |

### `SDP_REQ_DV_AAA160` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `replyFromConversationRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `replyFromConversationRequest()` |

### `SDP_REQ_DV_AAA161` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `resendFromConversationRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `resendFromConversationRequest()` |

### `SDP_REQ_DV_AAA162` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `deleteConversationFromRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `deleteConversationFromRequest()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByQuickRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByCancelRequest()` |

### `SDPOD_AUTO_REQ_LSTUPDATED_BY012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByRequesterEdit()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByRequesterEdit()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_021` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByMergeRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedByEditBulkrequest()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByRequestertemplate()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByRequestertemplate()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByEditBulkrequestSDadmin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByEditBulkrequestSDadmin()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedServiceTemplateFromIncidentTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedServiceTemplateFromIncidentTemp()` |

### `SDPOD_AUTO_REQ_SR_LST_UPDATED_BY_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByInctoService()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByInctoService()` |

### `SDPOD_AUTO_REQ_SR_LST_UPDATED_BY_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastupdatedByInctoServiceSDadminlogin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastupdatedByInctoServiceSDadminlogin()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastUpdatedByCustomFilterTempviewSdadmin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastUpdatedByCustomFilterTempviewSdadmin()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyCloumnChooserLastupdatedbySDadmin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyCloumnChooserLastupdatedbySDadmin()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastUpdatedByCustomFilterRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastUpdatedByCustomFilterRequesterLogin()` |

### `SDPOD_AUTO_REQ_LST_UPDATED_BY_048` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyLastUpdatedByCustomFilterArchiveRequests()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyLastUpdatedByCustomFilterArchiveRequests()` |

### `SDPOD_Notes Attachment And Mentions_046,SDPOD_Notes Attachment And Mentions_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAbleToAddNoteAndAttachmentInDashboard()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyShouldNotViewNoteAndAttachmentInDashboardOnceDeleted()` |

### `SDP_AUTO_REQ_CART2402_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `incidentTemplateCopyWithServiceCategory()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `incidentTemplateCopyWithServiceCategory()` |

### `SDPOD_Req_Sol_003,SDPOD_Req_sol_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `CheckRejectedSearchSolutions()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `CheckRejectedSearchSolutions()` |

### `SDPOD_Req_Sol_005,SDPOD_Req_Sol_006` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `checkRejectedStatusFilterPresent()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `checkRejectedStatusFilterPresent()` |

### `SDPOD_Req_sol_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionForNewRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionForNewRequest()` |

### `SDPOD_Req_Sol_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionDetach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionDetach()` |

### `SDPOD_Req_Sol_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `MultipleSelectSolutionAttach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `MultipleSelectSolutionAttach()` |

### `SDPOD_Req_Sol_014` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionCount()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionCount()` |

### `SDPOD_Req_Sol_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionHover()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionHover()` |

### `SDPOD_Req_Sol_016` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `DetachIconPresence()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `DetachIconPresence()` |

### `SDPOD_Req_Sol_017` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionDetailView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionDetailView()` |

### `SDPOD_Req_Sol_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionDescriptionforDetach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionDescriptionforDetach()` |

### `SDPOD_Req_Sol_020` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionViewDetailPopup()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionViewDetailPopup()` |

### `SDPOD_Req_Sol_021, SDPOD_Req_Sol_004` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `TrashedSolutioninReferredSolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `TrashedSolutioninReferredSolution()` |

### `SDPOD_Req_Sol_022` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `AlreadyAssociatedSolutionList()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `AlreadyAssociatedSolutionList()` |

### `SDPOD_Req_Sol_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `AlreadyAssociatedSolutionDescription()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `AlreadyAssociatedSolutionDescription()` |

### `SDPOD_Req_Sol_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `AlreadyAssociatedSolutionCount()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `AlreadyAssociatedSolutionCount()` |

### `SDPOD_Req_Sol_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionTemplateForRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionTemplateForRequest()` |

### `SDPOD_Req_Sol_031` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionCopyPOPUP()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionCopyPOPUP()` |

### `SDPOD_Req_Sol_030` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionCOPYAttach()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionCOPYAttach()` |

### `SDPOD_Req_Sol_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionCOPYDescription()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionCOPYDescription()` |

### `SDPOD_Req_Sol_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionCopyForEditRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionCopyForEditRequest()` |

### `SDPOD_Req_Sol_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SuggestedSolutionHideForRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SuggestedSolutionHideForRequest()` |

### `SDPOD_Req_Sol_043` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyResolutionToLinkedRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyResolutionToLinkedRequest()` |

### `SDPOD_Req_Sol_045, SDPOD_Req_Sol_067` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyResolutioninRequestHistory()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyResolutioninRequestHistory()` |

### `SDPOD_Req_Sol_046, SDPOD_Req_Sol_050, SDPOD_Req_Sol_051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `TrashRequestWithResolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `TrashRequestWithResolution()` |

### `SDPOD_Req_Sol_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `RestoreRequestWithResolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `RestoreRequestWithResolution()` |

### `SDPOD_Req_Sol_048, SDPOD_Req_Sol_063` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionHeaderforRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionHeaderforRequest()` |

### `SDPOD_Req_Sol_052, SDPOD_Req_Sol_053` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ArchieveRequestwithResolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ArchieveRequestwithResolution()` |

### `SDPOD_Req_Sol_055` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `PrintPreviewRequestWithResolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `PrintPreviewRequestWithResolution()` |

### `SDPOD_Req_Sol_056` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionForDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionForDuplicateRequest()` |

### `SDPOD_Req_Sol_057` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutioninEditDuplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutioninEditDuplicateRequest()` |

### `SDPOD_Req_Sol_058` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `MergeRequestwithSolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `MergeRequestwithSolution()` |

### `SDPOD_Req_Sol_059` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `splitRequestwithSolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `splitRequestwithSolution()` |

### `SDPOD_Req_Sol_060` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionforIncidenttoService()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionforIncidenttoService()` |

### `SDPOD_Req_Sol_061` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionforCancelledRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionforCancelledRequest()` |

### `SDPOD_Req_Sol_062` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ResolutionforRevertCancelRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ResolutionforRevertCancelRequest()` |

### `SDPOD_Req_Sol_064` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ReferredSolutionStatuschange()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ReferredSolutionStatuschange()` |

### `SDPOD_Req_Sol_009, SDPOD_Req_Sol_010, SDPOD_Req_Sol_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `SolutionListBasedTopicFilter()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `SolutionListBasedTopicFilter()` |

### `SDPOD_Req_Sol_080` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `RestoredSolutioninReferredSolution()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `RestoredSolutioninReferredSolution()` |

### `SDPOD_Req_Sol_122, SDPOD_Req_Sol_123, SDPOD_Req_Sol_127` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `ApprovedOnlySolutionList()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `ApprovedOnlySolutionList()` |

### `SDPOD_REQUEST_SDGT_PERF_012` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requesterHeadPickerQuickIncident()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `requesterHeadPickerQuickIncident()` |

### `SDPOD_REQUEST_SDGT_PERF_013` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `nonAssociatedSiteCheckInRequesterHeadPicker()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `nonAssociatedSiteCheckInRequesterHeadPicker()` |

### `SDPOD_COLLECTION_FIELDS_INFO_TC021,SDPOD_REQCART2501_001,Cart Issue Id-75077` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAssetNavigateToAssetDetailsPageViaViewAssetDetailsIcon()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyAssetNavigateToAssetDetailsPageViaViewAssetDetailsIcon()` |

### `SDPOD_COLLECTION_FIELDS_INFO_TC021,SDP-REQ-CRE-0493,Cart Issue Id-73430` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `selectAssetsInFormForRequesterAndVerifyRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `selectAssetsInFormForRequesterAndVerifyRequesterLogin()` |

### `SDP_REQ_CV_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `enableTATExcludeCriteriaWithSystemLog()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `enableTATExcludeCriteriaWithSystemLog()` |

### `SDP_SGT_205` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shareIncidentRequestToOrgRoleUserNotHavingAssociation()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shareServiceRequestToOrgRoleUserNotHavingAssociation()` |

### `SDPOD_FGA_164` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `presenceAllowedAssetInRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `absenceAllowedAssetInRequest()` |

### `DelegationActionValidator` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `delegateApprovalInApprovalLinkPage()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `delegateApprovalInApprovalLinkPage()` |

### `CH1516_BI_WEEK_CART_63125` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestCheckInKanbanView()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `requestCheckInKanbanView()` |

### `SDPOD_SERVICE_CATEGORY_019` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyDisabledIncidentTemplatePresentInNewIncidentDropdownInRequesterLogin()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `verifyEnabledIncidentTemplatePresentInNewIncidentDropdownInRequesterLogin()` |

### `SDPOD_ReqSuitePerf_4.1.1_046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyRequestInlineDetailsViewSectionsInPreviousRequestPopup()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyRequestInlineDetailsViewSectionsInPreviousRequestPopup()` |

### `SDP_AUTO_REQ_CART2402_035` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `duplicateHistoryWithPrefix()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `duplicateHistoryWithPrefix()` |

### `SDPOD_AUTO_REQ_SR_LST_UPDATED_BY_026` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyLastupdatedServiceTemplateFromIncidentTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedServiceTemplateFromIncidentTemp()` |

### `SDPOD_AUTO_REQ_SR_LSTUPDATEDBY_011` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyLastupdatedByRequesterEdit()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyLastupdatedByRequesterEdit()` |

### `SDPOD_TLHCA_106` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyHelpcardPresentnotWhenConvertServiceToIncident()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardPresentnotWhenConvertServiceToIncident()` |

### `SDPOD_TLHCA_104` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `verifyHelpcardPresentWhenConvertServiceToIncident()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `verifyHelpcardPresentWhenConvertServiceToIncident()` |

### `SDPOD_AUTO_REQ_SITE_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/sitebased/RequestSiteBased.java` | `verifySiteFieldIsnotDisplayed()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/sitebased/RequestSiteBased.java` | `createRequestWithNoSite()` |

### `SDPOD_ReqTags_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkTagIsCancelled()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkCancelTagAfterAdding()` |

### `SDPOD_ReqTags_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `cancelTag()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkCancelTagPresentInDropDown()` |

### `SDPOD_ReqTags_068` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `mergeRequestHavingTags()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `mergeRequestHavingTags()` |

### `SDPOD_ReqTags_069` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `mergeRequestandBothRequestHaveNoTags()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `mergeRequestandBothRequestHaveNoTags()` |

### `SDPOD_ReqTags_070` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `mergeRequestandParentRequestHaveNoTags()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `mergeRequestandParentRequestHaveNoTags()` |

### `SDPOD_ReqTags_071` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `mergeRequestAndParentRequestHavingTags()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `mergeRequestAndParentRequestHavingTags()` |

### `SDPOD_ReqTags_072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `splitRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `splitRequest()` |

### `SDPOD_ReqTags_073` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `duplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `duplicateRequest()` |

### `SDPOD_ReqTags_074` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkHistoryduplicateRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `checkHistoryduplicateRequest()` |

### `SDPOD_ReqTags_082` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `disassociateTagInPendingRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `disassociateTagInPendingRequest()` |

### `SDPOD_ReqTags_084` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `associateTagInPendingRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `associateTagInPendingRequest()` |

### `SDPOD_ReqTags_087` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `changeTemp()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `changeTemp()` |

### `SDPOD_ReqTags_092` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `duplicateCancelRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `duplicateCancelRequest()` |

### `SDPOD_ReqTags_177` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `checkIncidentToService()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `checkIncidentToService()` |

### `SDPOD_ReqTags_178` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/request/tags/RequestTags.java` | `createService()` |
| 2 | `com/zoho/automater/selenium/modules/requests/request/tags/ServiceRequestTags.java` | `createService()` |

### `SDPOD_APPROVALS_NEED_MORE_INFO_001` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/requests/requestapprovals/RequestApprovals.java` | `presenceOfNewTabsInIncidentRequest()` |
| 2 | `com/zoho/automater/selenium/modules/requests/requestapprovals/RequestApprovals.java` | `presenceOfNewTabsInServiceRequest()` |

### `SDPOD_AUTO_SOL_CREATE_003` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `createApprovedPublicSolutionGT()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `solutionDraftsValidator()` |

### `SDPOD_AUTO_SOL_CREATE_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `createUnAppPubSolAllUserGroupsRevDateGT()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `createSolutionWithTechGroup()` |

### `SDPOD_AUTO_SOL_132` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deletePublicUnAppSolutionFromListViewLocalActions()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeletePublicUnAppSolutionFromListViewLocalActions()` |

### `SDPOD_AUTO_SOL_133` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deletePrivateUnAppSolutionFromListViewLocalActions()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeletePrivateUnAppSolutionFromListViewLocalActions()` |

### `SDPOD_AUTO_SOL_134` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPrivSolutionFromListViewLocalActions()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPrivSolutionFromListViewLocalActions()` |

### `SDPOD_AUTO_SOL_135` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPubSolutionFromListViewLocalActions()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPubSolutionFromListViewLocalActions()` |

### `SDPOD_AUTO_SOL_LV_136` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deletePublicUnAppSolutionFromListView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeletePublicUnAppSolutionFromListView()` |

### `SDPOD_AUTO_SOL_LV_137` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deletePrivateUnAppSolutionFromListView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeletePrivateUnAppSolutionFromListView()` |

### `SDPOD_AUTO_SOL_LV_138` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPrivSolutionFromListView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPrivSolutionFromListView()` |

### `SDPOD_AUTO_SOL_LV_139` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPubSolutionFromListView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPubSolutionFromListView()` |

### `SDPOD_AUTO_SOL_DV_156` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteUnAppPrivSolutionFromdetailView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteUnAppPrivSolutionFromdetailView()` |

### `SDPOD_AUTO_SOL_DV_157` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteAppPrivSolutionFromdetailView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteAppPrivSolutionFromdetailView()` |

### `SDPOD_AUTO_SOL_DV_159` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `deleteUnAppPublicSolutionFromdetailView()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `trashDeleteUnAppPublicSolutionFromdetailView()` |

### `SDPOD_SOLUTIONS_SG_42,SDPOD_SOLUTIONS_SG_19` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifySharesubTopicWindowFields()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `changeTopicOwner()` |

### `SDPOD_Req_Sol_082, SDPOD_Req_Sol_083, SDPOD_Req_Sol_084, SDPOD_Req_Sol_085, SDPOD_Req_Sol_081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `RejectedSolutioncheckinLinkedSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionFullPermission.java` | `RejectedSolutioncheckinLinkedSolution()` |

### `SDPOD_Req_Sol_086, SDPOD_Req_Sol_087, SDPOD_Req_Sol_088, SDPOD_Req_Sol_081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `SolutionStatuscheckinLinkedSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionFullPermission.java` | `SolutionStatuscheckinLinkedSolution()` |

### `SDPOD_Req_Sol_081` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `RejectedSolutionDetachFromLinkedSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionFullPermission.java` | `RejectedSolutionDetachFromLinkedSolution()` |

### `SDPOD_KB_Article_032` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateTitleNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generateTitleNewSolution()` |

### `SDPOD_KB_Article_033` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generateContentNewSolution()` |

### `SDPOD_KB_Article_034` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generatekeywordsNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generatekeywordsNewSolution()` |

### `SDPOD_KB_Article_024` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `elaborateContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `elaborateContentNewSolution()` |

### `SDPOD_KB_Article_025` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `shortenContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `shortenContentNewSolution()` |

### `SDPOD_KB_Article_023` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `defaultContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `defaultContentNewSolution()` |

### `SDPOD_KB_Article_028` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `howToGuideContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `howToGuideContentNewSolution()` |

### `SDPOD_KB_Article_029` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `fAqContentNewSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `fAqContentNewSolution()` |

### `SDPOD_KB_Article_038` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `isSolutionGeneratedInEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `isSolutionGeneratedInEditSolution()` |

### `SDPOD_KB_Article_040` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateTitleEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `generateTitleEditSolution()` |

### `SDPOD_KB_Article_041` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `generateContentEditSolution()` |

### `SDPOD_KB_Article_042` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generatekeywordsEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `generatekeywordsEditSolution()` |

### `SDPOD_KB_Article_046` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `elaborateContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `elaborateContentEditSolution()` |

### `SDPOD_KB_Article_047` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `shortenContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `shortenContentEditSolution()` |

### `SDPOD_KB_Article_045` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `defaultContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `defaultContentEditSolution()` |

### `SDPOD_KB_Article_050` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `howToGuideContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `howToGuideContentEditSolution()` |

### `SDPOD_KB_Article_051` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `fAqContentEditSolution()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionEditOnly.java` | `fAqContentEditSolution()` |

### `SDPOD_KB_Article_008` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `solutionGeneratorInNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `solutionGeneratorInNewSolutionListview()` |

### `SDPOD_KB_Article_065` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateTitleNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generateTitleNewSolutionListview()` |

### `SDPOD_KB_Article_066` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generateContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generateContentNewSolutionListview()` |

### `SDPOD_KB_Article_067` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `generatekeywordsNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `generatekeywordsNewSolutionListview()` |

### `SDPOD_KB_Article_071` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `elaborateContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `elaborateContentNewSolutionListview()` |

### `SDPOD_KB_Article_072` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `shortenContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `shortenContentNewSolutionListview()` |

### `SDPOD_KB_Article_070` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `defaultContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `defaultContentNewSolutionListview()` |

### `SDPOD_KB_Article_075` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `howToGuideContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `howToGuideContentNewSolutionListview()` |

### `SDPOD_KB_Article_076` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `fAqContentNewSolutionListview()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/roles/SolutionAddOnly.java` | `fAqContentNewSolutionListview()` |

### `SDPOD_SOL_VERSION_CTRL_015` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyInDraftPageOptionsDisplayedLastUpdatedBy()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyUserAbleToApproveDraft()` |

### `SDPOD_SOL_VERSION_CTRL_058` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `searchSolutionVersionUsingTitleFunctionality()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyVersionsDisplayedForTrashSolutions()` |

### `SDPOD_SOL_VERSION_CTRL_069` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyNewDraftVersionNotCreatedWhenContentIsSimilar()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyActiveTagDisplayedInCurrentVersion()` |

### `SDPOD_SOL_VERSION_CTRL_086` — ×2 occurrences

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifySolutionDraftsHistory()` |
| 2 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `verifyEnableVersioningAddedInSystemLogs()` |

---

## Part 2 — Empty Scenario IDs

> 1372 methods have `id = ""` in `@AutomaterScenario`. They get a blank key in ChromaDB and cannot be looked up by ID.

| # | Java File | Method |
|---|-----------|--------|
| 1 | `com/zoho/automater/selenium/modules/activities/activity/Activity.java` | `createNoteMentionsAndAttachmentInNote()` |
| 2 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/BusinessRules.java` | `checkBRFilterBySiteForMSPIssue()` |
| 3 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/BusinessRules.java` | `checkAllSitesListedWhenChooseAllCustomerForMSPIssue()` |
| 4 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/BusinessRules.java` | `checkInactiveCustomersListedOrNot()` |
| 5 | `com/zoho/automater/selenium/modules/admin/automation/businessrules/requests/CustomerIssuesinBusinessRule.java` | `checkSystemLogcontainsRequestId()` |
| 6 | `com/zoho/automater/selenium/modules/admin/automation/cdetection/FreezeWindow.java` | `freezeConflictInChangeWithAnnouncement()` |
| 7 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkModeFieldforClosingRequest()` |
| 8 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkLevelFieldforClosingRequest()` |
| 9 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkGroupFieldforClosingRequest()` |
| 10 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkTechnicianFieldforClosingRequest()` |
| 11 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkCategoryFieldforClosingRequest()` |
| 12 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkSubCategoryFieldforClosingRequest()` |
| 13 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkItemFieldforClosingRequest()` |
| 14 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkPriorityFieldforClosingRequest()` |
| 15 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasDescriptionforClosingRequest()` |
| 16 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasResolutionforClosingRequest()` |
| 17 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasWorklogforClosingRequest()` |
| 18 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasWorklogforClosingRequestUsingLv()` |
| 19 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasWorklogforClosingRequestUsingSpotEdit()` |
| 20 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasUrgencyforClosingRequest()` |
| 21 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasImpactforClosingRequest()` |
| 22 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasRequestTypeforClosingRequest()` |
| 23 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasAssociatedTaskforClosingRequest()` |
| 24 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasAllChildRequestsShouldbeClosedforClosingRequest()` |
| 25 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `checkFieldasAssociatedChecklistsShouldbeCompletedforClosingRequest()` |
| 26 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasModeandCloseRequestusingBulkEdit()` |
| 27 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasLevelandCloseRequestusingBulkEdit()` |
| 28 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasGroupandCloseRequestusingBulkEdit()` |
| 29 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasTechnicianandCloseRequestusingBulkEdit()` |
| 30 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasCategoryDetailsandCloseRequestusingBulkEdit()` |
| 31 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasPriorityandCloseRequestusingBulkEdit()` |
| 32 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasUrgencyandCloseRequestusingBulkEdit()` |
| 33 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasImpactandCloseRequestusingBulkEdit()` |
| 34 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasRequestTypeandCloseRequestusingBulkEdit()` |
| 35 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasAssociatedTasksShouldbeClosedandCloseRequestusingListview()` |
| 36 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasChildRequestShouldbeClosedandCloseRequestinLV()` |
| 37 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectFieldasAssociatedChecklistsShouldbeClosedandCloseRequestinLV()` |
| 38 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `confirmUserAcknowledgmentToPromptaMessage()` |
| 39 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `SelectAllUDFFieldinClosingRulesandCloseRequestinDV()` |
| 40 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `selectAllUDFandcloseRequestusingEditTabinDv()` |
| 41 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `selectAllUDFandcloseRequestusingEditIconinLv()` |
| 42 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `selectAllUDFandcloseRequestusingSpotEdit()` |
| 43 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `createUDFfieldwithDefaultValueandcloseRequestusingSpotEdit()` |
| 44 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `createUDFfieldwithDefaultValueandcloseRequestusingLv()` |
| 45 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `createUDFfieldwithDefaultValueandcloseRequestusingDv()` |
| 46 | `com/zoho/automater/selenium/modules/admin/automation/closurerules/RequestClosureRules.java` | `selectAllUDFandcloseRequestusingBulkEdit()` |
| 47 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `createApprovalChangesInCustomActions()` |
| 48 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `editChangeApprovalsUsingRowActionsInCustomAcions()` |
| 49 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `deleteChangeApprovalsUsingRowActionsInCustomAcions()` |
| 50 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `disableAndEnableChangeApprovalsUsingToggleSlider()` |
| 51 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `deleteChangeApprovalsFromActionsDropdown()` |
| 52 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `disableAndEnableChangeApprovalsFromActionsDropdown()` |
| 53 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `approvalSettingsInChangeApprovalsFromGlobalConfiguration()` |
| 54 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ChangeApprovals.java` | `approvalNotificationInChangeApprovalsFromGlobalConfiguration()` |
| 55 | `com/zoho/automater/selenium/modules/admin/automation/customactions/approvals/ReleaseApprovals.java` | `createApprovalReleasesInCustomActions()` |
| 56 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ChangeNotification.java` | `createChangeNotificationWithChangeRolesViaUI()` |
| 57 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ChangeNotification.java` | `createChangeNotificationWithChangeUsersViaUI()` |
| 58 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ChangeNotification.java` | `verifyChangeRolesDropdownValuesInNotifyField()` |
| 59 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ChangeNotification.java` | `verifyChangeUsersDropdownValuesInNotifyField()` |
| 60 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ChangeNotification.java` | `createChangeNotificationInCustomActions()` |
| 61 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `createProblemNotificationWithNotifiyToTechnicianViaUI()` |
| 62 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `editProblemNotificationWithNotifiyToTechnicianViaUI()` |
| 63 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `deleteProblemNotificationViaSettings()` |
| 64 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `disableandEnableProblemNotificationUsingRowActions()` |
| 65 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `disableAndEnableProblemNotificationUsingToggleSlider()` |
| 66 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/ProblemNotification.java` | `disableAndEnableProblemNotificationViaActionsButton()` |
| 67 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `createRequestNotificationWithNotifiyToTechnicianViaUI()` |
| 68 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `editRequestNotificationWithNotifiyToTechnicianViaUI()` |
| 69 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `deleteRequestNotificationViaSettings()` |
| 70 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `disableandEnableRequestNotificationUsingRowActions()` |
| 71 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `disableAndEnableRequestNotificationUsingToggleSlider()` |
| 72 | `com/zoho/automater/selenium/modules/admin/automation/customactions/notification/RequestNotification.java` | `disableAndEnableRequestNotificationViaActionsButton()` |
| 73 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `createAndVerifyTaskInCustomActions()` |
| 74 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `editTaskUsingRowActions()` |
| 75 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `deleteTaskUsingRowActions()` |
| 76 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `disableAndEnableTaskUsingRowActions()` |
| 77 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `disableAndEnableTaskUsingToggleSlider()` |
| 78 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `deleteTaskFromActionsDropdown()` |
| 79 | `com/zoho/automater/selenium/modules/admin/automation/customactions/task/ProblemTask.java` | `disableAndEnableTaskFromActionsDropdown()` |
| 80 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `createAndVerifyTaskAndTimerInCustomActions()` |
| 81 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `editTimerUsingRowActionsInCustomAcions()` |
| 82 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `deleteTimerUsingRowActionsInCustomAcions()` |
| 83 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `disableAndEnableTimerUsingRowActions()` |
| 84 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `disableAndEnableTimerUsingToggleSlider()` |
| 85 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `verifyTaskNotPresentInTimerWhenTaskIsDisabled()` |
| 86 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `deleteTimerFromActionsDropdown()` |
| 87 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `disableAndEnableTimerFromActionsDropdown()` |
| 88 | `com/zoho/automater/selenium/modules/admin/automation/customactions/timer/ProblemTimer.java` | `expandTimerFromListviewAndVerify()` |
| 89 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/NotificationRules.java` | `notifyRequesterWhenAPublicNoteIsAdded()` |
| 90 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `notifyUserWhenAssignedAnyChangeRolesForEmailNotifications()` |
| 91 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/change/ChangeNotification.java` | `editNotifyChangeOwnerWhenNewProblemDetachFromChangeForPN()` |
| 92 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `notifyRequesterWhenPublicNoteIsAdded()` |
| 93 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 94 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `incidentandServicerequestExportallData()` |
| 95 | `com/zoho/automater/selenium/modules/admin/automation/notificationrules/request/RequestNotification.java` | `incidentandServicerequestExportSelectedData()` |
| 96 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForKeyboard()` |
| 97 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForPrinter()` |
| 98 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForAccesspoint()` |
| 99 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForProjector()` |
| 100 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForRouter()` |
| 101 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForScanner()` |
| 102 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForServer()` |
| 103 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForSmartPhone()` |
| 104 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForSwitches()` |
| 105 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForTablet()` |
| 106 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForVirtualHost()` |
| 107 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForVirtualMachine()` |
| 108 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `checkAllAssetTriggerForWorkstation()` |
| 109 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `createTriggerInUIForAsset()` |
| 110 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `editTriggerInUIForAsset()` |
| 111 | `com/zoho/automater/selenium/modules/admin/automation/triggers/AssetTrigger.java` | `createTriggerInUIWithCFForAsset()` |
| 112 | `com/zoho/automater/selenium/modules/admin/automation/triggers/CMDBTrigger.java` | `createTriggerInUIForCMDB()` |
| 113 | `com/zoho/automater/selenium/modules/admin/automation/triggers/CMDBTrigger.java` | `editTriggerInUIForCMDB()` |
| 114 | `com/zoho/automater/selenium/modules/admin/automation/triggers/CMDBTrigger.java` | `createTriggerInUIWithCFForCMDB()` |
| 115 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalIsAdded()` |
| 116 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `deleteChangeTriggerUsingRowActions()` |
| 117 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `editChangeTriggerUsingRowActions()` |
| 118 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `disableAndEnableChangeTriggerUsingRowActions()` |
| 119 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `disableAndEnableChangeTriggerUsingToggleSlider()` |
| 120 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `deleteChangeTriggerFromActionsDropdown()` |
| 121 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalIsExecutedAsApprovedAndVerifyInHistory()` |
| 122 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalIsExecutedAsRejectedAndVerifyInHistory()` |
| 123 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyAutomaticApprovaIfRequesterAndApproverAreSameAndVerifyInHistory()` |
| 124 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyMandateCommentsForAllApprovalsAndVerifyInHistory()` |
| 125 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `notifyOtherApproversActOnApprovalsAndVerifyInHistory()` |
| 126 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyAutoApproveIfSameApproverHasPreviousLevelAndVerifyInHistory()` |
| 127 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalFRAIsExecutedAndVerifyInHistory()` |
| 128 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalM2AIsExecutedAndVerifyInHistory()` |
| 129 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalLevelsIsExecutedAndVerifyInHistory()` |
| 130 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalLevelE2AIsExecutedAndVerifyInHistory()` |
| 131 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalLevelA2AWithTasksIsExecutedAndVerifyInHistory()` |
| 132 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalLevelA2AWithTasksIsExecutedAndVerifyInHistoryWhileEdited()` |
| 133 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `verifyChangeTriggerWithApprovalLevelE2AWithNotesIsExecutedAndVerifyInHistory()` |
| 134 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `checkTechnicicanListOrNotUnderCriteriaValueinTriggerForMSPIssue()` |
| 135 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `checkOtherCustomerTechniciansListOrNotInTaskTechnicianFieldForMSPIssue()` |
| 136 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `additionFieldValueListedOrNotInCriteriaBUilderForMSPIssue()` |
| 137 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createTriggerInUIForChange()` |
| 138 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `editTriggerInUIForChange()` |
| 139 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ChangeTrigger.java` | `createTriggerInUIWithCFForChange()` |
| 140 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `checkContractTriggerInCreate()` |
| 141 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `checkContractTriggerInEdit()` |
| 142 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `checkContractTriggerInDelete()` |
| 143 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `createTriggerInUIForContract()` |
| 144 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `editTriggerInUIForContract()` |
| 145 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ContractTrigger.java` | `createTriggerInUIWithCFForContract()` |
| 146 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkRequestHistoryWhenTimerisDeleted()` |
| 147 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkEnableZiaAfterRefreshForMSPIssue()` |
| 148 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkUnderSiteDefaultValueIsPresentForReportModuleForMSPIssue()` |
| 149 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkSCCMIntegrationPageIsWorkingForMSPIssue()` |
| 150 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkDepartmentShownUnderSiteAndCustomer()` |
| 151 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `globalSearchElemendHideNewRequestIconOrNorForMSPIssue()` |
| 152 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkDepartmentListedUnderCustomer()` |
| 153 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkMSPCustomerIconShownOrNot()` |
| 154 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkCustomerChooserDropDrownShownOrNot()` |
| 155 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `newProbeSiteFiedInputBoxShownOrNot()` |
| 156 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkSandBoxIsEnableOrDisable()` |
| 157 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `checkTaskButtonIsShownForInactiveCustomerInQuickAction()` |
| 158 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createTriggerInUIForRequest()` |
| 159 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `editTriggerInUIForRequest()` |
| 160 | `com/zoho/automater/selenium/modules/admin/automation/triggers/IncidentRequestTrigger.java` | `createTriggerInUIWithCF()` |
| 161 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `verifyProblemTriggerAdded()` |
| 162 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `deleteTriggerUsingRowActions()` |
| 163 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `editTriggerUsingRowActions()` |
| 164 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `disableAndEnableTriggerUsingRowActions()` |
| 165 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `disableAndEnableTriggerUsingToggleSlider()` |
| 166 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `deleteTriggerFromActionsDropdown()` |
| 167 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `verifyTimerNotPresentInTriggerWhenTimerIsDisabled()` |
| 168 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `checkProblemTriggerInCreate()` |
| 169 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `checkProblemTriggerInEdit()` |
| 170 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskInCreate()` |
| 171 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskInEdit()` |
| 172 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskInDelete()` |
| 173 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsAllWorklogInCreate()` |
| 174 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsAllWorklogInEdit()` |
| 175 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsAllWorklogInDelete()` |
| 176 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsWorklogInCreate()` |
| 177 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsWorklogInEdit()` |
| 178 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsWorklogInDelete()` |
| 179 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskWorklogInCreate()` |
| 180 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskWorklogInEdit()` |
| 181 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsTaskWorklogInDelete()` |
| 182 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsNotesInCreate()` |
| 183 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsNotesInEdit()` |
| 184 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createProblemTriggerWithSubentityIsNotesInDelete()` |
| 185 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createTriggerInUIForProblem()` |
| 186 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `editTriggerInUIForProblem()` |
| 187 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java` | `createTriggerInUIWithCFForProblem()` |
| 188 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `checkCustomerFieldIsDisplayOrNot()` |
| 189 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `checkProblemTriggerInCreate()` |
| 190 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `checkProblemTriggerInEdit()` |
| 191 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `checkProblemTriggerInDelete()` |
| 192 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskInCreate()` |
| 193 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskInEdit()` |
| 194 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskInDelete()` |
| 195 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskInCreate()` |
| 196 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskInEdit()` |
| 197 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskInDelete()` |
| 198 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskInCreate()` |
| 199 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskInEdit()` |
| 200 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskInDelete()` |
| 201 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneInCreate()` |
| 202 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneInEdit()` |
| 203 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneInDelete()` |
| 204 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskWorklogInCreate()` |
| 205 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskWorklogInEdit()` |
| 206 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskWorklogInDelete()` |
| 207 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskWorklogInCreate()` |
| 208 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskWorklogInEdit()` |
| 209 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskWorklogInDelete()` |
| 210 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskWorklogInCreate()` |
| 211 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskWorklogInEdit()` |
| 212 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneTaskWorklogInDelete()` |
| 213 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMembersInCreate()` |
| 214 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMembersInEdit()` |
| 215 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMembersInDelete()` |
| 216 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectCommentsInCreate()` |
| 217 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectCommentsInEdit()` |
| 218 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectCommentsInDelete()` |
| 219 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneCommentsInCreate()` |
| 220 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneCommentsInEdit()` |
| 221 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsMilestoneCommentsInDelete()` |
| 222 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskCommentsInCreate()` |
| 223 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskCommentsInEdit()` |
| 224 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsProjectTaskCommentsInDelete()` |
| 225 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsmilestoneTaskCommentsInCreate()` |
| 226 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsmilestoneTaskCommentsInEdit()` |
| 227 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsmilestoneTaskCommentsInDelete()` |
| 228 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskCommentsInCreate()` |
| 229 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskCommentsInEdit()` |
| 230 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createProjectTriggerWithSubentityIsAllTaskCommentsInDelete()` |
| 231 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createTriggerInUIForProject()` |
| 232 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `editTriggerInUIForProject()` |
| 233 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ProjectTrigger.java` | `createTriggerInUIWithCFForProject()` |
| 234 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerInCreate()` |
| 235 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerInEdit()` |
| 236 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerInDelete()` |
| 237 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalLevelInCreate()` |
| 238 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalLevelInEdit()` |
| 239 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalLevelInDelete()` |
| 240 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalInCreate()` |
| 241 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalInEdit()` |
| 242 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityApprovalInDelete()` |
| 243 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityInvoiceInCreate()` |
| 244 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityInvoiceInEdit()` |
| 245 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityInvoiceInDelete()` |
| 246 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityPaymentInCreate()` |
| 247 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityPaymentInEdit()` |
| 248 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `checkPurchaseTriggerSubentityPaymentInDelete()` |
| 249 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `createTriggerInUIForPurchase()` |
| 250 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `editTriggerInUIForPurchase()` |
| 251 | `com/zoho/automater/selenium/modules/admin/automation/triggers/PurchaseTrigger.java` | `createTriggerInUIWithCFForPO()` |
| 252 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createTriggerInUIForRelease()` |
| 253 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `editTriggerInUIForRelease()` |
| 254 | `com/zoho/automater/selenium/modules/admin/automation/triggers/ReleaseTrigger.java` | `createTriggerInUIWithCFForRelease()` |
| 255 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerInCreate()` |
| 256 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerInEdit()` |
| 257 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerInDelete()` |
| 258 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerSubentityCommentsInCreate()` |
| 259 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerSubentityCommentsInEdit()` |
| 260 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `checkSolutionTriggerSubentityCommentsInDelete()` |
| 261 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `createTriggerInUIForSolution()` |
| 262 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `editTriggerInUIForSolution()` |
| 263 | `com/zoho/automater/selenium/modules/admin/automation/triggers/SolutionTrigger.java` | `createTriggerInUIWithCFForSolution()` |
| 264 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createPrinterAssetWorkflow()` |
| 265 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createAccessPointsAssetWorkflow()` |
| 266 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createProjectorsAssetWorkflow()` |
| 267 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createRoutersAssetWorkflow()` |
| 268 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createScannersAssetWorkflow()` |
| 269 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createServersAssetWorkflow()` |
| 270 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createSmartphonesAssetWorkflow()` |
| 271 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createSwitchesAssetWorkflow()` |
| 272 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createTabletsAssetWorkflow()` |
| 273 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createVirtualHostsAssetWorkflow()` |
| 274 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createVirtualMachinesAssetWorkflow()` |
| 275 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createWorkstationsAssetWorkflow()` |
| 276 | `com/zoho/automater/selenium/modules/admin/automation/workflows/AssetWorkflow.java` | `createWorkflowWithCFAndWebhookForKBAsset()` |
| 277 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `jusforTest()` |
| 278 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `additionFieldValueListedOrNotForMSPIssue()` |
| 279 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `checkTechnicianListedOrNotInIfAndWaitForNode()` |
| 280 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `checkNewLifeCycleButtonShownForInactiveCustome()` |
| 281 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `inactiveCustomerSiteIsShownOrNotInChangeFieldUpdate()` |
| 282 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `createWorkflowWithSwitchNodeGroupAsField()` |
| 283 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ChangeWorkflow.java` | `createWorkflowWithCFAndWebhookForChange()` |
| 284 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createWorkflowOfIncidentRequest()` |
| 285 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `verifyWorkflowRedoUndoAndReset()` |
| 286 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `checkInvalidWorkflowForIncidentRequest()` |
| 287 | `com/zoho/automater/selenium/modules/admin/automation/workflows/IncidentRequestWorkflow.java` | `createWorkflowWithCFAndWebhookForIR()` |
| 288 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createProblemWorkflowInUI()` |
| 289 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `verifyWorkflowRedoUndoAndReset()` |
| 290 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `checkInvalidWorkflowForProblem()` |
| 291 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsIFForProblem()` |
| 292 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsWaitForForProblem()` |
| 293 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsSwitchForProblem()` |
| 294 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsNotificationForProblem()` |
| 295 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsFieldUpdateForProblem()` |
| 296 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsTaskForProblem()` |
| 297 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsForkForProblem()` |
| 298 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createSingleNodeIsJoinForProblem()` |
| 299 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `problemEditWorkflow()` |
| 300 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ProblemWorkflow.java` | `createWorkflowWithCFAndWebhookForProblem()` |
| 301 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ReleaseWorkflow.java` | `createWorkflowWithCFAndWebhookForRelease()` |
| 302 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createServiceRequestWorkflow()` |
| 303 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `verifyWorkflowRedoUndoAndReset()` |
| 304 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `checkInvalidWorkflowForIncidentRequest()` |
| 305 | `com/zoho/automater/selenium/modules/admin/automation/workflows/ServiceRequestWorkflow.java` | `createWorkflowWithCFAndWebhookForSR()` |
| 306 | `com/zoho/automater/selenium/modules/admin/customization/additionalfields/RequestUDF.java` | `addAssetEntityWithNameAssetDeptInRequestLookup()` |
| 307 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureApInSelectedProduct()` |
| 308 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configurePrintersInSelectedProduct()` |
| 309 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureRouterInSelectedProduct()` |
| 310 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureServerInSelectedProduct()` |
| 311 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureSpInSelectedProduct()` |
| 312 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureSwitchInSelectedProduct()` |
| 313 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureTabletInSelectedProduct()` |
| 314 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureWorkstationInSelectedProduct()` |
| 315 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `configureKbInSelectedProduct()` |
| 316 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `assetAcknowledgementinAp()` |
| 317 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `assetAcknowledgementinSp()` |
| 318 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `assetAcknowledgementinKb()` |
| 319 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkInStoreAssetisPresentinAcknowledgement()` |
| 320 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinApAsset()` |
| 321 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinPrinterAsset()` |
| 322 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinCiscoRouterAsset()` |
| 323 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinServerAsset()` |
| 324 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinSpAsset()` |
| 325 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinCiscoSwitchAsset()` |
| 326 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinTabletAsset()` |
| 327 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinWorkstationAsset()` |
| 328 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinProjectorAsset()` |
| 329 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgmentTabinScannerAsset()` |
| 330 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgeisnotPresentForApAsset()` |
| 331 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAssignmentHistorySubtabinApDv()` |
| 332 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/assetacknowledgement/AssetAcknowledgement.java` | `checkAcknowledgeisPresentinApwithCertainCondition()` |
| 333 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkConsumableProductTypeButtons()` |
| 334 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `createConsumableProductTypeinUI()` |
| 335 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `editSoftwareProductType()` |
| 336 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkSiblingFunctionalityofComputer()` |
| 337 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkChildProductisVisibleinParentProductType()` |
| 338 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `createSectionNameinTemplate()` |
| 339 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `editSectionNameinTemplate()` |
| 340 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkAssetConfigRole()` |
| 341 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkSDAssetManagerRole()` |
| 342 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkSDRemoteControl()` |
| 343 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkandCreatePrinterusingCustomRoles()` |
| 344 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinAccessPoint()` |
| 345 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinPrinter()` |
| 346 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinCiscoRouter()` |
| 347 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinServer()` |
| 348 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinWorkstation()` |
| 349 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinSmartphone()` |
| 350 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinCiscoSwitch()` |
| 351 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinTablet()` |
| 352 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinProjector()` |
| 353 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinScanner()` |
| 354 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinKeyboard()` |
| 355 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinVirtualHost()` |
| 356 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinVirtualMachine()` |
| 357 | `com/zoho/automater/selenium/modules/admin/customization/assetmanagement/producttype/ProductType.java` | `checkUDFinComputer()` |
| 358 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `navigateToSyncRules()` |
| 359 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `checkHelpSyncRules()` |
| 360 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `disableFromEditSyncRules()` |
| 361 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `enableFromEditSyncRules()` |
| 362 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `editSyncRuleAfterExecution()` |
| 363 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationWithoutAction()` |
| 364 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationWithAction1()` |
| 365 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationWithAction2()` |
| 366 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationWithAction3()` |
| 367 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `validationWithAction4()` |
| 368 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `assetSyncRuleCreationInUI()` |
| 369 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `assetSyncRuleCreationInUIWithoutCondition()` |
| 370 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `executeSyncRuleByCreatingAssetInUI()` |
| 371 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `assetSyncRuleCreationInUIWithUDF()` |
| 372 | `com/zoho/automater/selenium/modules/admin/customization/cmdbmanagement/syncrules/SyncRules.java` | `userSyncRuleCreationInUIWithUDF()` |
| 373 | `com/zoho/automater/selenium/modules/admin/customization/helpdesk/category/Category.java` | `checkAllCategoryValueListOutForMSPIssue()` |
| 374 | `com/zoho/automater/selenium/modules/admin/dataAdministration/exportdata/ExportData.java` | `exportGLCode()` |
| 375 | `com/zoho/automater/selenium/modules/admin/dataAdministration/exportdata/ExportData.java` | `exportCostCenter()` |
| 376 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForRequests()` |
| 377 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForChange()` |
| 378 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForRelease()` |
| 379 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForProblems()` |
| 380 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForProjects()` |
| 381 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForSolutions()` |
| 382 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForPurchases()` |
| 383 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForContracts()` |
| 384 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForCMDB()` |
| 385 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkImportDataForAsset()` |
| 386 | `com/zoho/automater/selenium/modules/admin/dataAdministration/importdata/ImportData.java` | `checkMandatoryAlert()` |
| 387 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `siteInSystemLog()` |
| 388 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `operationalHoursInSystemLog()` |
| 389 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `holidayGroupsInSystemLog()` |
| 390 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `departmentInSystemLog()` |
| 391 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `currencyInSystemLog()` |
| 392 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `userGroupInSystemLog()` |
| 393 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `fgaInSystemLog()` |
| 394 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `levelInSystemLog()` |
| 395 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `categoryInSystemLog()` |
| 396 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `statusInSystemLog()` |
| 397 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `modeInSystemLog()` |
| 398 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `impactInSystemLog()` |
| 399 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `urgencyInSystemLog()` |
| 400 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `priorityInSystemLog()` |
| 401 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `requestTypesInSystemLog()` |
| 402 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `taskTypesInSystemLog()` |
| 403 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `worklogTypesInSystemLog()` |
| 404 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `requestClosureCodeInSystemLog()` |
| 405 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `problemClosureCodeInSystemLog()` |
| 406 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `downtimeTypesInSystemLog()` |
| 407 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `changeTypesInSystemLog()` |
| 408 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `cabsInSystemLog()` |
| 409 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `changeRiskInSystemLog()` |
| 410 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `reasonForChangeInSystemLog()` |
| 411 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `changeClosureCodeInSystemLog()` |
| 412 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `changeStageStatusInSystemLog()` |
| 413 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `changeRoleInSystemLog()` |
| 414 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `projectTypeInSystemLog()` |
| 415 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `projectStatusInSystemLog()` |
| 416 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `releaseClosureCodeInSystemLog()` |
| 417 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `releaseStageInSystemLog()` |
| 418 | `com/zoho/automater/selenium/modules/admin/dataAdministration/systemlog/SystemLog.java` | `productTypesInSystemLog()` |
| 419 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `mandatoryCheckAndCreateForWorkflow()` |
| 420 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `editDeleteEnableDIsableForWorkflow()` |
| 421 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `bulkDeleteEnableDIsableForWorkflow()` |
| 422 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForWorkflow()` |
| 423 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `mandatoryCheckAndCreateForWFPreActions()` |
| 424 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `editDeleteEnableDIsableForWFPreActions()` |
| 425 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `bulkDeleteEnableDIsableForWFPreActions()` |
| 426 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForWFPreActions()` |
| 427 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `mandatoryCheckAndCreateForTrLCAndWF()` |
| 428 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `editDeleteEnableDIsableForTrLCAndWF()` |
| 429 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `bulkDeleteEnableDIsableForTrLCAndWF()` |
| 430 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrLCAndWF()` |
| 431 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 432 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `editDeleteEnableDIsableForTrCustomMenu()` |
| 433 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 434 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/AssetCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 435 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `mandatoryCheckAndCreateForTrigger()` |
| 436 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `editDeleteEnableDIsableForTrigger()` |
| 437 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `bulkDeleteEnableDIsableForTrigger()` |
| 438 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrigger()` |
| 439 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 440 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 441 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 442 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/CMDBCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 443 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `mandatoryCheckAndCreateForBRAndTimerWF()` |
| 444 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `editDeleteEnableDIsableForBRAndTimerWF()` |
| 445 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `bulkDeleteEnableDIsableForBRAndTimerWF()` |
| 446 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForBRAndTimerWF()` |
| 447 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `mandatoryCheckAndCreateForBRAndWF()` |
| 448 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `editDeleteEnableDIsableForBRAndWF()` |
| 449 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `bulkDeleteEnableDIsableForBRAndWF()` |
| 450 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForBRAndWF()` |
| 451 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `mandatoryCheckAndCreateForTRTimerWF()` |
| 452 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `editDeleteEnableDIsableForTRTimerWF()` |
| 453 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `bulkDeleteEnableDIsableForTRTimerWF()` |
| 454 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTRTimerWF()` |
| 455 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 456 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 457 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 458 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ChangeCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 459 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `mandatoryCheckAndCreateForTrigger()` |
| 460 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `editDeleteEnableDIsableForTrigger()` |
| 461 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `bulkDeleteEnableDIsableForTrigger()` |
| 462 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrigger()` |
| 463 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 464 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 465 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 466 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ContractCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 467 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `mandatoryCheckAndCreateForBRAndTimer()` |
| 468 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `editDeleteEnableDIsableForBRAndTimer()` |
| 469 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `bulkDeleteEnableDIsableForBRAndTimer()` |
| 470 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForBRAndTimer()` |
| 471 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `mandatoryCheckAndCreateForWFPreRuleActions()` |
| 472 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `editDeleteEnableDIsableForWFPreRuleActions()` |
| 473 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `bulkDeleteEnableDIsableForWFPreRuleActions()` |
| 474 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForWFPreRuleActions()` |
| 475 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `mandatoryCheckAndCreateForAbortTimerAndWF()` |
| 476 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `editDeleteEnableDIsableForAbortTimerAndWF()` |
| 477 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `bulkDeleteEnableDIsableForAbortTimerAndWF()` |
| 478 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForAbortTimerAndWF()` |
| 479 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 480 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 481 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 482 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProblemCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 483 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `mandatoryCheckAndCreateForTrigger()` |
| 484 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `editDeleteEnableDIsableForTrigger()` |
| 485 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `bulkDeleteEnableDIsableForTrigger()` |
| 486 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrigger()` |
| 487 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 488 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 489 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 490 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ProjectCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 491 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `mandatoryCheckAndCreateForTrigger()` |
| 492 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `editDeleteEnableDIsableForTrigger()` |
| 493 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `bulkDeleteEnableDIsableForTrigger()` |
| 494 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrigger()` |
| 495 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 496 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 497 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 498 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/PurchaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 499 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `mandatoryCheckAndCreateForTRAndWF()` |
| 500 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `editDeleteEnableDIsableForTRAndWF()` |
| 501 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `bulkDeleteEnableDIsableForTRAndWF()` |
| 502 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTRAndWF()` |
| 503 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `mandatoryCheckAndCreateForWorkflow()` |
| 504 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `editDeleteEnableDIsableForWorkflow()` |
| 505 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `bulkDeleteEnableDIsableForWorkflow()` |
| 506 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForWorkflow()` |
| 507 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `mandatoryCheckAndCreateForWFAndTimer()` |
| 508 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `editDeleteEnableDIsableForWFAndTimer()` |
| 509 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `bulkDeleteEnableDIsableForWFAndTimer()` |
| 510 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForWFAndTimer()` |
| 511 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 512 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 513 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 514 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/ReleaseCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 515 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `mandatoryCheckAndCreateForBRAndTimer()` |
| 516 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `editDeleteEnableDIsableForBRAndTimer()` |
| 517 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `bulkDeleteEnableDIsableForBRAndTimer()` |
| 518 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForBRAndTimer()` |
| 519 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `mandatoryCheckAndCreateForBRAndWF()` |
| 520 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `editDeleteEnableDIsableForBRAndWF()` |
| 521 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `bulkDeleteEnableDIsableForBRAndWF()` |
| 522 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForBRAndWF()` |
| 523 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `mandatoryCheckAndCreateForTRAndLCAndTimer()` |
| 524 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `editDeleteEnableDIsableForTRAndLCAndTimer()` |
| 525 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `bulkDeleteEnableDIsableForTRAndLCAndTimer()` |
| 526 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTRAndLCAndTimer()` |
| 527 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `mandatoryCheckAndCreateForCustomMenu()` |
| 528 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `editDeleteEnableDIsableForCustomMenu()` |
| 529 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `bulkDeleteEnableDIsableForCustomMenu()` |
| 530 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/RequestCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForCustomMenu()` |
| 531 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/SolutionCustomFunction.java` | `mandatoryCheckAndCreateForTrigger()` |
| 532 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/SolutionCustomFunction.java` | `editDeleteEnableDIsableForTrigger()` |
| 533 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/SolutionCustomFunction.java` | `bulkDeleteEnableDIsableForTrigger()` |
| 534 | `com/zoho/automater/selenium/modules/admin/developerspace/customfunction/SolutionCustomFunction.java` | `verifyCancelSaveAndExcuteScriptButtonForTrigger()` |
| 535 | `com/zoho/automater/selenium/modules/admin/developerspace/custommenu/ProblemCustomMenu.java` | `createProblemCustomMenuAloneViaUI()` |
| 536 | `com/zoho/automater/selenium/modules/admin/developerspace/custommenu/ProblemCustomMenu.java` | `createProblemCustomMenuWithMenuItem()` |
| 537 | `com/zoho/automater/selenium/modules/admin/developerspace/custommenu/ProblemCustomMenu.java` | `verifyCustomMenuExecutedInProblem()` |
| 538 | `com/zoho/automater/selenium/modules/admin/generalsettings/advancedportalsettings/AdvancedPortalSettings.java` | `verifyOpenStatusWhenRequesterReplyToClosedRequestInRequesterLogin()` |
| 539 | `com/zoho/automater/selenium/modules/admin/generalsettings/advancedportalsettings/AdvancedPortalSettings.java` | `verifyOpenStatusWhenRequesterReplyToClosedRequestForRepliedWithIn1DaysInRequesterLogin()` |
| 540 | `com/zoho/automater/selenium/modules/admin/generalsettings/advancedportalsettings/AdvancedPortalSettings.java` | `verifyOpenStatusWhenRequesterReplyToClosedRequestForConversationInRequesterLogin()` |
| 541 | `com/zoho/automater/selenium/modules/admin/generalsettings/advancedportalsettings/AdvancedPortalSettings.java` | `verifyTemplateImageInQuickIncidentViaRequestPane()` |
| 542 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `selectSolutionCheckboxinRequeterPortalSettings()` |
| 543 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `unselectSolutionCheckboxinRequeterPortalSettings()` |
| 544 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `selectRequestTemplateCheckboxinRequeterPortalSettings()` |
| 545 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `unselectRequestTemplateCheckboxinRequeterPortalSettings()` |
| 546 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `selectAnnouncementsCheckboxinRequeterPortalSettings()` |
| 547 | `com/zoho/automater/selenium/modules/admin/generalsettings/requesterportal/requesterportalsettings/RequesterPortalSettings.java` | `unselectAnnouncementsCheckboxinRequeterPortalSettings()` |
| 548 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `verifyAllSitesFieldPresentInDepartmentUsersPopup()` |
| 549 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `editDepartmentViaSettingsIcon()` |
| 550 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/department/Department.java` | `deleteDepartmentViaSettingsIcon()` |
| 551 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `addHolidaysets()` |
| 552 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `editHolidaySet()` |
| 553 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `deleteHolidaySet()` |
| 554 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `addHolidayInHolidaySet()` |
| 555 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `editHolidayInHolidaySet()` |
| 556 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/holidaysets/HolidaySet.java` | `deleteHolidayInHolidaySet()` |
| 557 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `addOperationalHours()` |
| 558 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifySiteAndGroupInOHDetailsInListview()` |
| 559 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyValidationMessageForSiteAndGroupInOHPopup()` |
| 560 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `editOH()` |
| 561 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `deleteOHViaSettingsIcon()` |
| 562 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `associateSiteAndGroupViaSettingsIcon()` |
| 563 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyCreatedOHPresentInParticularSiteFilter()` |
| 564 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyCreatedOHPresentInParticularGroupFilter()` |
| 565 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `deleteOHFromListviewBtn()` |
| 566 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `addSpecialOperationalHours()` |
| 567 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyValidationMessageForAssociateOHInSpecialOperationalHourPopup()` |
| 568 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `editSpecialOperationalHours()` |
| 569 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `deleteSOHViaSettingsIcon()` |
| 570 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `deleteSOHFromListviewBtn()` |
| 571 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerIsExecutedWhenCreatedForOH()` |
| 572 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerIsExecutedWhenRequestEditedForOH()` |
| 573 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerIsExecutedForWorklogByOH()` |
| 574 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRExecutedEvenBreakHours()` |
| 575 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRShouldExecutedEvenBreakHours()` |
| 576 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRIsExecutedWhenCreatedForOH()` |
| 577 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRIsExecutedWhenEditedForOH()` |
| 578 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRIsNotExecutedWhenEditedForOOH()` |
| 579 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerIsExecutedWhenCreatedFORSOH()` |
| 580 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerIsExecutedWhenEditedFORSOH()` |
| 581 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRShouldNotExecutedWhenCreatedForSOHOOH()` |
| 582 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyBRShouldNotExecutedWhenEditedForSOHOOH()` |
| 583 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerShouldNotExecutedWhenTodayIsHoliday()` |
| 584 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerExecutedWhenOHExceptionIsNonWorkingDay()` |
| 585 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyTriggerExecutedWhenSOHExceptionIsNonWorkingDay()` |
| 586 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifySLAIsExecutedByOHandVerifyRHSViolatedIcon()` |
| 587 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifySLAIsExecutedWithFieldUpdate()` |
| 588 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifySLAIsExecutedWithEsclations()` |
| 589 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyAssociateAndDiassociateSOHFromDetails()` |
| 590 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/operationalhour/OperationalHour.java` | `verifyAbleToCreateSOHFromOHDetails()` |
| 591 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `verifyCopySiteIsCreated()` |
| 592 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `verifyDeletedAssociatedSiteIsPresentInInactiveFilter()` |
| 593 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `verifySiteIsDeleted()` |
| 594 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `verifySiteIsEdited()` |
| 595 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `verifySiteIsRestoreToActiveSite()` |
| 596 | `com/zoho/automater/selenium/modules/admin/instanceconfigurations/site/Site.java` | `checkAllCustomerSitesListOrNotForMSPIssue()` |
| 597 | `com/zoho/automater/selenium/modules/admin/probesanddiscovery/credential/Credential.java` | `createWindowsCredential()` |
| 598 | `com/zoho/automater/selenium/modules/admin/templatesandforms/changetemplate/ChangeTemplate.java` | `verifyUserGroupsPresentInChangeTemplate()` |
| 599 | `com/zoho/automater/selenium/modules/admin/templatesandforms/changetemplate/ChangeTemplate.java` | `createChangeInRequesterLoginByUserGroupChangeTemplate()` |
| 600 | `com/zoho/automater/selenium/modules/admin/templatesandforms/changetemplate/ChangeTemplate.java` | `verifyAbleToDeletedUserGroupInChangeTemplate()` |
| 601 | `com/zoho/automater/selenium/modules/admin/templatesandforms/changetemplate/ChangeTemplate.java` | `verifyDeletedUserGroupShouldNotPresentInChangeTemplate()` |
| 602 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `duplicateCheck()` |
| 603 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `disableAndEnableCSUsingToggleButton()` |
| 604 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSClearValueOptionsAction()` |
| 605 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSSetCriteriaAction()` |
| 606 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `unknown()` |
| 607 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSDateConstraintActionInFAFRFieldChange()` |
| 608 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSSetCriteriaActionInFAFRFieldChange()` |
| 609 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSShowErrorActionInFAFRFieldChange()` |
| 610 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSClearErrorActionInFAFRFieldChange()` |
| 611 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `unknown()` |
| 612 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSOnFieldChangeActionInFAFRFormSubmit()` |
| 613 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSDateConstraintActionInFAFRFormSubmit()` |
| 614 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSSetCriteriaActionInFAFRFormSubmit()` |
| 615 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSShowErrorActionInFAFRFormSubmit()` |
| 616 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ChangeCustomscript.java` | `checkCSClearErrorActionInFAFRFormSubmit()` |
| 617 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `checkButtonsinCSLV()` |
| 618 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `checkTaskGroupinCustomScripts()` |
| 619 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `importSampleScriptsinLV()` |
| 620 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `checkToggleButton()` |
| 621 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `checkRelatedFormRulesinCustomScript()` |
| 622 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `checkTaskGroupCountinCustomScripts()` |
| 623 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `addCustomScriptsinFormRule()` |
| 624 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/Customscripts.java` | `demo()` |
| 625 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `mandatoryCheckAndCreate()` |
| 626 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `duplicateCheck()` |
| 627 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `maxmimumNameLengthCheck()` |
| 628 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkLHSValuePresentInCodeContainerForGeneral()` |
| 629 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkLHSValuePresentInCodeContainerForAction()` |
| 630 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkLHSValuePresentInCodeContainerForLocalStorage()` |
| 631 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkLHSValuePresentInCodeContainerForFieldChangeEvents()` |
| 632 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkLHSValuePresentInCodeContainerForFormSubmitEvents()` |
| 633 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkImportSampleCustomScript()` |
| 634 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `editReleaseCustomScript()` |
| 635 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `disableAndEnableCSUsingSettingIcon()` |
| 636 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `disableAndEnableCSUsingToggleButton()` |
| 637 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `deleteCSUsingSettingIcon()` |
| 638 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `bulkDisableEnableAndDelete()` |
| 639 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAlertActionInFormLoad()` |
| 640 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSConfirmActionInFormLoad()` |
| 641 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSPageRedirectActionInFormLoad()` |
| 642 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetAPIActionInFormLoad()` |
| 643 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSHideFieldsActionInFormLoad()` |
| 644 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSShowFieldsActionInFormLoad()` |
| 645 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDisableActionInFormLoad()` |
| 646 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSEnableActionInFormLoad()` |
| 647 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSMandateActionInFormLoad()` |
| 648 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSNonMandateActionInFormLoad()` |
| 649 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSRemoveOptionsActionInFormLoad()` |
| 650 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAddOptionsActionInFormLoad()` |
| 651 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSResetOptionsActionInFormLoad()` |
| 652 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearOptionsActionInFormLoad()` |
| 653 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetValueOptionsActionInFormLoad()` |
| 654 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetValueOptionsActionInFormLoad()` |
| 655 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearValueOptionsActionInFormLoad()` |
| 656 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDataStoreSetAndGetActionInFormLoad()` |
| 657 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFieldChangeActionInFormLoad()` |
| 658 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFormLoad()` |
| 659 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDateConstraintActionInFormLoad()` |
| 660 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetCriteriaActionInFormLoad()` |
| 661 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAlertActionInFAFRFieldChange()` |
| 662 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSConfirmActionInFAFRFieldChange()` |
| 663 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSPageRedirectActionInFAFRFieldChange()` |
| 664 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetAPIActionInFAFRFieldChange()` |
| 665 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSHideFieldsActionInFAFRFieldChange()` |
| 666 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSShowFieldsActionInFAFRFieldChange()` |
| 667 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDisableActionInFAFRFieldChange()` |
| 668 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSEnableActionInFAFRFieldChange()` |
| 669 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSMandateActionInFAFRFieldChange()` |
| 670 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSNonMandateActionInFAFRFieldChange()` |
| 671 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSRemoveOptionsActionInFAFRFieldChange()` |
| 672 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAddOptionsActionInFAFRFieldChange()` |
| 673 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSResetOptionsActionInFAFRFieldChange()` |
| 674 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearOptionsActionInFAFRFieldChange()` |
| 675 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetValueOptionsActionInFAFRFieldChange()` |
| 676 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetValueOptionsActionInFAFRFieldChange()` |
| 677 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearValueOptionsActionInFAFRFieldChange()` |
| 678 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDataStoreSetAndGetActionInFAFRFieldChange()` |
| 679 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFieldChangeActionInFAFRFieldChange()` |
| 680 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFAFRFieldChange()` |
| 681 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDateConstraintActionInFAFRFieldChange()` |
| 682 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetCriteriaActionInFAFRFieldChange()` |
| 683 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSShowErrorActionInFAFRFieldChange()` |
| 684 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearErrorActionInFAFRFieldChange()` |
| 685 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAlertActionInFAFRFormSubmit()` |
| 686 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSConfirmActionInFAFRFormSubmit()` |
| 687 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSPageRedirectActionInFAFRFormSubmit()` |
| 688 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetAPIActionInFAFRFormSubmit()` |
| 689 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSHideFieldsActionInFAFRFormSubmit()` |
| 690 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSShowFieldsActionInFAFRFormSubmit()` |
| 691 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDisableActionInFAFRFormSubmit()` |
| 692 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSEnableActionInFAFRFormSubmit()` |
| 693 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSMandateActionInFAFRFormSubmit()` |
| 694 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSNonMandateActionInFAFRFormSubmit()` |
| 695 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSRemoveOptionsActionInFAFRFormSubmit()` |
| 696 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSAddOptionsActionInFAFRFormSubmit()` |
| 697 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSResetOptionsActionInFAFRFormSubmit()` |
| 698 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearOptionsActionInFAFRFormSubmit()` |
| 699 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSGetValueOptionsActionInFAFRFormSubmit()` |
| 700 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetValueOptionsActionInFAFRFormSubmit()` |
| 701 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearValueOptionsActionInFAFRFormSubmit()` |
| 702 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDataStoreSetAndGetActionInFAFRFormSubmit()` |
| 703 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFieldChangeActionInFAFRFormSubmit()` |
| 704 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFAFRFormSubmit()` |
| 705 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSDateConstraintActionInFAFRFormSubmit()` |
| 706 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSSetCriteriaActionInFAFRFormSubmit()` |
| 707 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSShowErrorActionInFAFRFormSubmit()` |
| 708 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/ReleaseCustomscript.java` | `checkCSClearErrorActionInFAFRFormSubmit()` |
| 709 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `mandatoryCheckAndCreate()` |
| 710 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `duplicateCheck()` |
| 711 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `maxmimumNameLengthCheck()` |
| 712 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkLHSValuePresentInCodeContainerForGeneral()` |
| 713 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkLHSValuePresentInCodeContainerForAction()` |
| 714 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkLHSValuePresentInCodeContainerForLocalStorage()` |
| 715 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkLHSValuePresentInCodeContainerForFieldChangeEvents()` |
| 716 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkLHSValuePresentInCodeContainerForFormSubmitEvents()` |
| 717 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkImportSampleCustomScript()` |
| 718 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `editRequestCustomScript()` |
| 719 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `disableAndEnableCSUsingSettingIcon()` |
| 720 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `disableAndEnableCSUsingToggleButton()` |
| 721 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `deleteCSUsingSettingIcon()` |
| 722 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `bulkDisableEnableAndDelete()` |
| 723 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAlertActionInFormLoad()` |
| 724 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSConfirmActionInFormLoad()` |
| 725 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSPageRedirectActionInFormLoad()` |
| 726 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetAPIActionInFormLoad()` |
| 727 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSHideFieldsActionInFormLoad()` |
| 728 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSShowFieldsActionInFormLoad()` |
| 729 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDisableFieldsActionInFormLoad()` |
| 730 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSEnableFieldsActionInFormLoad()` |
| 731 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSMandateActionInFormLoad()` |
| 732 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSNonMandateActionInFormLoad()` |
| 733 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSRemoveOptionsActionInFormLoad()` |
| 734 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAddOptionsActionInFormLoad()` |
| 735 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSResetOptionsActionInFormLoad()` |
| 736 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearOptionsActionInFormLoad()` |
| 737 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetValueActionInFormLoad()` |
| 738 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetValueActionInFormLoad()` |
| 739 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearFieldValueActionInFormLoad()` |
| 740 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDataStoreSetAndGetActionInFormLoad()` |
| 741 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFieldChangeActionInFormLoad()` |
| 742 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFormLoad()` |
| 743 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDateConstraintActionInFormLoad()` |
| 744 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetCriteriaActionInFormLoad()` |
| 745 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAlertActionInFieldChange()` |
| 746 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSConfirmActionInFieldChange()` |
| 747 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSPageRedirectActionInFieldChange()` |
| 748 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetAPIActionInFieldChange()` |
| 749 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSHideFieldsActionInFieldChange()` |
| 750 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSShowFieldsActionInFieldChange()` |
| 751 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDisableFieldsActionInFieldChange()` |
| 752 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSEnableFieldsActionInFieldChange()` |
| 753 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSMandateActionInFieldChange()` |
| 754 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSNonMandateActionInFieldChange()` |
| 755 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSRemoveOptionsActionInFieldChange()` |
| 756 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAddOptionsActionInFieldChange()` |
| 757 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSResetOptionsActionInFieldChange()` |
| 758 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearOptionsActionInFieldChange()` |
| 759 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetValueActionInFieldChange()` |
| 760 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetValueActionInFieldChange()` |
| 761 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearFieldValueActionInFieldChange()` |
| 762 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDataStoreSetAndGetActionInFieldChange()` |
| 763 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFieldChangeActionInFieldChange()` |
| 764 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFieldChange()` |
| 765 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDateConstraintActionInFieldChange()` |
| 766 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetCriteriaActionInFieldChange()` |
| 767 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSShowfieldErrorActionInFieldChange()` |
| 768 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearfieldErrorActionInFieldChange()` |
| 769 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAlertActionInFormSubmit()` |
| 770 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSConfirmActionInFormSubmit()` |
| 771 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSPageRedirectActionInFormSubmit()` |
| 772 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetAPIActionInFormSubmit()` |
| 773 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSHideFieldsActionInFormSubmit()` |
| 774 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSShowFieldsActionInFormSubmit()` |
| 775 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDisableFieldsActionInFormSubmit()` |
| 776 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSEnableFieldsActionInFormSubmit()` |
| 777 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSMandateActionInFormSubmit()` |
| 778 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSNonMandateActionInFormSubmit()` |
| 779 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSRemoveOptionsActionInFormSubmit()` |
| 780 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSAddOptionsActionInFormSubmit()` |
| 781 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSResetOptionsActionInFormSubmit()` |
| 782 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearOptionsActionInFormSubmit()` |
| 783 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSGetValueActionInFormSubmit()` |
| 784 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetValueActionInFormSubmit()` |
| 785 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearFieldValueActionInFormSubmit()` |
| 786 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDataStoreSetAndGetActionInFormSubmit()` |
| 787 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFieldChangeActionInFormSubmit()` |
| 788 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSOnFormSubmitAndAbortActionInFormSubmit()` |
| 789 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSDateConstraintActionInFormSubmit()` |
| 790 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSSetCriteriaActionInFormSubmit()` |
| 791 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSShowFieldErrorActionInFormSubmit()` |
| 792 | `com/zoho/automater/selenium/modules/admin/templatesandforms/customscripts/RequestCustomscript.java` | `checkCSClearFieldErrorActionInFormSubmit()` |
| 793 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `createFromRuleInUIWithCustomScript()` |
| 794 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `mandatoryCheckForChange()` |
| 795 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `createFromRuleInUIWithAllActions()` |
| 796 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `checkCancelButtonForChange()` |
| 797 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `bulkEnableDisableAndDeleteForChange()` |
| 798 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `duplicateCheckForChange()` |
| 799 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `enableDisableForSingleFAFRForChange()` |
| 800 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ChangeFAFR.java` | `editFAFRForChange()` |
| 801 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `createFromRuleInUIWithCustomScript()` |
| 802 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `mandatoryCheckForIncident()` |
| 803 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `createFromRuleInUIWithAllActions()` |
| 804 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `checkCancelButtonForIR()` |
| 805 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `bulkEnableDisableAndDeleteForIncidentRequest()` |
| 806 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `duplicateCheckForIncident()` |
| 807 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `enableDisableForSingleFAFRForIR()` |
| 808 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/IncidentFAFR.java` | `editFAFRForIR()` |
| 809 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `createFromRuleInUIWithCustomScript()` |
| 810 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `mandatoryCheckForProblem()` |
| 811 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `createFromRuleInUIWithAllActions()` |
| 812 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `checkCancelButtonForProblem()` |
| 813 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `bulkEnableDisableAndDeleteForProblem()` |
| 814 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `duplicateCheckForProblem()` |
| 815 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `enableDisableForSingleFAFRForProblem()` |
| 816 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ProblemFAFR.java` | `editFAFRForProblem()` |
| 817 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `createFromRuleInUIWithCustomScript()` |
| 818 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `mandatoryCheckForRelease()` |
| 819 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `createFromRuleInUIWithAllActions()` |
| 820 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `checkCancelButtonForRelease()` |
| 821 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `bulkEnableDisableAndDeleteForRelease()` |
| 822 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `duplicateCheckForRelease()` |
| 823 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `enableDisableForSingleFAFRForRelease()` |
| 824 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ReleaseFAFR.java` | `editFAFRForRelease()` |
| 825 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `createFromRuleInUIWithCustomScript()` |
| 826 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `mandatoryCheckForService()` |
| 827 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `createFromRuleInUIWithAllActions()` |
| 828 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `checkCancelButtonForSR()` |
| 829 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `bulkEnableDisableAndDeleteForServiceRequest()` |
| 830 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `duplicateCheckForservice()` |
| 831 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `enableDisableForSingleFAFRForSR()` |
| 832 | `com/zoho/automater/selenium/modules/admin/templatesandforms/formrules/ServiceFAFR.java` | `editFAFRForSR()` |
| 833 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `checkDefaultTemplateForMSPIssue()` |
| 834 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `newIncidentTemplateButtonIsShownForInactiveCustomer()` |
| 835 | `com/zoho/automater/selenium/modules/admin/templatesandforms/incidenttemplate/IncidentTemplate.java` | `verifyTheTechnicianViewPermissionToTheirOwnRequests()` |
| 836 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `verifyTasksInProjectTemplate()` |
| 837 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `verifyTasksIsPresentInProjectByProjectTemplate()` |
| 838 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `createTaskWithAddTaskDropdownInProjectTemplate()` |
| 839 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `deleteMilestoneUsingRowActionsInProjectTemplate()` |
| 840 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `editMilestoneUsingRowActionsInProjectTemplate()` |
| 841 | `com/zoho/automater/selenium/modules/admin/templatesandforms/projecttemplate/ProjectTemplate.java` | `deleteMultipleMilestoneUsingDeleteButtonInProjectTemplate()` |
| 842 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyIconsPresentInCustomizeWindow()` |
| 843 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `descendingOrderInSerCatCustomize()` |
| 844 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `ascendingOrderInSerCatCustomize()` |
| 845 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyHelpCard()` |
| 846 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `moveServiceCategoryIntoAnotherFromNewServiceCategoryPopup()` |
| 847 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyMovedCategoryPresentInAnotherCategoryViaClickHere()` |
| 848 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyServiceTemplateShouldNotPresentWhenTreeIconDisabled()` |
| 849 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyIncidentTemplateShouldNotPresentWhenTreeIconDisabled()` |
| 850 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledServiceCategoryPresentInSearchTemplate()` |
| 851 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledServicetemplatePresentInSearchTemplate()` |
| 852 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledIncidentTemplatePresentInSearchTemplate()` |
| 853 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `copyInnerServiceTemplate()` |
| 854 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `deleteInnerServiceTemplateFromActions()` |
| 855 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `disableEnableInnerServiceTemplateFromActions()` |
| 856 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `disableEnableInnerIncidentTemplateFromActions()` |
| 857 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `deleteInnerIncidentTemplateFromActions()` |
| 858 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `deleteServiceCategoryAndMoveAllChildrenToAnotherCategory()` |
| 859 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/ServiceCategory.java` | `verifyDisabledIncidentTemplateShouldNotPresentInRequestCreation()` |
| 860 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `verifyingNoAlertWhileAccessingIncidentRequestTemplate()` |
| 861 | `com/zoho/automater/selenium/modules/admin/templatesandforms/servicecategory/roles/HelpdeskConfig.java` | `verifyDisabledIncidentTemplateShouldNotPresentInRequestCreation()` |
| 862 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `editTaskTemplateFromRowActions()` |
| 863 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `deleteTaskTemplateFromRowActions()` |
| 864 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `disableTaskTemplateFromRowActions()` |
| 865 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `disableAndEnableTaskTemplatesUsingToggleSlider()` |
| 866 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `copyTemplateForTaskTemplate()` |
| 867 | `com/zoho/automater/selenium/modules/admin/templatesandforms/tasktemplate/TaskTemplate.java` | `copyTaskTemplateUsingRowActions()` |
| 868 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `addUserGroup()` |
| 869 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `editUserGroupsFormUI()` |
| 870 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `deleteUserGroupsFormUI()` |
| 871 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `verifyEmailSiteUserGroup()` |
| 872 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `addEmailJobtitleVIPUserDepartmentAndVerify()` |
| 873 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `createAndAssociateOrgRolesInUsersAndVerify()` |
| 874 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `verifyAbleToCreateRequestByRequesterUsingAssociatedUserGroupTemplate()` |
| 875 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `verifyAbleToCreateRequestByRequesterUsingAssociatedUserGroupTemplateInServiceRequest()` |
| 876 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `verifyRequesterShouldNotPresentUnderPreviewWhenVIPCriteriaNotMatched()` |
| 877 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/usergroups/UserGroups.java` | `editOrgRolesCriteriaInUserGroupsFormUI()` |
| 878 | `com/zoho/automater/selenium/modules/admin/usersandpermissions/users/technician/Technician.java` | `allSitesIsShownOrNotInFilterBySiteDropDownForMSPIssue()` |
| 879 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkDefaultCategoryPredictioninRequest()` |
| 880 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkCustomCategoryPredictioninRequest()` |
| 881 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkDefaultSubCategoryPredictioninRequest()` |
| 882 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkCustomSubCategoryPredictioninRequest()` |
| 883 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkDefaultItemPredictioninRequest()` |
| 884 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkCustomItemPredictioninRequest()` |
| 885 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkDefaultPriorityPredictioninRequest()` |
| 886 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkCustomPriorityPredictioninRequest()` |
| 887 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkTemplatePredictioninRequest()` |
| 888 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkCategoryPrediction()` |
| 889 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkSubCategoryPrediction()` |
| 890 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkItemPrediction()` |
| 891 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkPriorityPrediction()` |
| 892 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkTechnicianPrediction()` |
| 893 | `com/zoho/automater/selenium/modules/admin/zia/Zia.java` | `checkTemplatePrediction()` |
| 894 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `CancelButtonwhileDeleteApLv()` |
| 895 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createAccessPointAssetviaQuickActions()` |
| 896 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createServerAssetviaQuickActions()` |
| 897 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createSmartPhoneAssetviaQuickActions()` |
| 898 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createCiscoRouterAssetviaQuickActions()` |
| 899 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createCiscoSwitchAssetviaQuickActions()` |
| 900 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createKeyboardAssetviaQuickActions()` |
| 901 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `searchAssetviaGlobalSearchBox()` |
| 902 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkEmptyAssetsMessageinRequester()` |
| 903 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAssetsHeaderinPrintPreview()` |
| 904 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkConsumableHeaderinPrintPreview()` |
| 905 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkSoftwareLicenseHeaderinPrintPreview()` |
| 906 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAllAssetsandCommontoDepartFilterUnderAssets()` |
| 907 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAssignedtoUsersFilterUnderAssets()` |
| 908 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkCommontoDepartmentFilterUnderConsumables()` |
| 909 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAllConsumablesFilterUnderConsumables()` |
| 910 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAssignedtoUsersFilterUnderConsumables()` |
| 911 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `checkAllFiltersinSlUnderDepartmentField()` |
| 912 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `createAccessPointAssetWithDefaultFields()` |
| 913 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `editAccessPointAssetWithDefaultFields()` |
| 914 | `com/zoho/automater/selenium/modules/assets/asset/Asset.java` | `allocateLicenseToSoftware()` |
| 915 | `com/zoho/automater/selenium/modules/assets/roles/AssetConfigRoleinAsset.java` | `checkAssetAllocationisPresent()` |
| 916 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `CancelButtonwhileDeleteApLv()` |
| 917 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `checkandcreateAccessPoint()` |
| 918 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `checkandCreatePinterusingFullControl()` |
| 919 | `com/zoho/automater/selenium/modules/assets/roles/FullControlRoleinAsset.java` | `checkandCreateApusingFullControl()` |
| 920 | `com/zoho/automater/selenium/modules/assets/roles/SDAssetManagerRoleinAsset.java` | `checkAssetAllocationisPresent()` |
| 921 | `com/zoho/automater/selenium/modules/assets/roles/SDRemoteControlRoleinAsset.java` | `checkAssetAllocationisPresentinSDRemote()` |
| 922 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `attachDetachProjectsInitiatedThatChangeInRHS()` |
| 923 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `attachDetachProjectCasuedByChangeInRHSViaNewProjectOption()` |
| 924 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifychangePrintPreviewLoaded()` |
| 925 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifychangePrintPreviewSectionDetailsIsNotPresent()` |
| 926 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyChangeDetailsSectionIsPresentAndNotPresent()` |
| 927 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyPlannningDetailsSectionIsPresentAndNotPresent()` |
| 928 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyCABEvaluationDetailsSectionIsPresentAndNotPresent()` |
| 929 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyImplementationDetailsSectionIsPresentAndNotPresent()` |
| 930 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyUATDetailsSectionIsPresentAndNotPresent()` |
| 931 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyReleaseDetailsSectionIsPresentAndNotPresent()` |
| 932 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyReviewDetailsSectionIsPresentAndNotPresent()` |
| 933 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyCloseDetailsSectionIsPresentAndNotPresent()` |
| 934 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyApprovalssSectionIsPresentAndNotPresent()` |
| 935 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyDowntimeSectionIsPresentAndNotPresent()` |
| 936 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyWorklogSectionIsPresentAndNotPresent()` |
| 937 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyNotesSectionIsPresentAndNotPresent()` |
| 938 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyConversationSectionIsPresentAndNotPresent()` |
| 939 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyStatusCommentsSectionIsPresentAndNotPresent()` |
| 940 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `verifyHistorySectionIsPresentAndNotPresent()` |
| 941 | `com/zoho/automater/selenium/modules/changes/change/DetailsView.java` | `copyChangeinDV()` |
| 942 | `com/zoho/automater/selenium/modules/changes/change/ImplementationStage.java` | `verifyArchievedRequestPresentInArchivedIncidentsTabInRequestCausedByChange()` |
| 943 | `com/zoho/automater/selenium/modules/changes/change/ImplementationStage.java` | `verifyAbletoAttachRequestInRecentIncidentsTabPresentInRequestInitiatedChange()` |
| 944 | `com/zoho/automater/selenium/modules/changes/change/ImplementationStage.java` | `verifyAttachAndDetachButtonNotPresentInArchievedIncidentInRequestsThatInitiatedChange()` |
| 945 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `allDataExportInChange()` |
| 946 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `currentViewExportInChange()` |
| 947 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `selectedDataExportInChange()` |
| 948 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 949 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `allDataExportInTrashChange()` |
| 950 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `currentViewExportInTrashChange()` |
| 951 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `selectedDataExportInTrashChange()` |
| 952 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifySelectedDataOptionIsDisabledInTrashChange()` |
| 953 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyChangeColumnChooserListed()` |
| 954 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyCloseStageAndCompletedStatusListed()` |
| 955 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `selectRolesInColumnChooserAndVerify()` |
| 956 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyRolesIconPresentInChange()` |
| 957 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyUsersAndAssignedRolesByClickingRolesIcon()` |
| 958 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `verifyNoUsersAssignedToChangeByClickingRolesIcon()` |
| 959 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `changeRolesUserShouldPresentInListiviewWhenAssociatedInTemplate()` |
| 960 | `com/zoho/automater/selenium/modules/changes/change/ListView.java` | `shortcutWithCtrlAlt()` |
| 961 | `com/zoho/automater/selenium/modules/changes/changetask/CabEvaluationTask.java` | `editTaskUsingRowActionInCABEvaluation()` |
| 962 | `com/zoho/automater/selenium/modules/changes/changetask/CabEvaluationTask.java` | `deleteTaskUsingRowActionInCABEvaluation()` |
| 963 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `demo()` |
| 964 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `newButtonShownOrNotForInactiveCustomer()` |
| 965 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `inactiveCustomerAbleOrUnabletoCreateNewBusinessView()` |
| 966 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `allDataExportInCmdb()` |
| 967 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `currentViewExportInCmdb()` |
| 968 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `selectedDataExportInCmdb()` |
| 969 | `com/zoho/automater/selenium/modules/cmdb/cmdb/Cmdb.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 970 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `allDataExportInCmdb()` |
| 971 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `currentViewExportInCmdb()` |
| 972 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `selectedDataExportInCmdb()` |
| 973 | `com/zoho/automater/selenium/modules/cmdb/roles/FullControlRoleinCmdb.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 974 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `createSameContractDifferentCustomerForMSPIssue()` |
| 975 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyExportIconInContract()` |
| 976 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyAllDataExportOptionsPresentInExportPopup()` |
| 977 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 978 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInExportPopup()` |
| 979 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `allDataExportInContract()` |
| 980 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `currentViewExportInContract()` |
| 981 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `selectedDataExportInContract()` |
| 982 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 983 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyExportIconPresentInTrashContract()` |
| 984 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyContractColumnChooserListed()` |
| 985 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyExpiredContractsFilterExport()` |
| 986 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyAllDataExportOptionsPresentInTrashContract()` |
| 987 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifyAllDataFromCurrentViewExportOptionsPresentInTrashContract()` |
| 988 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `verifySelectedDataFromCurrentViewExportOptionsPresentInTrashContract()` |
| 989 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `allDataExportInTrashContract()` |
| 990 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `currentViewExportInTrashContract()` |
| 991 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `selectedDataExportInTrashContract()` |
| 992 | `com/zoho/automater/selenium/modules/contracts/contract/Contract.java` | `selectedDataExportInYetToBeActiveContractFilter()` |
| 993 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `checkAddCountryColumnInCustomerCustomViewForMSPIssue()` |
| 994 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `createCustomerUseExcistingSiteName()` |
| 995 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `updateCountryForCustomer()` |
| 996 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `checkDescriptionShownEmptyOrNotForCustomCustomer()` |
| 997 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `customViewConditionIsNotAndIsNotEmptyWorkinfOrNotForMSPIssue()` |
| 998 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `encodeIssueForInactiveCustomer()` |
| 999 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `inactiveCustomerAnnouncementPageEditOptionIsHereOrNot()` |
| 1000 | `com/zoho/automater/selenium/modules/customers/customer/Customer.java` | `createPO()` |
| 1001 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `addAnnouncementWithUserGroup()` |
| 1002 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `verifyAnnouncementNameInBanner()` |
| 1003 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `verifyUserGroupPresentInAnnouncementDetailsview()` |
| 1004 | `com/zoho/automater/selenium/modules/general/announcement/Announcement.java` | `shortcutWithCtrlAlt()` |
| 1005 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `newGraphWidgetFieldsVerification()` |
| 1006 | `com/zoho/automater/selenium/modules/general/dashboard/Dashboard.java` | `dialGraphTypeInNewGraphWidget()` |
| 1007 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `checkIncidentAndServiceRequestIconShownOrNotForMSPIssue()` |
| 1008 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `siteListedUnderCustomerOrNotInSiteDropdownForMSPIssue()` |
| 1009 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `inactiveCustomerKnowTheNewMaintenanceButttonOrNotForMSPIssue()` |
| 1010 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `invalidCIisShownWhileEditingMaintenanceForMSPIssue()` |
| 1011 | `com/zoho/automater/selenium/modules/maintenance/requestmaintenance/RequestMaintenance.java` | `addMentionsForUsersInNotesFromDetailview()` |
| 1012 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyArchievedRequestPresentInArchivedIncidentsTabInProblem()` |
| 1013 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyUnableToAddNotesForArchivedRequestInArchievedIncidents()` |
| 1014 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAbletoAttachRequestInRecentIncidentsTabPresentInProblemForAssociatedIncidents()` |
| 1015 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyAttachAndDetachButtonNotPresentInArchievedIncident()` |
| 1016 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `allDataExportInProblem()` |
| 1017 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `currentViewExportInProblem()` |
| 1018 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `selectedDataExportInProblem()` |
| 1019 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 1020 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `allDataExportInTrashProblem()` |
| 1021 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `currentViewExportInTrashProblem()` |
| 1022 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `selectedDataExportInTrashProblem()` |
| 1023 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifySelectedDataOptionIsDisabledInTrashProblem()` |
| 1024 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `verifyProblemColumnChooserListed()` |
| 1025 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `shortcutWithAlt()` |
| 1026 | `com/zoho/automater/selenium/modules/problems/problem/Problem.java` | `unknown()` |
| 1027 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyExportIconInProblem()` |
| 1028 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `allDataExportInProblem()` |
| 1029 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `currentViewExportInProblem()` |
| 1030 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `selectedDataExportInProblem()` |
| 1031 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 1032 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `allDataExportInTrashProblem()` |
| 1033 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `currentViewExportInTrashProblem()` |
| 1034 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `selectedDataExportInTrashProblem()` |
| 1035 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifySelectedDataOptionIsDisabledInTrashProblem()` |
| 1036 | `com/zoho/automater/selenium/modules/problems/problem/roles/ProblemSDSiteAdminLVExport.java` | `verifyProblemColumnChooserListed()` |
| 1037 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `addProjectMilestoneInDefaultProjectManagerRole()` |
| 1038 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `editProjectMilestoneUsingRowActionsInDefaultProjectManagerRole()` |
| 1039 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `deleteProjectMilestoneUsingRowActionsInDefaultProjectManagerRole()` |
| 1040 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `deleteProjectMilestoneUsingDeleteButtonInDefaultProjectManagerRole()` |
| 1041 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `deleteMultipleProjectMilestoneUsingDeleteButtonInDefaultProjectManagerRole()` |
| 1042 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `closeSingleProjectMilestoneInDefaultProjectManagerRole()` |
| 1043 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `closeMultipleProjectMilestoneInDefaultProjectManagerRole()` |
| 1044 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `pickupSingleProjectMilestoneInDefaultProjectManagerRole()` |
| 1045 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `assignOwnerProjectMilestoneInDefaultProjectManagerRole()` |
| 1046 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `assignOwnerForMultipleProjectMilestoneInDefaultProjectManagerRole()` |
| 1047 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `organizeMilestoneInDefaultProjectManagerRole()` |
| 1048 | `com/zoho/automater/selenium/modules/projects/milestone/roles/projectmanager/MilestoneForProjectManager.java` | `quickAddProjectMilestoneInDefaultProjectManagerRole()` |
| 1049 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachChangeCausedByProjectInRHSViaNewChangeOption()` |
| 1050 | `com/zoho/automater/selenium/modules/projects/project/ProjectDetailsView.java` | `attachDetachChangeInitiatedTheProjectInRHS()` |
| 1051 | `com/zoho/automater/selenium/modules/projects/project/ProjectListView.java` | `shortcutWithCtrlAlt()` |
| 1052 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyNewProjectButtonNotPresentInProjectListviewViewEditRole()` |
| 1053 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editProjectUsingSettingsIconForViewEditRole()` |
| 1054 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editProjectindetailviewForViewEditRole()` |
| 1055 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteProjectNotPresentUsingSettingsIconForViewEditRole()` |
| 1056 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteBtnNotPresentInListviewForViewEditRole()` |
| 1057 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteProjectNotPresentFromActionsDropdownForViewEditRole()` |
| 1058 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyAddMilestoneBtnNotPresentForViewEditRole()` |
| 1059 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editProjectMilestoneUsingRowActionsForViewEditRole()` |
| 1060 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteNotPresentInMilestoneUsingRowActionsForViewEditRole()` |
| 1061 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteBtnNotPresentInMilestoneForViewEditRole()` |
| 1062 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editMilestoneFromMilestoneDetailviewForViewEditRole()` |
| 1063 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `deleteMilestoneInMilestoneDetailviewForViewEditRole()` |
| 1064 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteBtnNotPresentInMilestoneDetailviewForViewEditRole()` |
| 1065 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyAddTaskBtnNotPresentForViewEditRole()` |
| 1066 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyAddTaskBtnNotPresentFromActionsDropdownForViewEditRole()` |
| 1067 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editTaskUsingRowActionsForViewEditRole()` |
| 1068 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `editTaskInTaskDetailviewForViewEditRole()` |
| 1069 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteBtnNotPresentInTaskForViewEditRole()` |
| 1070 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `verifyDeleteBtnNotPresentInTaskDetailviewForViewEditRole()` |
| 1071 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewEditOnly.java` | `pickUpMilestoneForViewEditRole()` |
| 1072 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyNewProjectButtonNotPresentInProjectListviewViewAllRole()` |
| 1073 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditProjectNotPresentUsingSettingsIcon()` |
| 1074 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditProjectBtnNotPresentIndetailview()` |
| 1075 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteProjectNotPresentUsingSettingsIcon()` |
| 1076 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteBtnNotPresentInListview()` |
| 1077 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteProjectNotPresentFromActionsDropdown()` |
| 1078 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyAddMilestoneBtnNotPresent()` |
| 1079 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditMilestoneBtnNotPresentUsingRowActions()` |
| 1080 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteNotPresentInMilestoneUsingRowActions()` |
| 1081 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteBtnNotPresentInMilestone()` |
| 1082 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditBtnNotPresentInMilestoneDetailview()` |
| 1083 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteBtnNotPresentInMilestoneDetailview()` |
| 1084 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyAddTaskBtnNotPresent()` |
| 1085 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyAddTaskBtnNotPresentFromActionsDropdown()` |
| 1086 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditTaskNotPresentUsingRowActions()` |
| 1087 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyEditTaskBtnNotPresentInTaskDetailview()` |
| 1088 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteBtnNotPresentInTask()` |
| 1089 | `com/zoho/automater/selenium/modules/projects/project/roles/customroles/ProjectsViewOnly.java` | `verifyDeleteBtnNotPresentInTaskDetailview()` |
| 1090 | `com/zoho/automater/selenium/modules/projects/project/roles/projectmanager/ProjectManagerRole.java` | `verifyCustomFilterIconNotPresentInProjectListview()` |
| 1091 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `verifyAddedReplyTaskCommentsInHistory()` |
| 1092 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `editReplyFromTaskCommentsInProject()` |
| 1093 | `com/zoho/automater/selenium/modules/projects/projecttask/ProjectTask.java` | `addCommentFromTaskDetailviewActionsDropdown()` |
| 1094 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `addTaskInProjectInDefaultProjectManagerRole()` |
| 1095 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `editTaskUsingRowActionsInProjectInDefaultProjectManagerRole()` |
| 1096 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `editTaskAndVerifyInDetailviewInProjectInDefaultProjectManagerRole()` |
| 1097 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `deleteSingleTaskUsingRowActionInProjectInDefaultProjectManagerRole()` |
| 1098 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `deleteMultipleTaskInProjectInDefaultProjectManagerRole()` |
| 1099 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `createTaskWithAddTaskDropdownInProjectInDefaultProjectManagerRole()` |
| 1100 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `closeSingleTaskInProjectInDefaultProjectManagerRole()` |
| 1101 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `closeMultipleTaskInProjectInDefaultProjectManagerRole()` |
| 1102 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `triggerSingleTaskInProjectInDefaultProjectManagerRole()` |
| 1103 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `assignOwnerForSingleTaskInProjectInDefaultProjectManagerRole()` |
| 1104 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `assignOwnerForMultipleTaskInProjectInDefaultProjectManagerRole()` |
| 1105 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `assignMilestoneForSingleTaskInProjectInDefaultProjectManagerRole()` |
| 1106 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `assignMilestoneForMultipleTaskInProjectInDefaultProjectManagerRole()` |
| 1107 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `VerfiyTaskPresentInMilestoneInDefaultProjectManagerRole()` |
| 1108 | `com/zoho/automater/selenium/modules/projects/projecttask/roles/ProjectTaskForProjectManager.java` | `addTaskFromTemplateFromAddTaskDropdownInProjectInDefaultProjectManagerRole()` |
| 1109 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/CustomerIssueinPurchaseOrder.java` | `checkDecimalValuesareshowninTotalCostPO()` |
| 1110 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `allDataExportInPurchase()` |
| 1111 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `currentViewExportInPurchase()` |
| 1112 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `selectedDataExportInPurchase()` |
| 1113 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 1114 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `verifyPurchaseColumnChooserListed()` |
| 1115 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `exportApprovedPurchaseOrderFilter()` |
| 1116 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `exportApprovalPendingPurchaseOrderFilter()` |
| 1117 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `addNoteInConversationPageFromActionDropDownInPurchase()` |
| 1118 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `removeAttachemntFromNote()` |
| 1119 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `cancelNote()` |
| 1120 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `checkApprovarRejectedHimApproval()` |
| 1121 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `checkOtherUserNotesUnableToEditAndDelete()` |
| 1122 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `checkRequesterAbleApproveFromApprovalPopUp()` |
| 1123 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/PurchaseOrder.java` | `checkRequesterAbleRejecteFromApprovalPopUp()` |
| 1124 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `addNoteInConversationPageFromActionDropDownInPurchase()` |
| 1125 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `editNoteInConversationPageInPurchase()` |
| 1126 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `deleteNoteInConversationPageInPurchase()` |
| 1127 | `com/zoho/automater/selenium/modules/purchaseorders/purchaseorder/purchaseorderview/PurchaseOrderView.java` | `checkOtherUserNotesUnableToEditAndDelete()` |
| 1128 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyArchievedRequestPresentInArchivedIncidentsTabInRequestInitiatedRelease()` |
| 1129 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `allDataExportInRelease()` |
| 1130 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `currentViewExportInRelease()` |
| 1131 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `selectedDataExportInRelease()` |
| 1132 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifySelectedDataOptionIsDisabledInExportPopup()` |
| 1133 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `verifyReleaseColumnChooserListed()` |
| 1134 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `attachDetachAssociateMilestoneThatInitiatedRelease()` |
| 1135 | `com/zoho/automater/selenium/modules/releases/release/ListView.java` | `shortcutWithCtrlAlt()` |
| 1136 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `verifyCloseStageAndCompletedStatusListedInRelease()` |
| 1137 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `exportAllDataFromCanceledReleaseFilter()` |
| 1138 | `com/zoho/automater/selenium/modules/releases/release/ReleaseManagerCases.java` | `exportAllDataFromClosedReleaseFilter()` |
| 1139 | `com/zoho/automater/selenium/modules/releases/releasetask/CloseTask.java` | `verifyAlertMessageInOrganizeTaskPopupInClosure()` |
| 1140 | `com/zoho/automater/selenium/modules/releases/releasetask/DevelopmentTask.java` | `verifyAlertMessageInOrganizeTaskPopupInDevelopment()` |
| 1141 | `com/zoho/automater/selenium/modules/releases/releasetask/PlanningTask.java` | `verifyAlertMessageInOrganizeTaskPopupInPlanning()` |
| 1142 | `com/zoho/automater/selenium/modules/releases/releasetask/ReviewTask.java` | `verifyAlertMessageInOrganizeTaskPopupInReview()` |
| 1143 | `com/zoho/automater/selenium/modules/releases/releasetask/SubmissionTask.java` | `verifyAlertMessageInOrganizeTaskPopup()` |
| 1144 | `com/zoho/automater/selenium/modules/releases/releasetask/TestingTask.java` | `verifyAlertMessageInOrganizeTaskPopupInPlanning()` |
| 1145 | `com/zoho/automater/selenium/modules/releases/releasetask/UATTask.java` | `addTaskTypeWithSpecialCharInEditTaskPopupInUAT()` |
| 1146 | `com/zoho/automater/selenium/modules/releases/releasetask/UATTask.java` | `verifyAlertMessageInOrganizeTaskPopupInUAT()` |
| 1147 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkHistorywhileApprovalRequiredForaRequest()` |
| 1148 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkEmailIdisShowninBulkEditLookupfieldDropdown()` |
| 1149 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `checkApprovalButtoninRequester()` |
| 1150 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `CheckTasksCountinOriginalSRandDuplicateSR()` |
| 1151 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1152 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `incidentandServicerequestExportallData()` |
| 1153 | `com/zoho/automater/selenium/modules/requests/CustomerIssuesinRequest.java` | `incidentandServicerequestExportSelectedData()` |
| 1154 | `com/zoho/automater/selenium/modules/requests/request/Request.java` | `checkForReminderinHome()` |
| 1155 | `com/zoho/automater/selenium/modules/requests/request/Request.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1156 | `com/zoho/automater/selenium/modules/requests/request/Request.java` | `incidentandServicerequestExportallData()` |
| 1157 | `com/zoho/automater/selenium/modules/requests/request/Request.java` | `incidentandServicerequestExportSelectedData()` |
| 1158 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `spotEditCategoryFromDetailsTab()` |
| 1159 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addNotesFromDP()` |
| 1160 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `spotEditAssetDetailsView()` |
| 1161 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `checkForReminderinHome()` |
| 1162 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyRequestIsLandingToDetailviewFromPreviousRequestPopup()` |
| 1163 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAbleToAddNotesInMergeRequestPopup()` |
| 1164 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAbleToAddNotesInLinkedRequestPopup()` |
| 1165 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addNotesInPopupAndLinkedRequest()` |
| 1166 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `createRequestUsingMobileApplicationMode()` |
| 1167 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyMobileApplicationModeIsPresentInEditForm()` |
| 1168 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyMobileApplicationModeIsPresentInRequesterForm()` |
| 1169 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `checkCatagoryFieldSearchAndSelectForMSPIssue()` |
| 1170 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `FilterFavouriteIconIsShownOrNotForMSPIssue()` |
| 1171 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `quickActionNewRequestPopUpIsShownForInactiveCustomer()` |
| 1172 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `inactiveCustomerableOrUnableToPerformeAnyActionInKanbanView()` |
| 1173 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyExportIcon()` |
| 1174 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyExportAllDataOption()` |
| 1175 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyExportAllDataCurrentviewoption()` |
| 1176 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyExportSelectedDataCurrentViewoption()` |
| 1177 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportAllDataFromCurrentView()` |
| 1178 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expAllData()` |
| 1179 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expSelectedData()` |
| 1180 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportAllDataFromCVTempview()` |
| 1181 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expAllDatatempview()` |
| 1182 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expSelectedDataTempview()` |
| 1183 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportAllRequests()` |
| 1184 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportPendingRequest()` |
| 1185 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportTrashRequest()` |
| 1186 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `exportAllMyRequest()` |
| 1187 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expOpenUnassigned()` |
| 1188 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `expRequestsCreatedTodayIncident()` |
| 1189 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `cancelRequestExport()` |
| 1190 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `completedRequestExport()` |
| 1191 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `allMygroupRequestExp()` |
| 1192 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `archiveRequestExport()` |
| 1193 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `reqExportCustomTemplate()` |
| 1194 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `reqExportCustomTemplateWithUdf()` |
| 1195 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `requestExpCreatedfromActions()` |
| 1196 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForGroupMembersInNotesFromListView()` |
| 1197 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForTechnicianInNotesFromListView()` |
| 1198 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRequesterReportingToInNotesFromListView()` |
| 1199 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForTechnicianReportingToInNotesFromListView()` |
| 1200 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForGroupHeadInNotesFromListView()` |
| 1201 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForUsersInNotesFromListView()` |
| 1202 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyErrorShouldThrownForRequesterMentionInNote()` |
| 1203 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyNotesShouldDisplayForLinkedRequest()` |
| 1204 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyNoteMentionsIsUpdatedFromDetailview()` |
| 1205 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyUserDetailsWhenHoverInDetailview()` |
| 1206 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAttachmentIsPresentInTrashRequest()` |
| 1207 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyRequesterNotAllowedToEditNotes()` |
| 1208 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyRequesterNotAllowedToEditAttachments()` |
| 1209 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAttachmentIsPresentInRestoreRequestDetailview()` |
| 1210 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyNoteAndAttachmentDeletedAndVerifyInHistory()` |
| 1211 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyNoteAndAttachmentVerifyInHistory()` |
| 1212 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteInchargeOfRequest()` |
| 1213 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteManagerOfRequest()` |
| 1214 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteManagerOfRequester()` |
| 1215 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteManagerOfTechnician()` |
| 1216 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteInchargeOfRequester()` |
| 1217 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForSiteInchargeOfTechnician()` |
| 1218 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptHeadOfTechnician()` |
| 1219 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptHeadOfRequest()` |
| 1220 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForGeneralManager()` |
| 1221 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptApproverOfTechnician()` |
| 1222 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptApproverOfRequest()` |
| 1223 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptInchargeOfRequest()` |
| 1224 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForDeptInchargeOfTechnician()` |
| 1225 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalInchargeOfRequest()` |
| 1226 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalInchargeOfRequester()` |
| 1227 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalInchargeOfTechnician()` |
| 1228 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalManagerOfRequest()` |
| 1229 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalManagerOfRequester()` |
| 1230 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `addMentionsForRegionalManagerOfTechnician()` |
| 1231 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `verifyAssetsPresentInAssetsOwnedPopup()` |
| 1232 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutGoToPageHR()` |
| 1233 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutWithAlt()` |
| 1234 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutWithCtrlAlt()` |
| 1235 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutShift()` |
| 1236 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `globalSearch()` |
| 1237 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutForDetailPage()` |
| 1238 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `shortcutForRequestActions()` |
| 1239 | `com/zoho/automater/selenium/modules/requests/request/incident/IncidentRequest.java` | `withClosureRule()` |
| 1240 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `spotEditAssetDetailsView()` |
| 1241 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyMobileApplicationModeIsPresentInRequesterForm()` |
| 1242 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyExportIcon()` |
| 1243 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyExportAllDataOption()` |
| 1244 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyExportAllDataCurrentviewoption()` |
| 1245 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyExportSelectedDataCurrentViewoption()` |
| 1246 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportAllDataFromCurrentView()` |
| 1247 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expAllData()` |
| 1248 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expSelectedData()` |
| 1249 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportAllDataFromCVTempview()` |
| 1250 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expAllDatatempview()` |
| 1251 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expSelectedDataTempview()` |
| 1252 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportAllRequests()` |
| 1253 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportPendingRequest()` |
| 1254 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportTrashRequest()` |
| 1255 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `exportAllMyRequest()` |
| 1256 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expOpenUnassigned()` |
| 1257 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `expRequestsCreatedTodayIncident()` |
| 1258 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `cancelRequestExport()` |
| 1259 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `completedRequestExport()` |
| 1260 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `allMygroupRequestExp()` |
| 1261 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `archiveRequestExport()` |
| 1262 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `reqExportCustomTemplate()` |
| 1263 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `reqExportCustomTemplateWithUdf()` |
| 1264 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `requestExpCreatedfromActions()` |
| 1265 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `verifyAssetsPresentInAssetsOwnedPopup()` |
| 1266 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `addMentionsForDeptApproverOfRequest()` |
| 1267 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `incidentandServicerequestExportallData()` |
| 1268 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1269 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `incidentandServicerequestExportSelectedData()` |
| 1270 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `withClosureRule()` |
| 1271 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `shortcutWithCtrlAlt()` |
| 1272 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControl.java` | `shortcutWithAlt()` |
| 1273 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `verifyExportIcon()` |
| 1274 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `verifyExportAllDataOption()` |
| 1275 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `verifyExportAllDataCurrentviewoption()` |
| 1276 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportAllDataFromCurrentView()` |
| 1277 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expAllData()` |
| 1278 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expSelectedData()` |
| 1279 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportAllDataFromCVTempview()` |
| 1280 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expAllDatatempview()` |
| 1281 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expSelectedDataTempview()` |
| 1282 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportAllRequests()` |
| 1283 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportPendingRequest()` |
| 1284 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportTrashRequest()` |
| 1285 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `exportAllMyRequest()` |
| 1286 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expOpenUnassigned()` |
| 1287 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `expRequestsCreatedTodayIncident()` |
| 1288 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `cancelRequestExport()` |
| 1289 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `completedRequestExport()` |
| 1290 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `allMygroupRequestExp()` |
| 1291 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `archiveRequestExport()` |
| 1292 | `com/zoho/automater/selenium/modules/requests/request/roles/IncidentRequestFullControlExport.java` | `reqExportCustomTemplate()` |
| 1293 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1294 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `incidentandServicerequestExportallData()` |
| 1295 | `com/zoho/automater/selenium/modules/requests/request/roles/Requester.java` | `incidentandServicerequestExportSelectedData()` |
| 1296 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `spotEditAssetDetailsView()` |
| 1297 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportAllDataFromCurrentView()` |
| 1298 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expAllData()` |
| 1299 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expSelectedData()` |
| 1300 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportAllDataFromCVTempview()` |
| 1301 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expAllDatatempview()` |
| 1302 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expSelectedDataTempview()` |
| 1303 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportAllRequests()` |
| 1304 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportPendingRequest()` |
| 1305 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportTrashRequest()` |
| 1306 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportAllMyRequestService()` |
| 1307 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expOpenUnassigned()` |
| 1308 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `expRequestsCreatedTodayService()` |
| 1309 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `cancelRequestExport()` |
| 1310 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `completedRequestExport()` |
| 1311 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `allMygroupRequestExpService()` |
| 1312 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `reqExportCustomTemplate()` |
| 1313 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `reqExportCustomTemplateWithUdf()` |
| 1314 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `exportConvertedIncidentRequestFromActions()` |
| 1315 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `incidentandServicerequestExportallData()` |
| 1316 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1317 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `withClosureRule()` |
| 1318 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `shortcutWithCtrlAlt()` |
| 1319 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControl.java` | `shortcutWithAlt()` |
| 1320 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportAllDataFromCurrentView()` |
| 1321 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expAllData()` |
| 1322 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expSelectedData()` |
| 1323 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportAllDataFromCVTempview()` |
| 1324 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expAllDatatempview()` |
| 1325 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expSelectedDataTempview()` |
| 1326 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportAllRequests()` |
| 1327 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportPendingRequest()` |
| 1328 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportTrashRequest()` |
| 1329 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `exportAllMyRequestService()` |
| 1330 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expOpenUnassigned()` |
| 1331 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `expRequestsCreatedTodayService()` |
| 1332 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `cancelRequestExport()` |
| 1333 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `completedRequestExport()` |
| 1334 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `allMygroupRequestExpService()` |
| 1335 | `com/zoho/automater/selenium/modules/requests/request/roles/ServiceRequestFullControlExport.java` | `reqExportCustomTemplate()` |
| 1336 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `addNotesFromDP()` |
| 1337 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `spotEditAssetDetailsView()` |
| 1338 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `checkForReminderinHome()` |
| 1339 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `createRequestUsingMulitipleApprovalStageTemplateForMSPIssue()` |
| 1340 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportAllDataFromCurrentView()` |
| 1341 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expAllData()` |
| 1342 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expSelectedData()` |
| 1343 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportAllDataFromCVTempview()` |
| 1344 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expAllDatatempview()` |
| 1345 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expSelectedDataTempview()` |
| 1346 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportAllRequests()` |
| 1347 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportPendingRequest()` |
| 1348 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportTrashRequest()` |
| 1349 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportAllMyRequestService()` |
| 1350 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expOpenUnassigned()` |
| 1351 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `expRequestsCreatedTodayService()` |
| 1352 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `cancelRequestExport()` |
| 1353 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `completedRequestExport()` |
| 1354 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `allMygroupRequestExpService()` |
| 1355 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `reqExportCustomTemplate()` |
| 1356 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `reqExportCustomTemplateWithUdf()` |
| 1357 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `exportConvertedIncidentRequestFromActions()` |
| 1358 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutGoToPageHR()` |
| 1359 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutWithAlt()` |
| 1360 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutWithCtrlAlt()` |
| 1361 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutShift()` |
| 1362 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `globalSearch()` |
| 1363 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutForDetailPage()` |
| 1364 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `shortcutForRequestActions()` |
| 1365 | `com/zoho/automater/selenium/modules/requests/request/service/ServiceRequest.java` | `withClosureRule()` |
| 1366 | `com/zoho/automater/selenium/modules/requests/request/sitebased/RequestSiteBased.java` | `incidentandServicerequestExportallDatacurrentview()` |
| 1367 | `com/zoho/automater/selenium/modules/requests/request/sitebased/RequestSiteBased.java` | `incidentandServicerequestExportallData()` |
| 1368 | `com/zoho/automater/selenium/modules/requests/request/sitebased/RequestSiteBased.java` | `incidentandServicerequestExportSelectedData()` |
| 1369 | `com/zoho/automater/selenium/modules/requests/worklog/Worklog.java` | `createandEditWorklogUsingActionsDrop()` |
| 1370 | `com/zoho/automater/selenium/modules/requests/worklog/Worklog.java` | `createandEditWorklogViaTimeElapsedTab()` |
| 1371 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `SolutionWithTrashedProblem()` |
| 1372 | `com/zoho/automater/selenium/modules/solutions/solution/Solution.java` | `shortcutWithAlt()` |