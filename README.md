# velo-supervisor-2000
Velo Supervisor 2000 is a program to keep track of lifetime and service intervals of bicycle components, based on activity data from Strava.

---
**📡 IMPORTANT INFORMATION TO USERS PARTICIPARTING IN PILOTING Q1 2025**

🔴 There are currently some major limitations in this software, most notably that installation records and service records cannot be changed once they are created. Please take this into consideration if you are piloting. We are working on fixing this. See the [project board](https://github.com/users/xivind/projects/2/views/1) for a complete list of issues

The onboarding procedure is not ready yet, but you can start piloting already now by setting up Velo Supervisor 2000 manually. Complete the following steps:
- **Step 1:** Copy the file `backend/template_db.sqlite` and place it somewhere outside the repo
- **Step 2:** Copy the file `backend/strava_tokens.example.json` and place it somewhere outside the repo. You should rename the file as well, e.g. to `strava_tokens.json`. Modify it with your own data and dont share it with anyone else. [See this tutorial](https://developers.strava.com/docs/getting-started/) on how to obtain the oauth-data from Strava
- **Step 3:** Make a copy of `backend/config.json.example` and rename it to `config.json`. This new file should reside within the backend directory. It is in .gitignore, so it will not be synced to remote. Update it with the correct path to your database file and Strava tokens
- **Step 4:** Create a virtual Python 3 environment and install the required packages, e.g. by using `pip install -r requirements.txt` Skip this step if you prefer to deploy the program as a Docker container. If you deploy as Docker container, you can have a look at the script `create-container-vs2000.sh` for inspiration, but surely you need to modify it to your liking
- **Step 5:** To run the program from your terminal, instead of deploying as a Docker container, use this command from within the backed directory: `uvicorn main:app --log-config uvicorn_log_config.ini` Make sure that you actviate the newly created python 3 environment in advance
- **Step 6:** On startup the program will call Stravas APIs and get the last 200 rides abd related bikes, but since this is the first time you run the program, you need to manually fetch all ride data and all bikes. This is done by navigating to the `CONFIG` tab and click the button `Get all rides`
- **Step 7:** You are all set and can now register your first components. The rest will hopefully be self explanatory. Reach out if you have any comments or questions, and create issues for bug reports and feature requests as needed
---

**Whether you are part of the pilot group or not, join the work, either by forking the repo and contribute with PRs or simply by submitting <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issues</a> 🙋**

## Setup and configuration
TODO

## Bugs
There are currently quite a few bugs scattered around. If you find any, please submit them as an <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issue</a>.

## Versioning and branches
Velo Supervisor 2000 uses <a href="https://semver.org/" class="text-decoration-none">Semantic Versioning Specification (SemVer)</a> as versioning scheme. Versions are expressed as tags. A Github action runs each time the repository receives a commit or a pull request is accepted, and writes the current version to `current_version.txt`. Use these commands to create new tags:
- `git tag -a vX.Y.Z -m "Version X.Y.Z"`
- `git push --tags`

As a principle, development is to be done in dev-branches and will be merged into the master branch as needed. Review the changes in the PR and create a new version tag accordingly before merging.

## Changelog

**Future releases**
- GUI optimized for mobile devices
- Incident reports
- Improved initital setup and configuration
- ... and much more

**Planned for v0.4.0**
- ...

**Planned for v0.3.1**
- Bugfixes
- Preliminary onboarding instructions for pilot users
- ...

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
