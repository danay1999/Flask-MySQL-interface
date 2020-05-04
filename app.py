from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb


app = Flask(__name__)

app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='henrybooks'
app.config['MYSQL_CURSORCLASS']='DictCursor'


mysql = MySQL(app)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/authors/')
def author():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT * FROM Author ORDER BY authorNum''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/author.html',results=results)

@app.route('/books/')
def book():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT * FROM Book ORDER BY title ''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/books.html',results=results)

@app.route('/branch/')
def branch():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT * FROM Branch ''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/branch.html',results=results)
   
@app.route('/copy/')
def copy():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT Book.bookCode ,title, branchNum, copyNum, quality, price FROM Book JOIN Copy WHERE Book.bookCode = Copy.bookCode''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/copy.html',results=results)

@app.route('/inventory/')
def inventory():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT Book.bookCode, title, branchNum, OnHand FROM Inventory JOIN Book WHERE Book.bookCode = Inventory.bookCode ORDER BY title''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/inventory.html',results=results)

@app.route('/publisher/')
def publisher():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT * FROM Publisher ''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/publisher.html',results=results)

@app.route('/wrote/')
def wrote():  
    cursor = mysql.connection.cursor() 
    cursor.execute('''SELECT Book.bookCode, title, Author.authorNum, authorFirst, authorLast, sequence FROM Wrote JOIN Author, Book WHERE Book.bookCode = Wrote.bookCode and Wrote.authorNum = Author.authorNum ORDER BY authorNum''')
    results = cursor.fetchall()
    cursor.close()
    return render_template('/wrote.html',results=results)
   

@app.route('/addbook/', methods=['GET', 'POST'])
def addbook():    
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        title = request.form['title']
        publisherCode = request.form['publisherCode']
        bookType = request.form['bookType']
        paperback = request.form['paperback']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Book (bookCode, title, publisherCode, type, paperback) VALUES (%s,%s,%s,%s,%s)''',(bookCode,title,publisherCode,bookType,paperback))        
        print ("Book succesfully inserted in table 'book'")
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Book ORDER BY title ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/books.html', results=results)
    return render_template('/addbook.html')

@app.route('/addpublisher/', methods=['GET', 'POST'])
def addpublisher():
    if 'publisherCode' in request.form:
        publisherCode = request.form['publisherCode']
        publisherName = request.form['publisherName']
        city = request.form['city']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Publisher (publisherCode, publisherName, city) VALUES (%s,%s,%s)''',(publisherCode,publisherName, city))        
        print ("Publisher succesfully inserted in table 'publisher'")
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Publisher ORDER BY publisherName ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/publisher.html', results=results)
    return render_template('/addpublisher.html')

@app.route('/addauthor/', methods=['GET', 'POST'])
def addauthor():
    if 'authorFirst' in request.form:
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT MAX(authorNum)+1 FROM Author''')
        maxindex=cursor.fetchone()
        authorNum=maxindex['MAX(authorNum)+1']
        cursor.execute('''INSERT INTO Author (authorNum, authorLast, authorFirst) VALUES (%s,%s,%s)''',(authorNum, authorLast, authorFirst))        
        print ("Author succesfully inserted in table 'author'")
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Author ORDER BY authorNum ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/author.html', results=results)
    return render_template('/addauthor.html')

@app.route('/addcopy/', methods=['GET', 'POST'])
def addcopy():
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        branchNum = request.form['branchNum']
        copyNum = request.form['copyNum']
        quality = request.form['quality']
        price = request.form['price']
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO Copy (bookCode, branchNum, copyNum, quality, price) VALUES (%s,%s,%s,%s,%s)''',(bookCode, branchNum, copyNum, quality, price))        
        print ("Copy succesfully inserted in table 'copy'")
        mysql.connection.commit()
        cursor.execute('''SELECT Book.bookCode ,title, branchNum, copyNum, quality, price FROM Book JOIN Copy WHERE Book.bookCode = Copy.bookCode''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/copy.html', results=results)
    return render_template('/addcopy.html')

@app.route('/deletebook/', methods=['GET', 'POST'])
def deletebook():
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM Book WHERE bookCode = (%s)''' ,[bookCode])
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Book ORDER BY title ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/books.html', results=results)
    return render_template('/deletebook.html')

@app.route('/deletepublisher/', methods=['GET', 'POST'])
def deletepublisher():
    if 'publisherCode' in request.form:
        publisherCode = request.form['publisherCode']
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM Publisher WHERE publisherCode = (%s)''' ,[publisherCode])
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Publisher''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/publisher.html', results=results)
    return render_template('/deletepublisher.html')

@app.route('/deleteauthor/', methods=['GET', 'POST'])
def deleteauthor():
    if 'authorNum' in request.form:
        authorNum = request.form['authorNum']
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM Author WHERE authorNum = (%s)''' ,[authorNum])
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Author ORDER BY authorNum''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/author.html', results=results)
    return render_template('/deleteauthor.html')

@app.route('/deletecopy/', methods=['GET', 'POST'])
def deletecopy():
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        copyNum = request.form['copyNum']
        cursor = mysql.connection.cursor()
        cursor.execute('''DELETE FROM Copy WHERE bookCode = (%s) AND copyNum = (%s)''' ,[bookCode,copyNum])
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Copy''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/copy.html', results=results)
    return render_template('/deletecopy.html')

@app.route('/updatebook/', methods=['GET', 'POST'])
def updatebook():  
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        title = request.form['title']
        publisherCode = request.form['publisherCode']
        bookType = request.form['bookType']
        paperback = request.form['paperback']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Book SET title=%s, publisherCode=%s, type=%s, paperback=%s WHERE bookCode=%s''',(title,publisherCode,bookType,paperback,bookCode))        
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Book ORDER BY title ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/books.html', results=results)
    return render_template('/updatebook.html')

@app.route('/updatepublisher/', methods=['GET', 'POST'])
def updatepublisher():
    if 'publisherCode' in request.form:
        publisherCode = request.form['publisherCode']
        publisherName = request.form['publisherName']
        city = request.form['city']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Publisher SET publisherName=%s, city=%s WHERE publisherCode=%s''',(publisherName, city, publisherCode))        
        print ("Publisher succesfully inserted in table 'publisher'")
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Publisher ORDER BY publisherName ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/publisher.html', results=results)
    return render_template('/updatepublisher.html')

@app.route('/updateauthor/', methods=['GET', 'POST'])
def updateauthor():
    if 'authorFirst' in request.form:
        authorNum = request.form['authorNum']
        authorFirst = request.form['authorFirst']
        authorLast = request.form['authorLast']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Author SET authorLast=%s, authorFirst=%s WHERE authorNum=%s''',( authorLast, authorFirst, authorNum))        
        print ("Author succesfully inserted in table 'author'")
        mysql.connection.commit()
        cursor.execute('''SELECT * FROM Author ORDER BY authorNum ''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/author.html', results=results)
    return render_template('/updateauthor.html')

@app.route('/updatecopy/', methods=['GET', 'POST'])
def updatecopy():
    if 'bookCode' in request.form:
        bookCode = request.form['bookCode']
        branchNum = request.form['branchNum']
        copyNum = request.form['copyNum']
        quality = request.form['quality']
        price = request.form['price']
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE Copy SET branchNum=%s, copyNum=%s, quality=%s, price=%s WHERE bookCode=%s''',(branchNum, copyNum, quality, price, bookCode))        
        print ("Copy succesfully inserted in table 'copy'")
        mysql.connection.commit()
        cursor.execute('''SELECT Book.bookCode ,title, branchNum, copyNum, quality, price FROM Book JOIN Copy WHERE Book.bookCode = Copy.bookCode''')
        results = cursor.fetchall()
        cursor.close()
        return render_template('/copy.html', results=results)
    return render_template('/updatecopy.html')

@app.route('/searchresults', methods=['GET', 'POST'])
def searchresults():  
    if request.method == "POST":
        string = "%" + request.form['string'] + "%"
        print(string)
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT title, authorFirst, authorLast, publisherName, OnHand, branchName FROM Book, Author, Wrote, Publisher JOIN Inventory, Branch WHERE title LIKE (%s) AND Book.BookCode = Inventory.BookCode AND Inventory.BranchNum = Branch.BranchNum AND  Book.bookCode = Wrote.bookCode AND Author.authorNum = Wrote.authorNum AND Publisher.publisherCode = Book.publisherCode  ORDER BY title''', [string])
        results=cursor.fetchall()
        return render_template('searchresults.html', results=results)
    return render_template('index.html')
    
      
if __name__ == '__main__':
    app.run(debug=True)

