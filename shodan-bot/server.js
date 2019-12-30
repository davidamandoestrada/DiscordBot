'use strict';

const express = require('express');
const fs = require('fs');

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

    res.setHeader('Content-Type', 'application/json');
    readJson('./resources/data.json', (err, data) => {
        const lowerCaseMessageContent = content.toLocaleLowerCase();
        const functionToCheckIfStringIsInIterable = (string) => { return (element) => element.toLocaleLowerCase() == string }

        const messageIsProfane = data.profanity.some(functionToCheckIfStringIsInIterable(lowerCaseMessageContent))
        const messageIsPolitical = data.political.some(functionToCheckIfStringIsInIterable(lowerCaseMessageContent))
        const messageIsEpic = data.epic.some(functionToCheckIfStringIsInIterable(lowerCaseMessageContent))

        if (messageIsProfane) {
            res.send(JSON.stringify({ response_message: `***${author}, Watch your mouth, insect.***`, error: null }));
        }
        else if (messageIsPolitical) {
            res.send(JSON.stringify({ response_message: `***${author}, No politics, insect!***`, error: null }));
        }
        else if (messageIsEpic) {
            res.send(JSON.stringify({ response_message: `***${author}, I tire of this topic, insect! Move along!***`, error: null }));
        }
        else {
            res.send(JSON.stringify({ response_message: "I am shodan", error: null }));
        }

    })

});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);