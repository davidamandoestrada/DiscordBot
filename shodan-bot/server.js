'use strict';

const express = require('express');
const fs = require('fs');
const FuzzySet = require('fuzzyset.js')
const utility = require('./utility');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.use(express.json())

const readJson = (path, cb) => {
    fs.readFile(require.resolve(path), (err, data) => {
        if (err)
            cb(err)
        else
            cb(null, JSON.parse(data))
    })
}

app.get('/message', (req, res) => {
    const author = req.body.author;
    const content = req.body.content;

    readJson('./resources/data.json', (err, data) => {

        const fuzzyProfanityWords = FuzzySet(data.profanity);
        const fuzzyPoliticalWords = FuzzySet(data.political)
        const fuzzyEpicsWords = FuzzySet(data.epic)


        const fuzzyProfanityMatches = utility.getFuzzyMatches(fuzzyProfanityWords, content)
        const fuzzyPoliticalMatches = utility.getFuzzyMatches(fuzzyPoliticalWords, content)
        const fuzzyEpicMatches = utility.getFuzzyMatches(fuzzyEpicsWords, content)

        const responses = []
        if (fuzzyProfanityMatches.length > 0) {
            responses.push(`***${author}, Watch your mouth, insect.***`)
            responses.push(fuzzyProfanityMatches.map(match => JSON.stringify(match)).toString())
        }
        if (fuzzyPoliticalMatches.length > 0) {
            responses.push(`***${author}, No politics, insect!***`)
            responses.push(fuzzyPoliticalMatches.map(match => JSON.stringify(match)).toString())
        }
        if (fuzzyEpicMatches.length > 0) {
            responses.push(`***${author}, I tire of this topic, insect! Move along!***`)
            responses.push(fuzzyEpicMatches.map(match => JSON.stringify(match)).toString())
        }

        if (responses.length == 0) {
            responses.push("Message received and processed")
        }

        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify({ response_message: responses.join("\n"), error: null }));


    })

});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);