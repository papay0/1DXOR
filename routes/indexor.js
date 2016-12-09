var express = require('express');
var router = express.Router();
var db = require('../db/db');
var math = require("mathjs");
var exec = require('child_process').exec;

router.get('/', function (req, res, next) {
	var collection = db.get().collection('words');
	// Call a python script in order to stemm and remove_stop_word from the input sentence
	var documentArray = null;
	var sentence = req.query.words;
	var documentsNumber = 0;
	var p =  db.get().collection('documents').count().then(res => documentsNumber = res).then(() =>  
	query(sentence).then((result) => {
		
		var matchingDocuments = createDocumentArray(result);
		
		var matrix = buildMatrix(result, matchingDocuments);
		var Q = computeIDF(result);
		var scores = computeScores(matrix, matchingDocuments, Q);
		
		scores = sortedScores(scores);
		console.log(scores);
		res.render('documents', {documents: scores})
	}));
	/*	var resultMerged = [].concat.apply([], result);
		console.log(resultMerged);
		res.render('documents', { documents: sortByFrequency_old(resultMerged) });
	}).catch(function(e) {
		res.render('documents', {documents: ["ERROR: "+e]});*/

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

	function findWord(word) {
		return new Promise(
				(resolve, error) => {
					collection.find({'word': word }).toArray(function (err, result) {
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


	function query(words) {
		return stem(words).then((res) => { // search into bdd for every word
			var arrayOfPromises = [];
			var stems = res.split(" ");
			for (var i = 0; i < stems.length; i++) {
				var findPromise = findWord(stems[i]);
				arrayOfPromises.push(findPromise);
				console.log("word: " + stems[i]);
			}
			return Promise.all(arrayOfPromises);
		});
	}

	function stem(sentence){
		var cmd = 'python3 indexer/stem_me.py ' + sentence;
		return new Promise((resolve, error) => {
			exec(cmd, function (err, stdout, stderr) { // stem sentence with python code
				if (err) error(err);
				resolve(stdout);
			});
		});
	}

	MatchingDocuments = (function() {
		function MatchingDocuments() {
			this.documentsIDs = {}
			this.documents = []
		}

		MatchingDocuments.prototype.addDocument = function(documentName)  {
			if (this.documentsIDs[documentName]===undefined) {
				this.documentsIDs[documentName] = this.documents.length
					this.documents.push(documentName);
			}
		}

		MatchingDocuments.prototype.getName = function(index) {
			return this.documents[index];
		}

		MatchingDocuments.prototype.getIndex = function(name) {
			return this.documentsIDs[name];
		}

		MatchingDocuments.prototype.size = function() {
			return this.documents.length;
		}
		return MatchingDocuments;
	})();

	function createDocumentArray(results) {
			var matchingDocuments = new MatchingDocuments()	
			
			for (var wordResults of results) {
				for (document of wordResults) {
					matchingDocuments.addDocument(document.name);
					
				}
			}

		return matchingDocuments;
	}

	function buildMatrix(results, matchingDocuments) {

		var mat = math.zeros(matchingDocuments.size(), results.length);
		for (var wId = 0; wId < results.length; wId++) {
			var wordResults = results[wId];
			for (var doc of wordResults ) {
				mat.subset(math.index(matchingDocuments.getIndex(doc.name), wId), doc.count);
			}
		}
		console.log(mat._data);
		return mat;
	}

	function computeScores(matrix, matchingDocuments, Q) {
		var scores = {};
		for (var documentId = 0; documentId < matchingDocuments.size()  ; documentId++) {
			var score = 0;
			// subset(math.index(documentId,[0,matrix.size()[1]-1]))
			score = matrix._data[documentId].reduce((a, b, i) => a+b*Q[i]);
			scores[matchingDocuments.getName(documentId)]=score;
		}
		return scores;
	}

	function IDF(wordDocuments) {
		var idf = []
		for (var docs of wordDocuments) {
			idf.push(log(documentNumber/docs.length))
		}

		return idf;
	}

	function sortedScores(scores) {
		var scoreArray = [];
		for (var docName in scores) {
			scoreArray.push([docName, scores[docName]]);
		}
		return scoreArray.sort((a,b)=>{return -a[1] + b[1]});
	}

});

module.exports = router;
