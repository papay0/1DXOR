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
	var p = query(sentence).then((result) => {
		matchingDocuments = createDocumentArray(result);
		matrix = buildMatrix(result, matchingDocuments);
		scores = computeScores(matrix, matchingDocuments);
		scores = sortedScores(scores);
		console.log(scores);
		res.render('documents', {documents: scores})
	});
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

	class MatchingDocuments {
		constructor() {
			this.documentsIDs = {}
			this.documents = []
		}

		addDocument(documentName) {
			if (this.documentsIDs[documentName]===undefined) {
				this.documentsIDs[documentName] = this.documents.length
					this.documents.push(documentName);
			}
		}

		getName(index) {
			return this.documents[index];
		}

		getIndex(name) {
			return this.documentsIDs[name];
		}

		size() {
			return this.documents.length;
		}
	}

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

	function computeScores(matrix, matchingDocuments) {
		var scores = {};
		for (var documentId = 0; documentId < matchingDocuments.size()  ; documentId++) {
			var score = 0;
			matrix.subset(math.index(documentId,[0,matrix.size()[1]-1])).map((val)=>{score+=val});
			scores[matchingDocuments.getName(documentId)]=score;
		}
		return scores;
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
