# go.param.me
This repo holds the code for `go.param.me`, a URL shortener for my personal links. The whole site is static and everything is hosted by GitHub Pages.

## Redirects
All the redirect URLs are maintained in a single [CSV file](redirects.csv), which is fetched by the client-side [JavaScript](script.js) each time someone visits the site. There is no dynamic content as everything is done by the client-side. 

## GitHub Actions
In order to add more links, I can update [redirects.csv](redirects.csv). However, GitHub Actions makes it possible to automate this process. I have set up a [worksflow](.github.workflow.yml) which runs [this Python script](add_url.py) everytime a new issue is created. The script checks for 2 things:
- The issue is titled "Add URL"
- The issue is created by me

If the criteria is met, it adds the short URL and long URL pair specified in the body to the [redirects.csv](redirects.csv)
