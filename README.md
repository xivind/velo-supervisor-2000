# velo-supervisor-2000
Program to monitor bicycle service intervals
Some more text

> 🙋 Join the work, fork the repo and contribue with PRs!

## Bugs
There are currently quite a few bugs scattered around. If you find any, please submit them as an <a href="https://github.com/xivind/velo-supervisor-2000/issues" class="text-decoration-none">issue</a>.

## Branches and versioning
Velo Supervisor 2000 uses <a href="https://semver.org/" class="text-decoration-none">Semantic Versioning Specification (SemVer)</a> as versioning scheme. Versions are expressed as tags. A Github action runs each time the repository receives a commit or a pull request is accepted, and writes the current version to `current_version.txt`. Use these commands to create new tags:
- `git tag -a vX.Y.Z -m "Version X.Y.Z"`
- `git push --tags`

## Changelog

**Future releases**
- GUI optimized for mobile devices
- Incident reports
- Improved initital setup and configuration
- ... and much more

**Planned for v0.9.2**
- Banner to display more than seven days since update from Strava

**v0.2.0**
- Configured to run in Docker

**v0.1.0**
- Running version of program (bugs are present)
- Code updated to work with FastAPI 0.115.0