Welcome to 1DXOR!
===================

- IN DEV -
==========

Installation
-------------
> **What do you need?**
>
> - mongodb
> - python3
> - BeautifulSoup
> - nltk
> - node.js

Run it
------

```
$ git clone https://github.com/papay0/1DXOR.git
$ cd 1DXOR
$ npm install
$ cd indexer/
$ python3 main.py
$ cd ..
$ npm start
Go to http://0.0.0.0:4000/
```

Use it
------
You can for the moment query http://0.0.0.0:4000/indexor/your_word
The result will be a page with the different documents where 'your word' is in it.

MongoDB
-------
> **Good to know**
>
> - Show all 'tables': show dbs
> - Use a specidif one: use db1
> - See which database I use: db
> - Show all the collections: show collections
> - Delete a collection: db.my_collection.drop()
> - Print content of a collection: db.my_collection.find();
> - Print content of a collection, but more beautifully: db.my_collection.find().pretty();

Schema Database
---------------

key_documents:
```
{
    "_id" : "Document1",
    "words" : {
        "day" : 1,
        "over" : 2,
        "sunrise": 7,
        "computer": 1
    }
},
{
    "_id" : "Document2",
    "words" : {
        "computer" : 3,
        "network" : 1,
        "database": 9
    }
}
```

key_words:
```
{
    "_id" : "computer",
    "documents" : [ 
        "Document1",
        "Document2"
    ]
},
{
    "_id" : "sunrise",
    "documents" : [ 
        "Document1"
    ]
}
```

TODO
-------------
> - Use a stemmer for the search as well
> - Create a full stack (Express, MongoDB, Angular2: [docs](http://adrianmejia.com/blog/2014/10/01/creating-a-restful-api-tutorial-with-nodejs-and-mongodb/))
