import os
from github import Github

print(os.environ["GITHUB_ACTIONS"])

github = Github(os.environ["TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
issue = repo.get_issue(number=int(os.environ["ISSUE"]))

if issue.title == "Add URL" and issue.user.login == "paramt":
	with open("redirects.csv", "a") as csv:
		line = issue.body.replace(" --> ", ",")
		csv.write(line)
		csv.write("\n")

	issue.create_comment("The redirect has been added!")
	issue.edit(state="closed")

if issue.title == "Remove URL" and issue.user.login == "paramt":
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
