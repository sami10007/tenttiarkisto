# this script goes through all the *.tab files and creates a single django fixture
import json

SUPERUSERS = ["banjomies"]
ents = []

def lines(filename):
  for line in open(filename, "r"):
    yield line.rstrip('\n').split('\t')

def ent(model, pk, fields):
  return {"pk": pk, "model": model, "fields": fields}

# construct languages
ents.extend([ent("exams.lang", int(l[0]), {"code": l[1], "name": l[2]}) for l in lines("langs.tab")])

# construct users
def create_user(l):
  fields = {
      "username": l[1], 
      "is_active": True, 
      "is_superuser": l[1] in SUPERUSERS,
      "is_staff": int(l[6]) > 100, 
      "date_joined": l[3], 
      "last_login": l[4] if l[4] != "NULL" else l[3],
      "password": l[2]
    }
  if l[5] != "NULL":
    fields["email"] = l[5]
  return ent("auth.user", int(l[0]), fields)

ents.extend([create_user(l) for l in lines("users.tab")])

# construct courses
ents.extend([ent("exams.course", int(l[0]), {"code": l[1], "name": l[2]}) for l in lines("courses.tab")])

# construct exams

# tenttiarkisto contains broken data ie. some exams with course 0 which doesn't exist
def valid_exam(l):
  return l[1] != "0"

def create_exam(l):
  exam_date = l[2].split(" ")[0]
  date_added = l[5].split(" ")[0]
  fields = {
      "lang": int(l[3] if l[3] != "NULL" else 4),
      "course": int(l[1]),
      "exam_date": exam_date.replace("-00", "-01") if exam_date != "0000-00-00" else date_added,
      "submitter": int(l[4]) if l[4] != "NULL" else None,
      "date_added": date_added,
      "desc": l[6]
    }
  return ent("exams.exam", int(l[0]), fields)
VALID_EXAM_IDS = []
for l in lines("exams.tab"):
  if valid_exam(l):
    ents.append(create_exam(l))
    VALID_EXAM_IDS.append(l[0])

# construct exam files
ents.extend([ent("exams.examfile", int(l[0]), {"exam": int(l[1]), "exam_file": "exams/"+l[2]}) for l in lines("files.tab") if l[1] in VALID_EXAM_IDS])

print json.dumps(ents, indent=4)
