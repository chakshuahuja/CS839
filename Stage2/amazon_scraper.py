from selenium import webdriver
import time
import csv

class AmazonScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.books = {}
        self.write_header_to_csv()

    def extract_first_page_books(self):
        curr_count = len(self.books)
        counter = 0
        for book in self.driver.find_elements_by_xpath("//div[@id='mainResults']/ul/li"):
            header = book.find_element_by_class_name("s-color-twister-title-link")
            title = header.get_attribute("title")
            link = header.get_attribute("href").split('ref=')[0]
            author = [t.text for t in book.find_elements_by_class_name("a-spacing-none")][2].lstrip("by ")

            # Not extract and add duplicate books belonging to different categories
            if link in self.books: continue

            self.books[link] = {
                "counter": counter + curr_count,
                "link": link,
                "title": title,
                "author": author
            }
            counter += 1
    
    def extract_next_page_books(self):
        curr_count = len(self.books)
        counter = 0
        for book in self.driver.find_elements_by_class_name("s-result-item"):
            header = book.find_elements_by_class_name("sg-row")[1]
            title = header.find_element_by_class_name("a-color-base").text
            link = header.find_element_by_class_name("a-link-normal").get_attribute("href").split('ref=')[0]
            author = header.find_element_by_class_name("a-color-secondary").text.split("|")[0].lstrip("by ")

            # Not extract and add duplicate books belonging to different categories
            if link in self.books: continue

            self.books[link] = {
                "counter": counter + curr_count,
                "link": link,
                "title": title,
                "author": author
            }
            counter += 1
   
    def get_books_data(self, till_page=3):
        categroy_ids = {
            'History' : '9',
            'Mystery' : '18',
            'Literary' : '17'
        }

        for topic in categroy_ids:
            categroy_id = categroy_ids[topic]
            print('Extracting books from Topic ', topic, ' from ', categroy_id)
            page_number = 1
            print('First Page URL')
            print('https://www.amazon.com/s?rh=n%3A283155%2Cn%3A!1000%2Cn%3A' + categroy_id +'&page=' + str(page_number) + '&qid=1554049001')
            print()
            while page_number < till_page:
                try:
                    page_url = 'https://www.amazon.com/s?rh=n%3A283155%2Cn%3A!1000%2Cn%3A'+ categroy_id + '&page=' + str(page_number) + '&qid='
                    self.driver.get(page_url)
                    self.driver.implicitly_wait(5)
                    print('Extracting books from Page ', page_number)
                    if page_number == 1: self.extract_first_page_books()
                    else: self.extract_next_page_books()
                    print(len(self.books), 'books extracted successfully till now.')
                    page_number += 1
                except:
                    self.driver.quit()
        
    def get_books_additional_data(self):

        for book in self.books:
            print('Extracting from book '+ str(self.books[book]['counter']) + ': ', self.books[book]['title'])
            self.driver.get(book)
            self.driver.implicitly_wait(5)
            details = self.driver.find_element_by_xpath("//table[@id='productDetailsTable']")

            for detail in details.text.split('\n'):
                if ':' in detail:
                    k, v = detail.split(':', 1)
                    if k == "Average Customer Review": continue
                    self.books[book][k.strip()] = v.strip()

            # Write to CSV with pre-filled for missing fields
            kv = self.defaults.copy()
            kv.update(self.books[book])
            with open('amazon_books.csv', mode='a') as csv_file:
                self.writer = csv.DictWriter(csv_file, fieldnames=self.field_names, extrasaction='ignore')
                self.writer.writerow(kv)


    def write_header_to_csv(self):
        self.field_names = ['counter', 'title', 'author', 'link', 'Hardcover', 'Paperback', 'Publisher', 'Language', 'ISBN-10', 'ISBN-13', 'Product Dimensions', 'Shipping Weight', 'Amazon Best Sellers Rank', 'ASIN']
        self.defaults = {k:'N/A' for k in self.field_names}

        with open('amazon_books.csv', mode='w') as csv_file:
            self.writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
            self.writer.writeheader()

    def write_to_csv(self):
        with open('amazon_books.csv', mode='w') as csv_file:
            field_names = ['title', 'author', 'link']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for b in self.books:
                writer.writerow(self.books[b])

    def __del__(self):
        self.driver.quit()

AS = AmazonScraper()
AS.get_books_data(3)
# AS.write_to_csv()
AS.get_books_additional_data()
