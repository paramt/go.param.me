import os
from github import Github

github = Github(os.environ["GITHUB_TOKEN"])
repo = github.get_repo(os.environ["GITHUB_REPOSITORY"])
open_issues = repo.get_issues(state="open")

for issue in open_issues:
	if issue.title == "Add URL" and issue.user.login == "paramt":
		issue.body = "test --> https://www.param.me/test"
		with open("redirects.csv", "a") as csv:
			line = issue.body.replace(" --> ", ",")
			csv.write(line)
			csv.write("\n")

		issue.create_comment("The redirect has been added! Please allow up to 5 minutes for the changes to take place.")
		issue.edit(state="closed")
