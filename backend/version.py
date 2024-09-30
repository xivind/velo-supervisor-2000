#!/usr/bin/env python3
"""Script to maintain version number"""

import subprocess

def get_git_version():
    """Function to get latest version number"""
    try:
        # Get the latest tag
        version = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()

    except subprocess.CalledProcessError:
        # If no tags are found, use a default version
        version = "0.0.0"

    return version

# Write version to a file
with open('backend/current_version.txt', 'w', encoding='utf-8') as file:
    file.write(get_git_version())

print(f"Current version: {get_git_version()}")
