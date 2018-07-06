# QuoraCrawler
Crawler to scrape question information on given list of tags. It needs quora email and password to log in.
To run `crawler.py` you need Python version 3.5 or higher. This crawler uses *Selenium* so you it also should be installed. It can be made via pip: `pip install selenium` on your command line. Type `python crawler.py` to run crawler.
The results can be found in directory `Results`. Each filename corresponds to a question tag. The crawler saves question url, title, number of follows, number of views, number of answers and tags assigned to the question.
