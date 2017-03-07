Link Juicer
===========

![](https://travis-ci.org/chipbuster/link-juicer.svg?branch=master)

A Python script for extracting many (ideally all) links from a given web page, including those with dynamic JavaScript content.

# Quick Start

Install dependencies on macOS using Homebrew:

```
    brew update
    brew install phantomjs
```

Install dependencies on Ubuntu (etc.):

```
    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install nodejs
    sudo npm install phantomjs-prebuilt
```

TODO: add other linuxses

Next, install Python dependencies:

```
    pip install -r requirements.txt
```

At this point, you're ready to use the script. You need to go into the `linkjuicer` directory and edit the `juicer.py` file.
Edit the options (explanations are in the comments) above the banner that says "do not edit below this banner", then run

```
    python3 juicer.py
```

Logging info can be found the `.log` files that the juicer creates.


# For Devs

At the moment Link Juicer is a basic Python script; you'll need to set the 'url' variable before running. It launches the URL in a headless browser using Selenium WebDriver + PhantomJS, then examines every node in the DOM, including invisible ones. It first checks whether a node contains an href attribute, then clicks on the node and observes whether this action leads to a new URL. If clicking a link creates one or more new DOM nodes, the script collects any href attributes in these nodes (though it doesn't try clicking them). All URLs (and any other link attributes) are compiled in a list and printed in alphabetical order at the end of the process.

Some forks (notably chipbuster's) are using the git-flow work model. Installation and instruction are available [on their GitHub Repo](https://github.com/nvie/gitflow)
