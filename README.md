# velo-supervisor-2000
Program to keep track of lifetime and service intervals of bicycle components, based on activity data from Strava.

> **Join the work, either by forking the repo and contribute with PRs or simply by submitting <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issues</a> 🙋**

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
- Configured program to run in Docker
- Improved logic for versioning 

**v0.3.0**
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