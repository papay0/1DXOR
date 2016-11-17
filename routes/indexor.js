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
    exec(cmd, function (err, stdout, stderr) { // stem sentence with python code
      if (err) error(err);
      resolve(stdout);
    });
  }
  ).then((res) => { // search into bdd for every word
    var arrayOfPromises = [];
    var sentenceStemmed = res.split(" ");
    for (var i = 0; i < sentenceStemmed.length; i++) {
      var findPromise = async_find(sentenceStemmed[i]);
      arrayOfPromises.push(findPromise);
      console.log("word: " + sentenceStemmed[i]);
    }
    return Promise.all(arrayOfPromises);
  }).then(result => { // sort by frequency and display result
    var resultMerged = [].concat.apply([], result);
    res.render('documents', { documents: sortByFrequency_old(resultMerged) });
  }).catch(function(e) {
    res.render('documents', {documents: ["ERROR: "+e]});
});

  function sortByFrequency_old(array) {
    var frequency = {};
    array.forEach(function (value) {
      var key = Object.keys(value);
      if (key in frequency) {
        frequency[key] += value[key];
      } else {
        frequency[key] = value[key];
      }
    });
    console.log("frequency: "+JSON.stringify(frequency));
    return Object.keys(frequency).sort(function (a, b){return frequency[b]-frequency[a]}); // sort decreasing order
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
            console.log("["+word+"]res find: "+JSON.stringify(documents));
            resolve(documents);
          }
        });
      }
    );
  }

});
module.exports = router;
