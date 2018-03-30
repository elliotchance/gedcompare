# -*- coding: utf-8 -*-

import gedcom
import sys

# Since we are dealing with a lot of UTF-8 characters it can cuase encoding
# errors. I'm not sure if this is the right thing to do, but I found the the
# solution here: https://stackoverflow.com/a/21190382
reload(sys)
sys.setdefaultencoding('utf8')

# Genders
ICON_GENDER = u'🚻 '
ICON_MALE = u'♂️'
ICON_FEMALE = u'♀️'

# Life events
# FIXME: ICON_MARRIAGE: Use the male/male or female/female emoji for the correct
# genders.
ICON_BIRTH = u'👶 '
ICON_CHRISTENING = u'⛪ '
ICON_RESIDENCE = u'🏠 '
ICON_OCCUPATION = u'🔨 '
ICON_MARRIAGE = u'💑 '
ICON_DIVORCE = u'⚮'
ICON_DEATH = u'✝️ '
ICON_BURIAL = u'⚰️ '

# Other icons
ICON_NAME = u'📛 '
ICON_NOT_EQUAL = u'↔️ '
ICON_LEFT_ONLY = u'⬅️ '
ICON_RIGHT_ONLY = u'➡️ '

def person_str(p):
    if p is None:
        return "(none)"

    person_gender = ''
    if gender(p) == 'M':
        person_gender = ICON_MALE
    if gender(p) == 'F':
        person_gender = ICON_FEMALE

    name = "%s %s, %s" % (person_gender, p.name[1], p.name[0])

    if 'BIRT' in p and 'DEAT' in p:
        name += " (%s - %s)" % (birth_date(p), death_date(p))
    elif 'BIRT' in p:
        name += " (%s - )" % birth_date(p)
    elif 'DEAT' in p:
        name += " ( - %s)" % death_date(p)

    return name

def first_name(p):
    if p is None:
        return ''

    return p.name[0]

def last_name(p):
    if p is None:
        return ''
        
    return p.name[1]

def gender(p):
    if p is None or 'SEX' not in p:
        return ''
        
    return p['SEX'].value

def birth_date(p):
    if p is None or 'BIRT' not in p or 'DATE' not in p['BIRT']:
        return ''
        
    return p['BIRT']['DATE'].value

def birth_place(p):
    if p is None or 'BIRT' not in p or 'PLAC' not in p['BIRT']:
        return ''
        
    return p['BIRT']['PLAC'].value

def death_date(p):
    if p is None or 'DEAT' not in p or 'DATE' not in p['DEAT']:
        return ''
        
    return p['DEAT']['DATE'].value

def death_place(p):
    if p is None or 'DEAT' not in p or 'PLAC' not in p['DEAT']:
        return ''
        
    return p['DEAT']['PLAC'].value

def burial_date(p):
    if p is None or 'BURI' not in p or 'DATE' not in p['BURI']:
        return ''
        
    return p['BURI']['DATE'].value

def burial_place(p):
    if p is None or 'BURI' not in p or 'PLAC' not in p['BURI']:
        return ''
        
    return p['BURI']['PLAC'].value

# The python gedcom package does not support some GEDCOM elements. The easiest
# thing to do right now is to strip them out into a temp file first.
def prepare_file(file_path, tmp_path):
    with open(file_path, 'rb') as f:
        content = f.read().split('\r')
        content = [x for x in content if not x.startswith('2 CONT')]
        content = [x for x in content if not x.startswith('1 TITL')]

    with open(tmp_path, "w") as text_file:
        text_file.write('\n'.join(content))

print("Loading GEDCOM files...")

# Read all of the people from the first file (main).
prepare_file(sys.argv[1], '/tmp/a.ged')
gedcomfile = gedcom.parse('/tmp/a.ged')
people1 = {}

for person in gedcomfile.individuals:
   people1[person.id] = person

# Read all of the people from the second file (to diff).
prepare_file(sys.argv[2], '/tmp/b.ged')
gedcomfile = gedcom.parse('/tmp/b.ged')
people2 = {}

for person in gedcomfile.individuals:
   people2[person.id] = person

def find_by_id(people1, id2, person2):
    for id1, person1 in people1.iteritems():
        if id1 == id2:
            return id2

    return None

def find_by_name(people1, person2):
    matches = []
    for id1, person1 in people1.iteritems():
        if first_name(person1) == first_name(person2) and \
            last_name(person1) == last_name(person2):
            matches.append(id1)

    return matches

def find_people(person_map, people1, people2):
    for id2, person2 in people2.iteritems():
        # Ignore previous matches
        ignore = False
        for _, id1 in person_map:
            if id2 == id1:
                ignore = True
                break

        if ignore:
            continue

        # First try to find them by ID.
        match = find_by_id(people1, id2, person2)
        if match is not None:
            person_map.append([id2, match])
            continue

        # Match by name
        matches = find_by_name(people1, person2)
        if len(matches) == 1:
            person_map.append([id2, matches[0]])
            continue

        # We cannot match this person, or they are a new person.
        person_map.append([id2, None])

        if len(person_map) % 100 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

# Try to calculate the same people in each tree.
sys.stdout.write('Comparing trees')
sys.stdout.flush()

person_map = []
find_people(person_map, people1, people2)
find_people(person_map, people2, people1)
print "\n"

def compare_line(title, p1, p2, f):
    left, right = f(p1), f(p2)

    c = ICON_NOT_EQUAL
    if left is '' and right is not '':
        c = ICON_RIGHT_ONLY
    elif left is not '' and right is '':
        c = ICON_LEFT_ONLY

    if left is '':
        left = '(none)'
    if right is '':
        right = '(none)'

    if left != right:
        return '  %s %s %s    %s %s' % (title, left.ljust(60), c, title, right)

    return None

for id2, id1 in person_map:
    p1 = None
    if id1 in people1:
        p1 = people2[id2]
    p2 = None
    if id1 in people1:
        p2 = people1[id1]

    lines = filter(lambda x: x is not None, [
        compare_line(ICON_GENDER, p1, p2, gender),
        compare_line(ICON_NAME, p1, p2, first_name),
        compare_line(ICON_NAME, p1, p2, last_name),
        compare_line(ICON_BIRTH, p1, p2, birth_date),
        compare_line(ICON_BIRTH, p1, p2, birth_place),
        compare_line(ICON_DEATH, p1, p2, death_date),
        compare_line(ICON_DEATH, p1, p2, death_place),
        compare_line(ICON_BURIAL, p1, p2, burial_date),
        compare_line(ICON_BURIAL, p1, p2, burial_place),
    ])

    if len(lines) > 0:
        print '%s      %s' % (person_str(p1).ljust(65), person_str(p2))
        print '\n'.join(lines)
        print
