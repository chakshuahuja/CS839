from selenium import webdriver
import time
import csv

class AmazonScraper:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.books = {}

    def extract_first_page_books(self):
        for book in self.driver.find_elements_by_xpath("//div[@id='mainResults']/ul/li"):
            header = book.find_element_by_class_name("s-color-twister-title-link")
            title = header.get_attribute("title")
            link = header.get_attribute("href")
            author = [t.text for t in book.find_elements_by_class_name("a-spacing-none")][2].lstrip("by ")
            self.books[link] = {
                "link": link,
                "title": title,
                "author": author
            }
    
    def extract_next_page_books(self):
        for book in self.driver.find_elements_by_class_name("s-result-item"):
            header = book.find_elements_by_class_name("sg-row")[1]
            title = header.find_element_by_class_name("a-color-base").text
            link = header.find_element_by_class_name("a-link-normal").get_attribute("href")
            author = header.find_element_by_class_name("a-color-secondary").text.split("|")[0].lstrip("by ")
            self.books[link] = {
                "link": link,
                "title": title,
                "author": author
            }
   
    def get_books_data(self, till_page=3):
        page_number = 1
        while page_number < till_page:
            try:
                page_url = "https://www.amazon.com/s/ref=lp_1_pg_2/146-0611166-7984053?rh=n%3A283155%2Cn%3A%211000%2Cn%3A1&page=" + str(page_number) + "&ie=UTF8&qid=1553406119"
                self.driver.get(page_url)
                self.driver.implicitly_wait(5)
                print('Extracting books from Page ', page_number)
                if page_number == 1: self.extract_first_page_books()
                else: self.extract_next_page_books()
                print(len(self.books), 'books extracted successfully till now.')
                page_number += 1
            except:
                self.driver.quit()
        
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
AS.get_books_data(5)
AS.write_to_csv()
