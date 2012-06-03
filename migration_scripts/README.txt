How to migrate from old tenttiarkisto
-------------------------------------

1. Specify DB details in dumpalldata
2a. Run dumpalldata (./dumpalldata)
2b. Add "4\toth\tOther" to langs.tab
3. Create django fixture (python create_fixture.py > newfixture.json)
4. Import data into django using manage.py
     (python manage.py loaddata migration_scripts/newfixture.json)
5. Copy all the exam files from old exams/ to media/exams/
