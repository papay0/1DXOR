var express = require('express');
var router = express.Router();
var db = require('../db/db');
var exec = require('child_process').exec;

router.get('/', function (req, res, next) {
  var collection = db.get().collection('words');
  // Call a python script in order to stemm and remove_stop_word from the input sentence
  var sentence = req.query.words;
  var cmd = 'python3 indexer/stem_me.py ' + sentence;
  var p = new Promise((resolve, error) => {
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
    var resultMerged = [].concat.apply([], result);
    console.log("resultMerged: "+resultMerged);
    console.log("result: " + sortByFrequency(resultMerged));
    res.render('documents', { documents: sortByFrequency(resultMerged) });
  });

  function sortByFrequency(array) {
    var frequency = {};

    array.forEach(function (value) { frequency[value] = 0; });

    var uniques = array.filter(function (value) {
      return ++frequency[value] == 1;
    });

    return uniques.sort(function (a, b) {
      return frequency[b] - frequency[a];
    });
  }

  function async_find(word) {
    return new Promise(
      (resolve, error) => {
        collection.find({ '_id': word }).toArray(function (err, result) {
          if (err) error(err);
          if (!Object.keys(result).length) {
            resolve([]);
          } else {
            var documents = result[0].documents;
            console.log("res find: "+documents);
            resolve(documents);
          }
        });
      }
    );
  }

});
module.exports = router;
