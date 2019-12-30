'use strict';

const _ = require('lodash');
const express = require('express');
const fs = require('fs');
const FuzzySet = require('fuzzyset.js')

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';
const FUZZYMATCH_SCORE = 0.90

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

    res.setHeader('Content-Type', 'application/json');
    readJson('./resources/data.json', (err, data) => {
        const fuzzyProfanityWords = FuzzySet(data.profanity);
        const fuzzyPoliticalWords = FuzzySet(data.political)
        const fuzzyEpicsWords = FuzzySet(data.epic)

        const fuzzyProfanityMatches = _.flatten(content.split(" ").map(wordInMessageContent => {
            const fuzzyMatches = fuzzyProfanityWords.get(wordInMessageContent) || []
            const highlyRatedFuzzyMatches = fuzzyMatches.filter(fuzzyMatch => fuzzyMatch[0] >= FUZZYMATCH_SCORE)
            return highlyRatedFuzzyMatches.map(fuzzyMatch => {
                return {
                    "score": fuzzyMatch[0],
                    "cutOffScore": FUZZYMATCH_SCORE,
                    "wordMatched": fuzzyMatch[1],
                    "wordFromMessage": wordInMessageContent
                }
            })
        }))
        const fuzzyPoliticalMatches = _.flatten(content.split(" ").map(wordInMessageContent => {
            const fuzzyMatches = fuzzyPoliticalWords.get(wordInMessageContent) || []
            const highlyRatedFuzzyMatches = fuzzyMatches.filter(fuzzyMatch => fuzzyMatch[0] >= FUZZYMATCH_SCORE)
            return highlyRatedFuzzyMatches.map(fuzzyMatch => {
                return {
                    "score": fuzzyMatch[0],
                    "cutOffScore": FUZZYMATCH_SCORE,
                    "wordMatched": fuzzyMatch[1],
                    "wordFromMessage": wordInMessageContent
                }
            })
        }))
        const fuzzyEpicMatches = _.flatten(content.split(" ").map(wordInMessageContent => {
            const fuzzyMatches = fuzzyEpicsWords.get(wordInMessageContent) || []
            const highlyRatedFuzzyMatches = fuzzyMatches.filter(fuzzyMatch => fuzzyMatch[0] >= FUZZYMATCH_SCORE)
            return highlyRatedFuzzyMatches.map(fuzzyMatch => {
                return {
                    "score": fuzzyMatch[0],
                    "cutOffScore": FUZZYMATCH_SCORE,
                    "wordMatched": fuzzyMatch[1],
                    "wordFromMessage": wordInMessageContent
                }
            })
        }))
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

        responses.push("Message received and processed")
        res.send(JSON.stringify({ response_message: responses.join("\n"), error: null }));
        res.end()


    })

});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);