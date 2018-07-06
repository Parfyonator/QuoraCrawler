from time import time
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver


def authentication(browser, email, password):
  """Function to log in.

  Args:
    browser: instance of webdriwer class.
    email: user's email.
    password: corresponding password.

  """
  browser.get("https://www.quora.com")
  sleep(3)
  browser.find_element_by_xpath("//input[@tabindex='1']").send_keys(email)
  sleep(1)
  browser.find_element_by_xpath("//input[@tabindex='2']").send_keys(password)
  sleep(0.5)
  browser.find_element_by_xpath("//input[@tabindex='4']").click()


def set_browser():
  """Create webdriver instance and tune some settings.

  Returns:
    Webdriver instance.

  """
  firefox_profile = webdriver.FirefoxProfile()
  firefox_profile.set_preference('permissions.default.stylesheet', 2)
  firefox_profile.set_preference('permissions.default.image', 2)
  firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
  browser = webdriver.Firefox(firefox_profile=firefox_profile)

  return browser


def question_list(browser, url):
  """Scrape list of question urls from given url.

  Args:
    browser: instance of webdriwer class
    url: url to scrape from.

  Returns:
    List of question urls.

  """
  browser.get(url)
  sleep(2)

  url_lst = []
  prev_len = None
  body = browser.find_element_by_tag_name("body")
  body.send_keys(Keys.TAB)

  while(len(url_lst) != prev_len):
    prev_len = len(url_lst)
    url_lst = browser.find_elements_by_class_name("question_link")
    body.send_keys(Keys.END)
    sleep(4)

  return [url.get_attribute('href') for url in url_lst]


def get_data(browser, url):
  """Scrape data from the question url.

  Args:
    browser: instance of webdriwer class.
    url: question url.

  Returns:
    Data as a dictionary with following keys: 'url', 'title', 'follows',
    'views', 'answers' and 'tags'.

  """
  data = dict()

  # add url to data
  data['url'] = url

  # open url
  browser.get(url)
  sleep(5)

  # get question title
  questionTitle = browser.find_elements_by_class_name("rendered_qtext")[0].text
  data['title'] = questionTitle

  # get follows count
  try:
    follows = browser.find_elements_by_class_name("icon_action_bar-count")[0].text
    data['follows'] = follows[2:]
  except:
    data['follows'] = '0'

  # get views
  try:
    views = browser.find_element_by_class_name("ViewsRow HighlightRow").text
    data['views'] = views[:-5].replace(',', '')
  except:
    data['views'] = '0'

  # get answers count
  try:
    answers = browser.find_element_by_class_name("answer_count").text
    data['answers'] = answers[:-7]
  except:
    data['answers'] = '0'

  # open more tags if present
  try:
    browser.find_element_by_xpath("//span[@class='ViewMoreLink light view_more_topics_link']").\
      find_element_by_tag_name("a").click()
    sleep(2)
  except:
    pass

  # get tags
  elements = browser.find_elements_by_css_selector("span.TopicName.TopicNameSpan")
  tags = [elem.text for elem in elements if elem.text != '']
  data['tags'] = set(tags)

  return data


def save_data(data, filename):
  """Save data to file in folder 'Results/'.

  Args:
    data: list of dictionaries created by get_data function.
    filename: name of the file.

  """
  with open('Results/' + filename, 'w') as out:
    for d in data:
      s = d['url'] + ';'
      s += d['title'] + ';'
      s += d['follows'] + ';'
      s += d['views'] + ';'
      s += d['answers'] + ';'
      s += ', '.join(d['tags']) + '\n'
      out.write(s)


if __name__ == "__main__":
  # list of tags to search for
  tags = ['SaaS-Metrics',
          'SaaS-Marketing',
          'SaaS-Sales',
          'Software-as-a-Service-2']

  wrapper = 'https://www.quora.com/topic/{}/all_questions'

  begin = time()
  browser = set_browser()
  # paste your quora account email and password here
  authentication(browser, "EmailOfQuoraAccount", "Password")

  for tag in tags:
    url_lst = question_list(browser, wrapper.format(tag))

    data = []
    for url in url_lst[:5]:
      data.append(get_data(browser, url))

    save_data(data, '{}.csv'.format(tag))

  browser.close()

  print('{:.2f}'.format((time() - begin)/3600))
