Welcome to 1DXOR!
===================

Prerequisites
-------------
> **What do you need?**
>
> - mongodb
> - python3
> - BeautifulSoup
> - nltk

Installation
------------

```bash
$ git clone https://github.com/papay0/1DXOR.git
$ cd 1DXOR
$ npm install
$ npm run indexing
```

Use it
------

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

documents:
```javascript
{
    "_id" : "0az3e1aze4864aeaze45zac48",
		"name": "D11.html",
    "words" : {
        "day" : 1,
        "over" : 2,
        "sunrise": 7,
        "computer": 1
    }
},
{
    "_id" : "c1a8ze4a8448a4f8484a84z8r",
		"name": "D12.html",
    "words" : {
        "computer" : 3,
        "network" : 1,
        "database": 9
    }
}
```

words:
```javascript
{
    "_id" : "c3a9ze5a8449a5f8485a85z9r",
		"word": "georg"
    "documents" : {
        "Document1":1,
        "Document2": 12
    }
},
{
    "_id" : "c15a9za5a8449a58485a70z9r",
    "word" : "sunris",
    "documents" : {
        "Document1":15
    }
}
```
