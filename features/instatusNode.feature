Feature: Elevator

Scenario: initialize get_incidents verify_size_list not_empty_list view_incident_details get_incidents verify_size_list not_empty_list exit_system 

Given initialize
When get_incidents
And verify_size_list
And not_empty_list
Then notEmptyList
When view_incident_details
Then incidentActiveSuccess
When get_incidents
And verify_size_list
And not_empty_list
Then notEmptyList
When exit_system


Scenario: initialize get_incidents verify_size_list not_empty_list delete_a_incident_from_list get_incidents verify_size_list not_empty_list exit_system 

Given initialize
When get_incidents
And verify_size_list
And not_empty_list
Then notEmptyList
When delete_a_incident_from_list
Then deleteSuccess
When get_incidents
And verify_size_list
And not_empty_list
Then notEmptyList
When exit_system

