const _ = require('lodash');

// Constants
const FUZZYMATCH_SCORE = 0.80

module.exports = {
    getFuzzyMatches: function (typeOfMatch, stringToCheck) {
        return _.flatten(stringToCheck.split(" ").map(word => {
            const fuzzyMatches = typeOfMatch.get(word) || []
            const highScoringFuzzyMatches = fuzzyMatches.filter(fuzzyMatch => fuzzyMatch[0] >= FUZZYMATCH_SCORE)
            return highScoringFuzzyMatches.map(fuzzyMatch => {
                return {
                    "score": fuzzyMatch[0],
                    "cutOffScore": FUZZYMATCH_SCORE,
                    "word": word,
                    "wordMatchedAgainst": fuzzyMatch[1]
                }
            })
        }))
    }
}