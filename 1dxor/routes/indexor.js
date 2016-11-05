var express = require('express');
var router = express.Router();
var db = require('../db/db')
/* GET /todos listing. */
router.get('/:word', function(req, res, next) {
  var collection = db.get().collection('key_words');
  var word = req.param('word');
  collection.find({'_id': word}).toArray(function(err, result) {
    var documents = result[0].documents;
    console.log(documents);
    res.render('documents', { documents: documents});
  })
});
module.exports = router;
