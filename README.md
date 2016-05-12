# Pockyll

Automated linkpost updates using pocket, IFTTT and Wordpress 
finally started feeling like death sticks.

> "You wanna buy some death sticks?"<br>
> "You don't want to sell me death sticks."<br>
> "I don't wanna sell you death sticks."<br>
> "You want to go home an rethink your life."<br>
> "I want to  go home and rethink my life."<br>
> - Elan Sleazebaggano & Obi-Wan Kenobi

Pockyll is a python tool to create [Jekyll][j] linkposts from your
[pocket][pocket] collections.

## Features

* Pocket item syncing that converts your saved & tagged pocket items
  into linkposts wich merge seamlessly with standard Jekyll posts
* Linkpost management fully compatible with tools like e.g.
  [octopress][octopress]
* Incremental update support
* Tag-specific syncing
* Pocket OAuth authentication

## Installation 

```bash
$ pip install pockyll
```

## Pockyll setup

1. Login into [pocket][pocket_login], [create a new
  application][pocket_newapp] that has *retrieve* permissions.
2. Switch into your Jekyll site directory
3. `pockyll init` to generate a dummy config file `_pockyll.yml`
4. In `_pockyll.yml` enter the `pocket_consumer_key` created in step 1. 
   Edit other fields as required.
5. `pockyll auth` (will open a browser window and ask for pocket authentication)

## Site setup

By default, pockyll will give linkposts the type `reference` and include the 
target link in the `ref` variable inside the YAML post header:

	---
	title: "Clojure, The Good Parts"
	date: 2016-04-19T23:05:26
	type: "reference"
	ref: https://rasterize.io/blog/clojure-the-good-parts.html
	---

This allows us to treat normal and linkpost URLs differently, depending on
the type of the post:

```html
<div id="home">
  <ul id="blog-posts" class="posts fa-ul">
    {% for post in site.posts %}
      {% if post.type == "reference" %}
      <li><i class="fa-li fa fa-bookmark-o"></i>
          <a href="{{ post.ref }}">{{ post.title }}</a>
          <span>{{ post.date | date_to_string }}</span></li>
      {% else %}
      <li><i class="fa-li fa fa-pencil-square"></i>
          <a href="{{ post.url }}">{{ post.title }}</a>
          <span>{{ post.date | date_to_string }}</span></li>
      {% endif %}
    {% endfor %}
  </ul>
</div>
```

For normal posts, the `href` in `index.html` points to `post.url`. If the post is a linkpost, we let the `href` point to `post.ref` to enable direct external links.

## Usage

Once you have your site configured, it is time to sync the items.

1. `pockyll sync` (one-way sync of all new posts tagged with any 
   of `pocket_sync_tags`)
2. `jekyll build`
3. Optional: `jekyll serve` and marvel at the linkposts on your local server at
   <http://localhost:4000>.

## Examples

```
mk@kowalski:~/src/mysite$ pockyll sync
Requesting new items from Pocket API...
Syncing 164 items.
FIXME: ['FIXME', u'http://insighthealthdata.com/blog/HealthyBeats/index.html', u'1227075798']
FIXME: ['FIXME', u'http://ahmetalpbalkan.com/blog/8-months-microsoft/', u'374320379']
FIXME: ['FIXME', None, u'0']
Skipping: ['FIXME', None, u'0']
FIXME: ['FIXME', u'https://www.linkedin.com/pulse/agile-dead-matthew-kern', u'1264106151']
FIXME: ['FIXME', u'http://pjreddie.com/darknet/', u'1152066420']
FIXME: ['FIXME', u'https://www.chrisstucchio.com/blog/2013/bayesian_bandit.html', u'393364879']
Done (skipped 1).
mk@kowalski:~/src/mysite$
```

This is an example of an initial sync of a jekyll site against pocket (hence
the number of items).  Pockyll automatically 'fixes' missing titles but skips
items that lack a URI or an ID. I would now change into the `linkpost_dir`,
grep all files for the `title: "FIXME"` string and start editing, e.g.:

        vim `grep -l 'title: "FIXME"' *`


## Customization

Pockyll is configured using a `_pockyll.yml` configuration file located in
your Jekyll base directory. After successful OAuth authentication, the file
contains your secret Pocket access token. Hence, please make sure to
*include the pockyll configuration into your `.gitignore` file!*

### Configuration file

The overall configuration file structure looks like this:

```yaml
pocket_consumer_key: ***secret***
pocket_access_token: ***secret***
pocket_redirect_uri: 'https://getpocket.com/a/'
pocket_sync_tags: ['blog']
pocket_since: 12326342
linkpost_dir: '_posts/linkposts'
```

### Options

- `pocket_consumer_key`: this is the consumer key you obtain from the
  pocket developer API.
- `pocket_access_token`: the access token. Pockyll automatically stores 
  the token in the configuration file after the first successful OAuth
  authentication event.
- `pocket_redirect_uri`: the location to which your are redirected
  after successful authentication (this can be anything).
- `pocket_sync_tags`: a list of pocket tags that should be synced to
  Jekyll.
- `pocket_since`: pocket timestamp that marks the last sync.
  Automatically updated by pockyll.
- `linkpost_dir`: the directory where linkposts should be synced
  to. Change this to e.g. `_drafts/linkposts` if you want to review changes
  before publication. In that case use 

## License

Vanilla [MIT](https://github.com/mkirchner/pockyll/blob/master/LICENSE).

## Contact
Feel free to open issues if you run into trouble or have suggestions. Pull
Requests always welcome.

[j]: http://jekyllrb.com/
[octopress]: http://octopress.org/
[pocket]: https://getpocket.com/
[pocket_login]: https://getpocket.com/login
[pocket_newapp]: https://getpocket.com/developer/apps/new
