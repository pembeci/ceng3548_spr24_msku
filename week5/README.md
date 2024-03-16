## WEEK 5

### Commands used in lecture:

* For installing Scrapy and other libraries `poetry` is not required. You can use `pip`, `conda` or any other python package manager as well. 

* If you want to try poetry though, here are the steps you need:
    - [Install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) using the __offical__ installer.
    - Repo already contains `pyproject.toml` file so you can just use `poetry install` to create your virtual environment and install the dependency modules. 
    - Use `poetry shell` to activate the virtual environment so that further scrapy command line commands work. 

### What you missed if you weren't in class:

* By following the scrapy tutorial, we started scraping some Euroleague data. We started with some player stats from player pages.
* Then we learnt instead of hardcoding player page urls how we can scrap team pages to extract player page urls and then scrap those.
* In the team page, we were forced to use using regular expressions instead of CSS selectors since links were inside page script tags.  
* If you didn't use regular expressions before you can find a lot of resources for Python's `re` module or for the concept in general. 
* I used [this page](https://realpython.com/regex-python/) during the course and suggest this re tutorial and in general the site for learning Python and its modules further.

### Preparation for next week:

* Try to scrap more player stats from player pages. 
* Instead of hardcoding the team page urls as it is now, try to find and implement how we can scrap those too.

### Other notes:

* We'll talk about the term project more and decide on dates this week.


