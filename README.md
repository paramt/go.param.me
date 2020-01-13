# go.param.me
> A URL shortener for my personal links.

## Redirects
All the redirect URLs are maintained in a single [CSV file](redirects.csv), which is fetched by the client-side [JavaScript](script.js) each time someone visits the site. There is no dynamic content as everything is done by the client-side.

## GitHub Actions
Redirects can be added, removed, or modified by updating [redirects.csv](redirects.csv). However, GitHub Actions makes it possible to automate this process. Creating a new issue triggers [this worksflow](.github.workflow.yml) which runs [this Python script](add_url.py). The script is set up to automatically update redirects.csv based on the issue body.

### Add URL
In order to add a redirect, the issue must be created by me, be titled "Add URL", and have the <kbd>update redirects</kbd> label. The issue body needs to be:

```
Short URL --> Long URL
```

### Remove URL
In order to remove a redirect, the issue must be created by me, be titled "Remove URL", and have the <kbd>update redirects</kbd> label. The issue body should contain the short URL to remove.

## Modify
If you'd like to create your own URL shortener, fork this repo, modify [config.js](config.js), the meta redirect in [index.html](index.html), and the domain name in [CNAME](CNAME).

### `config.js`
| Option | Description | Type | Example |
| --- | --- | --- | --- |
| `shortDomain` | The short domain that will redirect to other URLs | str | `go.param.me` |
| `defaultRedirect` | The default redirect in case a link that does not exist is requested | str | `https://www.param.me` |
| `repo` | The GitHub repo where `redirects.csv` is located | str | `paramt/go.param.me` |
| `user` | The GitHub user that is allowed to modify the list of redirects by opening an issue | str | `paramt` |
| `netlify_redirects` | Whether or not the script should generate a `_redirects` file (used by Netlify's server-side redirects) | bool | `true` |

## License
The repo is licensed under the [MIT License](LICENSE), so you may use and modify the code in any way as long as the copyright and license notices are kept.
