'''
This script runs each time a new issue is created in the repo.
The script is triggered by this GitHub Action: /.github/workflows/main.yml
'''

import json
import os
import sys
from github import Github

# Set config variables from config.js
with open("config.js", "r") as js:
	config = js.read()[13:]
	config = json.loads(config)
	SHORT_DOMAIN = config["shortDomain"] # To construct issue comments
	GH_USERS = config["users"] # To filter new issues
	NETLIFY = config["netlify_redirects"] # Whether or not to update the _redirects file

# Get the issue that triggered the script
github = Github(os.environ["TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
issue = repo.get_issue(number=int(os.environ["ISSUE"]))

# Close and comment on issue, then exit script
def clean_exit(comment):
	issue.create_comment(comment)
	issue.edit(state="closed")
	sys.exit()

# Add redirect to _redirects
def add_netlify_redirects(short, long):
	with open("_redirects", "a") as redirects:
		redirects.write(f"/{short} {long}")
		redirects.write("\n")

# Remove redirect from _redirects
def remove_netlify_redirects(url):
	with open("_redirects", "r") as redirects:
		lines = redirects.readlines()

	with open("_redirects", "w") as redirects:
		# Empty file and write each line again except for the line to remove
		for line in lines:
			if line.split(" ")[0][1:] != url:
				redirects.write(line)

# Check whether issue is opened by an authorized user
authorized = issue.user.login in GH_USERS

if authorized and issue.get_labels()[0].name == "update redirects":
	os.system("git config --local user.email 'action@github.com'")
	os.system("git config --local user.name 'GitHub Actions'")

	if issue.title == "Add URL":
		# Use the first line of the issue body
		body = issue.body.split("\n")[0]

		try:
			short = body.split("-->")[0].strip()
			long = body.split("-->")[1].strip()
		except IndexError:
			clean_exit("Invalid syntax! Use \n ```\nShort URL --> Long URL\n```")

		# Make sure the short URL isn't already in use
		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()
			for line in lines:
				if line.split(",")[0] == short:
					clean_exit(f"The redirect `{SHORT_DOMAIN}/`{short}` already exists!")

		# Add the short,long URL pair to redirects.csv
		with open("redirects.csv", "a") as csv:
			csv.write(f"{short},{long}")
			csv.write("\n")

		if NETLIFY: add_netlify_redirects(short, long)

		os.system(f"git commit -m 'Add redirect: {short}' -m '#{os.environ['ISSUE']}' -a")
		clean_exit("The redirect has been added!")

	if issue.title == "Remove URL":
		body = issue.body.split("\n")[0].strip()
		removed = False

		with open("redirects.csv", "r") as csv:
			lines = csv.readlines()

		with open("redirects.csv", "w") as csv:
			# Empty file and write each line again except for the line to remove
			for line in lines:
				if line.split(",")[0] != body:
					csv.write(line)
				else:
					# Remove redirect from _redirects too
					remove_netlify_redirects(body)
					removed = True

		if removed:
			os.system(f"git commit -m 'Remove redirect: {body}' -m '#{os.environ['ISSUE']}' -a")
			clean_exit(f"The redirect `{SHORT_DOMAIN}/{body}` has been removed!")
		else:
			clean_exit(f"The redirect `{SHORT_DOMAIN}/{body}` doesn't exist!")
