import re
import sys
import time
import random

random.seed()
score = 0.0   # Score
rounds = 0.0  # Number of rounds
delay = 0.0    # Time delay between rounds
mc = False    # Multiple choice option


def kb_input(criteria=None, msg=None, allowEmpty=True):
    response = raw_input()
    if re.match('q(uit)?', response, re.I): sys.exit('Bye!')

    if criteria and msg:
        while not re.match(criteria, response, re.I):
            if allowEmpty and response == '': break
            print msg
            response = raw_input()

    return response


try:
    f = open(sys.argv[1:][-1]).readlines()
except:
    sys.exit('tinycards.py: usage: python tinycards.py [-t|-m] [filename]')

if '-t' in sys.argv:
    print 'Please enter the desired time delay between questions (minutes):'
    delay = float(kb_input('[\d\.]', 'Enter a decimal or float') or 0)

mc = '-m' in sys.argv

cards = zip([l[2:-1] for i, l in enumerate(f) if i%3 == 0],
            [l[2:-1] for i, l in enumerate(f) if i%3 == 1])

if mc:
    answers = [card[1] for card in cards]

while(cards):
    rounds = rounds + 1
    card = random.choice(cards)

    while(True):
        print '\nQuestion: ' + card[0]

        correct = None
        if mc:
            anscopy = answers
            choices = [card[1]]
            for i in range(3):
                choice = random.choice(anscopy)
                choices.append(choice)
                anscopy.remove(choice)

            for i in range(4):
                choice = random.choice(choices)
                if choice == card[1]: correct = i+1
                print '(%d) %s' % (i+1, choice)
                choices.remove(choice)

        if mc and int(kb_input('[1-4]', 'Please enter a number between 1 and 4', False)) == correct or not mc and re.sub(
                '[\s\(\)_]+', '', card[1]) == re.sub('[\s\(\)_]+', '', kb_input()):

            score = score + 1
            print '\nCorrect!\nScore: %d\nYour hit rate is %d%%.' % (score, (score/rounds)*100)
            break
        else:
            print '\nIncorrect. Would you like to try again? [Y,n]'
            response = kb_input('[yn]|yes|no', "Enter 'y' or 'n'")

            if re.match("no?", response, re.I):
                print '\nThe answer was ' + card[1]
                print 'Score: %d\nYour hit rate is %d%%' % (score, (score/rounds)*100)
                if score/rounds < 0.5: print "Hang in there, you'll get it!"
                break

    cards.remove(card)
    if delay: time.sleep(delay*60)

print 'Final Score\nCorrect: %d\nIncorrect: %d\nHit Ratio: %d%%' % (score, rounds-score, (score/rounds)*100)
if score/rounds > 0.8: print 'Congratulations! You rocked that set.'
