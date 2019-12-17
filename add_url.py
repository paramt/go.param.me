import os
from github import Github

print(os.environ["GITHUB_ACTIONS"])

github = Github(os.environ["TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
issue = repo.get_issue(number=os.environ["ISSUE"])

if issue.title == "Add URL" and issue.user.login == "paramt":
	with open("redirects.csv", "a") as csv:
		line = issue.body.replace(" --> ", ",")
		csv.write(line)
		csv.write("\n")

	issue.create_comment("The redirect has been added!")
	issue.edit(state="closed")

if issue.title == "Remove URL" and issue.user.login == "paramt":
	with open("redirects.csv", "r") as csv:
		lines = csv.readlines()

	with open("redirects.csv", "w") as csv:
		for line in csv:
			if line.split(",")[0] != issue.body:
				csv.write(line)

	issue.create_comment("The redirect has been removed!")
	issue.edit(state="closed")
