# velo-supervisor-2000
Program to monitor bicycle service intervals

Join the work, fork the repo and contribue with PRs!

Known limitations:
Rides deleted from Strava are not deleted in velo supervisor upon sync
Data validation happens frontend, so if you use only APIs make your own validation rules
Offset is to be set manually to adjust for distance not registered
Component type must be defined in order to prefill component details to work for component type


Use semver for tagging. For exmaple: git tag -a v0.8 -m "Version 0.8"
Remember to push tags to repo: git push --tags


Changelog - fix layout
1.0.x
Banner to display more than seven days since update from Strava

0.9.x
Version now runs as Github action
Configured to run in Docker
Updated code to work with FastAPI 0.115.0
Alphabetical sorting of component types in tables and drop downs
Getting data from Strava in the background
Configuration page
Improved component detail page (added back button and delete button)
Bugfixes

0.8.x
Introduced versioning
Working program, with some bugs

