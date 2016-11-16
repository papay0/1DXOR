var express = require('express');
var router = express.Router();
var db = require('../db/db');
var exec = require('child_process').exec;

router.get('/', function (req, res, next) {
  var collection = db.get().collection('words');
  // Call a python script in order to stemm and remove_stop_word from the input sentence
  var sentence = req.query.words;
  var cmd = 'python3 indexer/stem_me.py ' + sentence;
  var p = new Promise(
    (resolve, error) => {
      exec(cmd, function (err, stdout, stderr) {
        if (err) error(err);
        resolve(stdout);
      });
    }
  ).then((res) => {
    var arrayOfPromises = [];
    var sentenceStemmed = res.split(" ");
    for (var i = 0; i < sentenceStemmed.length; i++) {
      var findPromise = async_find(sentenceStemmed[i]);
      arrayOfPromises.push(findPromise);
      console.log("word: " + sentenceStemmed[i]);
    }
    return Promise.all(arrayOfPromises);
  }).then(result => {
    console.log("result: " + result);
    res.render('documents', { documents: result});
  });

  function async_find(word) {
    return new Promise(
      (resolve, error) => {
        collection.find({ '_id': word }).toArray(function (err, result) {
          if (err) error(err);
          //console.log('result: '+JSON.stringify(result));
          if (!Object.keys(result).length) {
            resolve([]);
          } else {
            var documents = result[0].documents;
            console.log(documents);
            resolve(documents);
          }
        });
      }
    );
  }

});
module.exports = router;
