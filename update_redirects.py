'''
This script runs each time a new issue is created in the repo.
The script is triggered by this GitHub Action: /.github/workflows/main.yml
'''

import os
import sys
from github import Github

# Get the issue that triggered the script
github = Github(os.environ["TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
issue = repo.get_issue(number=int(os.environ["ISSUE"]))

if issue.user.login == "paramt" and issue.get_labels()[0].name == "update redirects":
	if issue.title == "Add URL":
		short = issue.body.split(" --> ")[0]
		long = issue.body.split(" --> ")[1]

		# Make sure the short URL isn't already in use
		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()
			for line in lines:
				if line.split(",")[0] == short:
					issue.create_comment(f"The redirect go.param.me/`{short}` already exists!")
					issue.edit(state="closed")
					sys.exit()

		# Add the short,long URL pair to redirects.csv
		with open("redirects.csv", "a") as csv:
			csv.write(f"{short},{long}")
			csv.write("\n")

		issue.create_comment("The redirect has been added!")
		issue.edit(state="closed")

	if issue.title == "Remove URL":
		removed = False

		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()

		with open("redirects.csv", "w") as csv:
			for line in lines:
				if line.split(",")[0] != issue.body:
					csv.write(line)
				else:
					removed = True

		if removed:
			issue.create_comment(f"The redirect `go.param.me/{issue.body}` has been removed!")
		else:
			issue.create_comment(f"The redirect `go.param.me/{issue.body}` doesn't exist!")
		issue.edit(state="closed")
