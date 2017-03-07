Link Juicer
===========

![](https://travis-ci.org/chipbuster/link-juicer.svg?branch=master)

A Python script for extracting many (ideally all) links from a given web page, including those with dynamic JavaScript content.

Install dependencies on macOS using Homebrew:

    brew update
    brew install phantomjs

Install dependencies on Ubuntu (etc.):

    apt upgrade
    apt install nodejs-legacy npm
    sudo npm install phantomjs-prebuilt

Next, install Python dependencies:

    pip install -U pip
    pip install -U selenium lxml


At the moment Link Juicer is a basic Python script; you'll need to set the 'url' variable before running. It launches the URL in a headless browser using Selenium WebDriver + PhantomJS, then examines every node in the DOM, including invisible ones. It first checks whether a node contains an href attribute, then clicks on the node and observes whether this action leads to a new URL. If clicking a link creates one or more new DOM nodes, the script collects any href attributes in these nodes (though it doesn't try clicking them). All URLs (and any other link attributes) are compiled in a list and printed in alphabetical order at the end of the process.
