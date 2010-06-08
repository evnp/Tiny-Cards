import sys
import random
import re

random.seed()
score = 0.0  # Score
rounds = 0.0  # number of Rounds

f = open(sys.argv[1]).readlines()

cards = zip([l[2:-1] for i, l in enumerate(f) if i%3 == 0],
            [l[2:-1] for i, l in enumerate(f) if i%3 == 1])

while(cards):
    rounds = rounds + 1
    card = random.choice(cards)

    while(True):
        print '\nQuestion: ' + card[0]

        if re.sub('[\s\(\)_]+', '', card[1]) == re.sub('[\s\(\)_]+', '', raw_input()):
            score = score + 1
            print '\nCorrect!\nScore: %d\nYour hit rate is %d%%.' % (score, (score/rounds)*100)
            break
        else:
            print '\nIncorrect. Would you like to try again? [Y,n]'
            response = raw_input()

            while not re.match("[yn]|yes|no", response, re.I) and response != '':
                print "Please enter 'y' or 'n'"
                response = raw_input()

            if re.match("no?", response, re.I):
                print '\nThe answer was ' + card[1]
                print 'Score: %d\nYour hit rate is %d%%' % (score, (score/rounds)*100)
                if score/rounds < 0.5: print "Hang in there, you'll get it!"
                break

    cards.remove(card)

print 'Final Score\nCorrect: %d\nIncorrect: %d\nHit Ratio: %d%%' % (score, rounds-score, score/rounds)
if score/rounds > 0.8: print 'Congratulations! You rocked that set.'
