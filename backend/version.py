#!/usr/bin/env python3
"""Script to maintain version number"""

import subprocess

def get_git_info():
    """Function to get latest version number and commit hash"""
    try:
        # Get the latest tag
        version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
        
        # Get the latest commit hash (shortened)
        commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()
        
        # Combine version and hash
        full_version = f"{version}.{commit_hash}"

    except subprocess.CalledProcessError:
        # If no tags are found or not in a git repository, use a default version
        full_version = "0.0.0.unknown"

    return full_version

# Write version to a file
with open('backend/current_version.txt', 'w', encoding='utf-8') as file:
    file.write(get_git_info())

print(f"Current version: {get_git_info()}")
