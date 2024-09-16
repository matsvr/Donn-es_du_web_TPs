import json
import os

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

site_title = None
# TODO: When you come to create your API, there will be a small line of code to add here!

# Step 1: Web Scraping with BeautifulSoup


def get_page(url: str) -> str:
    """
    Return the HTML content of the page at the given URL.
    :param str url: The URL of the page to scrape.
    :return: The HTML content of the page.
    :raises requests.HTTPError: If the request to the URL returns an error."""
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except requests.HTTPError as e:
        raise e


def get_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the page from the BeautifulSoup object.
    :param BeautifulSoup soup: The BeautifulSoup object representing the parsed HTML page.
    :return: The title of the page.
    """
    title = soup.find(
        'h1').string  # from stackoverflow "https://stackoverflow.com/questions/35956045/extract-title-with-beautifulsoup"
    if title:
        return title


def get_book_info(soup: BeautifulSoup) -> dict[str, str, str, int, str]:
    """
    Extract information about a book from the BeautifulSoup object: ucp, title, price, rating, and description.
    :param BeautifulSoup soup: The BeautifulSoup object representing the parsed HTML page of a book.
    :return: A dictionary containing the extracted information about the book.
    """

    dic = {}
    tableau = soup.find("table", class_="table table-striped")
    if tableau:
        upc = tableau.find('td')
    dic["ucp"] = upc.string if upc else "None"

    bloc1 = soup.find("div", class_="col-sm-6 product_main")
    if bloc1:
        title = bloc1.find('h1')

    price = soup.find("p", class_="price_color")

    dic["title"] = title.string if title else "None"
    dic["price"] = price.string if price else "None"

    rating1 = soup.find('p', class_='star-rating One')
    if rating1 is not None:
        dic["rating"] = 1
    rating2 = soup.find('p', class_='star-rating Two')
    if rating2 is not None:
        dic["rating"] = 2
    rating3 = soup.find('p', class_='star-rating Three')
    if rating3 is not None:
        dic["rating"] = 3
    rating4 = soup.find('p', class_='star-rating Four')
    if rating4 is not None:
        dic["rating"] = 4
    rating5 = soup.find('p', class_='star-rating Five')
    if rating5 is not None:
        dic["rating"] = 5

    bloc2 = soup.find('article', class_='product_page')
    if bloc2:
        descr = bloc2.find('p', class_="")

    dic["description"] = descr.string if descr else "None"

    return dic


def get_books_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    """
    Extract the links to the books from the BeautifulSoup object.
    :param BeautifulSoup soup: The BeautifulSoup object representing the parsed HTML page.
    :param str base_url: The base URL of the website.
    :return: A list of URLs to the books."""
    links_list = []
    current_page = soup
    base_url = base_url+"catalogue/"
    current_url = base_url+"catalogue/page-1.html"

    while current_page is not None:
        bloc_livres = current_page.find('ol', class_='row')
        for link in bloc_livres.find_all('a')[::2]:
            href = link.get('href')
            if href and href.startswith('catalogue/'):
                links_list.append(base_url + href)

        next_page = current_page.find('li', class_='next')
        if next_page:
            next_page_url = base_url + next_page.a.get('href')
            current_page = BeautifulSoup(
                get_page(next_page_url), 'html.parser')
            current_url = next_page_url

        else:
            current_page = None

    return links_list


def get_books() -> tuple[str, list[dict[str, str, str, int, str]]]:
    """
    Scrape the books from the website and return the site title and a list of dictionaries containing the book information.
    :return: A tuple containing the site title and a list of dictionaries with the book information.
    """

    base_url = "https://books.toscrape.com/"
    url = base_url + "catalogue/page-1.html"
    page = get_page(url)
    soup = BeautifulSoup(page, 'html.parser')
    site_title = get_title(soup)
    links = get_books_links(soup, base_url)

    list_books = []
    for link in links:
        page = get_page(link)
        soup = BeautifulSoup(page, 'html.parser')
        book_info = get_book_info(soup)
        list_books.append(book_info)

    return (site_title, list_books)


# Step 2: Data handling with Pydantic and JSON
class Book(BaseModel):
    ucp: str
    title: str
    price: str
    rating: int
    description: str

# TODO: uncomment the following 4 functions AFTER implementing the Book class


def json_to_book(book_dict: dict[str, str, str, int, str]) -> Book:
    """
    Convert a dictionary to a Book instance.
    :param dict[str, str, str, int, str] book_dict: A dictionary containing the book information.
    :return: A Book instance created from the dictionary."""
    book = Book(ucp=book_dict[0], title=book_dict[1], price=book_dict[2],
                rating=book_dict[3], description=book_dict[4])
    return book


def book_to_json(book: Book) -> dict[str, str, str, int, str]:
    """
    Convert a Book instance to a dictionary.
    :param Book book: A Book instance.
    :return: A dictionary containing the book information."""
    return book.dict()


def save_books(site_title: str, books: list[Book]) -> None:
    """
    Save the list of books to a JSON file.
    :param str site_title: The title of the website.
    :param list[Book] books: The list of books to save.
    """
    pass


def load_books(site_title: str) -> list[Book]:
    """
    Load the list of books from a JSON file.
    :param str site_title: The title of the website.
    :return: The list of books loaded from the JSON file."""
    pass


# Step 3: API creation with FastAPI

# TODO: write here the 4 API endpoints with FastAPI here
# Main function to run the server (if needed outside the command line)
if __name__ == "__main__":
    # TODO: you can add your code below to test your application
    pass  # TODO: to be removed with your code

    # TODO: uncomment the following lines as you progress in the implementation. At the end of the lab, the code below should be uncommented and work entirely.
    # site_title, book_dict_list = get_books()
    # if book_dict_list is not None:
    #     books = [json_to_book(book_dict) for book_dict in book_dict_list]
    #     save_books(site_title, books)
    # import uvicorn

    # uvicorn.run(app, host="127.0.0.1", port=8000)
