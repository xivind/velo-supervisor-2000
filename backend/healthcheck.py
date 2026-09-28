#!/usr/bin/env python3
"""Health check run by the Docker daemon, exit code 0 means healthy and 1 means unhealthy. Prints the response,
since Docker stores the output and Portainer shows it as the reason for the health status"""

import sys
import urllib.error
import urllib.request

HEALTH_URL = "http://127.0.0.1:8000/health"

try:
    with urllib.request.urlopen(HEALTH_URL, timeout=4) as response:
        print(response.read().decode())
    sys.exit(0)

except urllib.error.HTTPError as error:
    print(error.read().decode())
    sys.exit(1)

except Exception as error:
    print(f"Health endpoint not reachable: {error}")
    sys.exit(1)
