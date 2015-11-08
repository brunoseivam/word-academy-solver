Word sets (`words.txt` and `words2.txt`) from https://github.com/docdis/english-words.

The database `db.txt` was built with:

    cat words*.txt | sed -e "/[^a-zA-Z]/d" | sed -e '/.\{3\}/!d' | tr A-Z a-z | sort | uniq > db.txt

Broken down:
* `cat words*.txt` joins all words\*.txt files together
* `sed -e "/[^a-zA-Z]/d"` removes all words that don't contain only ASCII alphabet characters
* `sed -e '/.\{3\}/!d'` removes all words with less than 3 characters
* `tr A-Z a-z` transforms all words to lowercase
* `sort` sorts the words in alphabetical order
* `uniq` removes duplicates
