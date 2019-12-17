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
