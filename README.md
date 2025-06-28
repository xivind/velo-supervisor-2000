# velo-supervisor-2000
Velo Supervisor 2000 is a program to keep track of lifetime and service intervals of bicycle components, based on activity data from Strava.

---
**📡 IMPORTANT INFORMATION TO USERS PARTICIPARTING IN PILOTING Q1 2025**

🔴 This software is currently under active development. Use it at your own risk, as there may be issues with data integrity. We do our best to solve bugs and make improvements, but cant promise you any support. The GUI does currently not work with mobile devices. Please take this into consideration if you are piloting. We are working on fixing this. See the [project board](https://github.com/users/xivind/projects/2/views/1) for a complete list of issues

The onboarding procedure is not ready yet, but you can start piloting already now by setting up Velo Supervisor 2000 manually. Complete the following steps:
- **Step 1:** Copy the file `backend/template_db.sqlite` and place it somewhere outside the repo
- **Step 2:** Copy the file `backend/strava_tokens.example.json` and place it somewhere outside the repo. You should rename the file as well, e.g. to `strava_tokens.json`. Modify it with your own data and dont share it with anyone else. [See this tutorial](https://developers.strava.com/docs/getting-started/) on how to obtain the oauth-data from Strava
- **Step 3:** Make a copy of `backend/config.json.example` and rename it to `config.json`. This new file should reside within the backend directory. It is in .gitignore, so it will not be synced to remote. Update it with the correct path to your database file and Strava tokens
- **Step 4:** Create a virtual Python 3 environment and install the required packages, e.g. by using `pip install -r requirements.txt` Skip this step if you prefer to deploy the program as a Docker container. If you deploy as Docker container, you can have a look at the script `create-container-vs2000.sh` for inspiration, but surely you need to modify it to your liking
- **Step 5:** To run the program from your terminal, instead of deploying as a Docker container, use this command from within the backed directory: `uvicorn main:app --log-config uvicorn_log_config.ini` Make sure that you actviate the newly created python 3 environment in advance
- **Step 6:** On startup the program will call Stravas APIs and get the last 200 rides and related bikes, but since this is the first time you run the program, you need to manually fetch all ride data and all bikes. This is done by navigating to the `CONFIG` tab and click the button `Get all rides`
- **Step 7:** You are all set and can now register your first components. The rest will hopefully be self explanatory. Reach out if you have any comments or questions, and create issues for bug reports and feature requests as needed
---

**Whether you are part of the pilot group or not, join the work, either by forking the repo and contribute with PRs or simply by submitting <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issues</a> 🙋 Please prefix suggestions for improvements with FEATURE REUQEST. We will review them and remove the prefix when decided how to follow up. Bug reports should be prefixed with BUG**

## Setup and configuration
TODO

## Bugs
There are still some bugs scattered around. If you find any, please submit them as an <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issue</a>.

## Versioning and branches
Velo Supervisor 2000 uses <a href="https://semver.org/" class="text-decoration-none">Semantic Versioning Specification (SemVer)</a> as versioning scheme. Versions are expressed as tags. A Github action runs each time the repository receives a commit or a pull request is accepted, and writes the current version to `current_version.txt`. Use these commands to create new tags:
- `git tag -a vX.Y.Z -m "Version X.Y.Z"`
- `git push --tags`

As a principle, development is to be done in the dev-branch. When changes are ready for testing and quality assurance, they should be merged into the staging branch. If tests and quality assurance completes successfully, the changes shall be merged from staging branch into the master branch. Review the changes in the PR and create a new version tag, according to the SemVer scheme, before merging into master.

## Changelog
*To see whats coming in the next release, check out the [project board](https://github.com/users/xivind/projects/2/views/1). All items marked as P0 are planned for the next release.*

**Future releases**
- GUI optimized for mobile devices
- Improved initital setup and configuration
- ... and much more

**Planned for v0.4.5**  

- See the [project board](https://github.com/users/xivind/projects/2/views/1) for whats coming in this release (all items marked as P0)

**v0.4.4 (CURRENT)**  

- Rearranged tables for incidents and workplans on bike details and component pages, and made these tables more informative
- Tables for incidents and workplans on component details page are hidden when there are no records to show
- Fixed a bug that added extra line breaks in text areas of incidents and workplans

**v0.4.3**  
*THIS IS A BREAKING CHANGE AND REQUIRES CHANGES TO DATA MODEL AND DB SCHEMA. IF YOU ARE UPGRADING FROM v0.4.2 OR EARLIER, USE [PROVIDED MIGRATION SCRIPT](https://github.com/xivind/velo-supervisor-2000/blob/master/backend/db_migration.py).*

There are new features in this version that require a database migration. Use [python3](https://www.python.org/downloads/) to run the script [db_migration.py from the backend folder](https://github.com/xivind/velo-supervisor-2000/blob/master/backend/db_migration.py). The script searches the home folders of the current user to find the velo supervisor 2000 database. Remember to backup the database first.

- New feature: Workplans for bikes and components
- New feature: Incident reports for bikes and components
- Improved database migration script, with more robust approach to find databases
- Improved handling of null values in component table
- Fixed a bug that in some cases would freeze the GUI if trying to escape a modal
- Fixed a bug that caused date fields and date pickers to be out of sync

**v0.4.2**  
*THIS IS A BREAKING CHANGE AND REQUIRES CHANGES TO DATA MODEL AND DB SCHEMA. IF YOU ARE UPGRADING FROM v0.4.1 OR EARLIER, USE [PROVIDED MIGRATION SCRIPT](https://github.com/xivind/velo-supervisor-2000/blob/master/backend/db_migration.py).*

The updates in this version require a database migration. Use [python3](https://www.python.org/downloads/) to run the script [db_migration.py from the backend folder](https://github.com/xivind/velo-supervisor-2000/blob/master/backend/db_migration.py). The script will check config.json to find the database, optionally the user will be prompted by the script to enter the path manually. Remember to backup the database first.  

- Possible to define mandatory component types and max quantities for any component type. Compliance for each bike is showed on landing page and bike details page. Remember to configure mandatory components and max quantities from component type page
- Improved handling of component types with better data validation and more intuitive GUI, sorting / searching of table etc
- Improved generation of unique IDs for installation history records. Ids no longer contain any information, except the ID itself
- Improvements in date picker functionality: dates can now be entered directly without using the picker, todays date time are prefilled for new records while date time is inherited from existing records when editing, improve gui for picker
- Fixed a bug that caused estimates for next service to be too high
- Fixed a bug that prevented services to be added using date time now

**v0.4.1**

- Made it possible to add components to retired bikes and change status on components assigned to retired bikes
- Switched date picker library from Flatpickr to Tempus Dominus (enables use on mobile devices)
- Added type ahead search in component tables
- Added distance to reached lifetime or service interval (whichever is closest) to components table in bike details
- Improved sorting of component tables
- Minor GUI improvements
- Misc bugfixes

**v0.4.0**

- Installation history and service history can now be modified
- Backend for distance calculation refactored
- Improved input validation backend and frontend
- Improved GUI with less clutter and more emphasis on important information
- Moved all user interaction to modals
- More accurate calculation of page load time
- Changed logic for bike statuses to be less misleading and more intuitive
- More informative error page
- Improved backend for handling deletion of records
- Made it possible to service components that are not assigned to a bike
- Made it possible to register components without adding them to bike
- Misc bugfixes

**v0.3.1**

- Fixed bug that prevented Strava activities to be saved properly
- Preliminary onboarding instructions for pilot users
- Minor GUI improvements

**v0.3.0**

- Configured program to run in Docker
- Improved logic for versioning  
- Feedback to user from business logic
- Improved input validation and user interaction
- Refactored backend and improved business logic
- Refactored frontend and introduced base template

**v0.2.0**

- Improved error handling and more informative error page
- Display banner if last pull from Strava hasnt happened in a while
- Misc bugfixes and minor improvements

**v0.1.0**

- Running version of program (bugs are present)
- Code updated to work with FastAPI 0.115.0
