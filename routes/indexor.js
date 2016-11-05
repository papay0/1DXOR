var express = require('express');
var router = express.Router();
var db = require('../db/db');
var exec = require('child_process').exec;

router.get('/', function(req, res, next) {
  res.render('documents', { documents: "You need to provide a word"});
}),

router.get('/:word', function(req, res, next) {

  // Call a python script in order to stemm and remove_stop_word from the input sentence
  var sentence = "\"Le chat est-il dans la voiture ?\""
  var cmd = 'python3 indexer/stem_me.py '+sentence;
  exec(cmd, function(error, stdout, stderr) {
    if (error) throw error;
    var result = stdout.split(" ");
    console.log(result);
    for (var i = 0; i < result.length; i++) {
      console.log("word: "+result[i]);
    }
  });

  var collection = db.get().collection('key_words');
  var word = req.param('word');
  collection.find({'_id': word}).toArray(function(err, result) {
    console.log('result: '+JSON.stringify(result));
    if (!Object.keys(result).length) {
      res.render('documents', { documents: ['empty']});
    } else {
      var documents = result[0].documents;
      console.log(documents);
      res.render('documents', { documents: documents});
    }
  })
});
module.exports = router;
