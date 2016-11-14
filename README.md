# linkedin-analyzer
Takes search results from LinkedIn and analyzes jobs before a school vs after.

Python 3.5
Additional Libraries: Beautiful Soup 4, XLWT

The initial version of this analyzes results for UXDI students at General Assembly. I also gathered LinkedIn data on GA's WDI and for HackReactor. The way this was written, it used downloaded html pages from linkedin search. I'm sure that html will be sufficiently different soon that this script doesn't work at all.

The scripts to run are:
linkedin-results-scraper1.py
to build json files from html files then
analyze1.py
to analyze the json files and output .xls files


