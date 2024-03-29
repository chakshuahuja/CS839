## Sources

### Amazon
- [CSV](https://github.com/chakshuahuja/CS839/blob/master/Stage2/Amazon/amazon_books.csv)
- [Code](https://github.com/chakshuahuja/CS839/tree/master/Stage2/Amazon)
### Barnes & Noble
- [CSV](https://github.com/chakshuahuja/CS839/blob/master/Stage2/barnesAndNoble/barnes_and_noble_books.csv)
- [Code](https://github.com/chakshuahuja/CS839/tree/master/Stage2/barnesAndNoble)

### Report
- [PDF](https://github.com/chakshuahuja/CS839/blob/master/Stage2/report.pdf)

Setup:

Make sure you have `Firefox` browser installed for `selenium` to run and have `geckodriver` installed (In case you need do, `brew install geckodriver`).

Install the requirements mentioned in requirements.txt (selenium, scrapy, scrapy-rotating-proxies) or if you have pip setup, you may do pip install --user -r requirements.txt

Make sure you have python 3 setup

To run Amazon crawler,

./amazon.sh

A CSV file named <b>amazon_books.csv</b> will be formed in the amazon sub-directory.

To run Barnes&Noble crawler,

./barnesAndNoble.sh

A CSV file named <b>barnesAndNoble.csv</b> will be created in the barnesAndNoble sub-directory.

If most of the proxies are dead, you can use more proxies from <a href="https://www.us-proxy.org/">here</a> and add them to <b>ROTATING_PROXY_LIST</b> option in barnesAndNoble/barnesAndNoble/settings.py

