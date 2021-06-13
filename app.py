import pyrebase
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random
import os
import cloudscraper
import bs4
from pyrebase import pyrebase
scraper = cloudscraper.create_scraper()
scraper.debug = True
app=Flask(__name__)

books=[]
links=[]
@app.route('/',methods=['POST','GET'])
def home():
    return render_template('index.html')

@app.route('/available',methods=['POST','GET'])
def available():
    global books
    global links

    if request.method=='POST':

        find_book=request.form['search']


        find_book_link = ''

        book_name = (find_book.strip(' ')).split()
        for i in book_name:
            find_book_link += '+' + i




        content = scraper.get(
                "https://www.pdfdrive.com/search?q={}&pagecount=&pubyear=&searchin=&em=".format(find_book_link)).text

        soup = bs4.BeautifulSoup(content, 'html.parser')

        result = soup.find_all("a", class_="ai-search", href=True)
        links = []
        for link in result:
                links.append(link['href'])
        books = []
        for i in links:
                zero = ''
                for j in i:
                    link1 = (str(i).split('-'))
                    link1.remove(link1[-1])
                    for i in link1:
                        i = i.strip('/')
                        zero += ' ' + i
                books.append(zero)

            # print(links)
        print(books)

        return render_template('available.html',books=books)

    return render_template('index.html')

@app.route('/download',methods=['POST','GET'])
def download():
    if request.method=='POST':
        book_name=request.form['form-select form-select-lg mb-3']
        buk_ind=books.index(book_name)
        link=links[int(buk_ind)]

        pdfdrive = 'https://www.pdfdrive.com'
        book_l = pdfdrive + link

        ########### D O W N L O A D I N G   L I N K   P R O C E S S I N G #########################
        import requests

        content = (
            scraper.get(book_l).text)

        soup = bs4.BeautifulSoup(content, 'html.parser')
        result = soup.find_all("a", id="download-button-link", href=True)
        download = []
        for link in result:
            download.append(link['href'])
        dwnld = 'https://www.pdfdrive.com'
        ttl = dwnld + download[0]

        #########id###########################

        id = (str(download[0]).split('-')[-1].split('.')[0][1:])
        # print(ttl)
        ###############################     final download      ###################

        content = (
            scraper.get(ttl).text)

        soup = bs4.BeautifulSoup(content, 'html.parser')

        ###############key session###################
        content = (
            scraper.get(ttl).text)

        soup = bs4.BeautifulSoup(content, 'html.parser')

        script = soup.find_all('script')
        # print(script[7])
        py = str(script[7]).split()
        last = (py[13].split(';')[1])
        token = (last.split(',')[2])
        session_key = (token.split(":")[1])

        updated_session_key = (session_key.strip("''"))
        download_link = '/download.pdf?id={}&h={}&u=cache&ext=pdf'.format(id, updated_session_key)
        print(pdfdrive + download_link)
        return redirect(pdfdrive+download_link)
    return "try refreshing the page"







if __name__ == '__main__':
    app.debug=True
    app.secret_key='success'
    app.run()