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

def clean_exit(comment):
	issue.create_comment(comment)
	issue.edit(state="closed")
	sys.exit()

if issue.user.login == "paramt" and issue.get_labels()[0].name == "update redirects":
	os.system("git config --local user.email 'action@github.com'")
	os.system("git config --local user.name 'GitHub Action'")

	if issue.title == "Add URL":
		try:
			short = issue.body.split("-->")[0].strip()
			long = issue.body.split("-->")[1].strip()
		except IndexError:
			clean_exit("Invalid syntax! Use \n ```\nShort URL --> Long URL\n```")

		# Make sure the short URL isn't already in use
		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()
			for line in lines:
				if line.split(",")[0] == short:
					clean_exit(f"The redirect `go.param.me/`{short}` already exists!")

		# Add the short,long URL pair to redirects.csv
		with open("redirects.csv", "a") as csv:
			csv.write(f"{short},{long}")
			csv.write("\n")

		os.system(f"git commit -m 'Add redirect: {short}' -m '#{os.environ['ISSUE']}' -a")
		clean_exit("The redirect has been added!")

	if issue.title == "Remove URL":
		removed = False

		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()

		with open("redirects.csv", "w") as csv:
			for line in lines:
				if line.split(",")[0] != issue.body.strip():
					csv.write(line)
				else:
					removed = True

		if removed:
			os.system(f"git commit -m 'Remove redirect: {issue.body}' -m '#{os.environ['ISSUE']}' -a")
			clean_exit(f"The redirect `go.param.me/{issue.body}` has been removed!")
		else:
			clean_exit(f"The redirect `go.param.me/{issue.body}` doesn't exist!")
