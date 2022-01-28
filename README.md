# wordle_helper
Given the results of guesses in Wordle, this class returns the list of words satisfying the conditions. 

### Usage
```
from wordle_helper import WordleHelper

wordle_helper = WordleHelper()

wordle_helper.add_result('query', '11111')

wordle_helper.add_result('minty', '32121')

words = wordle_helper.get_candidate_words()
```
1st input to add_result is the guess and 2nd input is the result encoded as follows

gray -> 1

yellow -> 2

green -> 3

After running the above code the variable words will be ['moist', 'motif'].

Tested on https://hellowordl.net/?challenge=bW90aWY.
