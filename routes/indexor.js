var express = require('express');
var router = express.Router();
var db = require('../db/db');
var exec = require('child_process').exec;

router.get('/', function(req, res, next) {var collection = db.get().collection('words');
  // Call a python script in order to stemm and remove_stop_word from the input sentence
  var sentence = req.query.words;
  var cmd = 'python3 indexer/stem_me.py '+sentence;
  var p = new Promise(
    (resolve, error) => {
      exec(cmd, function(err, stdout, stderr) {
        if (err) error(err);
        resolve(stdout);
      });
    }
  ).then((res) => {
    // TODO: for loop on each words, wait for the result of async_find, at the end return the array of Documents. (sorted by occurence)
    // check my nlc-manager.js
    async_find(res);
  })

  function async_find(word) {
    collection.find({'_id': word}).toArray(function(err, result) {
    console.log('result: '+JSON.stringify(result));
    if (!Object.keys(result).length) {
      res.render('documents', { documents: ['empty']});
    } else {
      var documents = result[0].documents;
      console.log(documents);
      res.render('documents', { documents: documents});
    }
  });
  };

});
module.exports = router;
