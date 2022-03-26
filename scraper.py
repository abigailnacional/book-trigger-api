'''This file includes functions that scrape the Book Trigger Warnings site.'''

import requests
from bs4 import BeautifulSoup
from appmodels.models import Book
import uuid

'''This function scrapes one Wiki article and returns a Book object.'''
def scrapeWikiArticle(url) -> Book:
    response = requests.get(
        url=url,
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    #Make ID for this book
    bookID = uuid.uuid4()

    #Get title, save as bookTitle
    longTitle = soup.find(id="firstHeading")
    splitTitle = longTitle.text.split(' by ')
    bookTitle = splitTitle[0]

    #Get authors, save as bookAuthors with authors split by commas
    authorLabel = soup.find(string="Author(s)")
    authorList = authorLabel.parent.find_next_sibling("td").contents
    #Count number of items in authorList. If there are two authors, the list will have 3 items; for example: ['Mom', <br/>, 'Dad']
    authorCount = 0
    for a in authorList:
        authorCount += 1
    #Get actual authors only. Initialize bookAuthors variable
    bookAuthors = ""
    #If there's only 1 author, just make that the bookAuthor
    if authorCount == 1:
        bookAuthors = authorList[0]
    else:
        #If there are many authors, you have to save them in 1 string
        for authorNum in range(authorCount):
            #Don't save the <br> entries
            if (authorNum % 2) == 0:
                bookAuthors = bookAuthors + authorList[authorNum] + ", "

    #Get genre(s), save as bookGenres with genres split by commas
    genreLabel = soup.find(string="Genre(s)")
    genreList = genreLabel.parent.find_next_sibling("td").contents
    #Count number of items in genreList. If there are two genres, the list will have 3 items; for example: ['Fantasy', <br/>, 'Romance']
    genreCount = 0
    for g in genreList:
        genreCount += 1
    #Get actual genres only. Initialize bookGenres variable
    bookGenres = ""
    #If there's only 1 genre, just make that the bookGenre
    if genreCount == 1:
        bookGenres = genreList[0]
    else:
        #If there are many genres, you have to save them in 1 string
        for genreNum in range(genreCount):
            #Don't save the <br> entries
            if (genreNum % 2) == 0:
                bookGenres = bookGenres + genreList[genreNum] + ", "

    #Get trigger(s), save as bookTriggers with triggers split by commas
    triggerLabel = soup.find(id="Trigger_Warnings")
    triggerListCheck = triggerLabel.parent.find_next_sibling("ul")
    bookTriggers = "None"
    if triggerListCheck != None:
        bookTriggers = ""
        #List of all triggers with the <li> still on them
        triggerList = triggerListCheck.find_all("li")
        for t in triggerList:
            #Iterate through all triggers in list, remove <li> tag, and add to bookTriggers; separate triggers with commas
            bookTriggers = bookTriggers + t.text + ", "

    #Get age group if it's there, save as bookAgeGroup. If it's not there, save bookAgeGroup as "None"
    bookAgeGroup = "None"
    ageGroupLabel = soup.find(string="Age group")
    if ageGroupLabel != None:
        bookAgeGroup = ageGroupLabel.parent.find_next_sibling("td").contents[0]

    #Get date on which the book was published, if it's there, save as bookPubDate. If it's not there, save bookPubDate as "None"
    bookPubDate = "None"
    pubDateLabel = soup.find(string="Published")
    if pubDateLabel != None:
        bookPubDate = pubDateLabel.parent.find_next_sibling("td").contents[0]

    #Get book publisher if it's there, save as bookPublisher. If it's not there, save bookPublisher as "None"
    bookPublisher = "None"
    publisherLabel = soup.find(string="Publisher")
    if publisherLabel != None:
        bookPublisher = publisherLabel.parent.find_next_sibling("td").contents[0]
    
    return Book(
            id=bookID,
            title=bookTitle,
            authors=bookAuthors,
            genres=bookGenres,
            triggers=bookTriggers,
            age_group=bookAgeGroup,
            published=bookPubDate,
            publisher=bookPublisher
            )

