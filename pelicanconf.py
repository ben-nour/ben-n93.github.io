AUTHOR = "Ben Nour"
SITENAME = "Ben Nour"
SITEURL = "https://ben-nour.com"
SITETITLE = "Ben Nour"

PATH = "content"
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "extra/favicon.ico": {"path": "favicon.ico"},
}

PLUGINS = ["sitemap", "seo"]
TIMEZONE = "Australia/Sydney"
DEFAULT_LANG = "en"
DELETE_OUTPUT_DIRECTORY = True

# FAVICON = './content/images/ben_favicon.jpg'

# Articles
ARTICLE_PATHS = [
    "blog",
]
ARTICLE_URL = "blog/{slug}.html"
ARTICLE_SAVE_AS = "blog/{slug}.html"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# SEO
SEO_REPORT = True 
SEO_ENHANCER = True
SEO_ENHANCER_OPEN_GRAPH = False 
SEO_ENHANCER_TWITTER_CARDS = False

# Blogroll
LINKS = (("blog", "https://ben-nour.com/category/blog.html"),)

# Social widget
SOCIAL = (
    ("github", "https://github.com/ben-nour"),
    ("twitter", "https://twitter.com/benjamin_nour"),
)

# Theme.
THEME = "/Users/benjaminnour/Documents/Pelican Themes/Peli-Kiera"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


# Misc.
DEFAULT_PAGINATION = 10
DISQUS_SITENAME = "ben-nour"