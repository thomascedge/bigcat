# run pytests
pytest -k "service" > logs/service_test.log 
pytest -k "e2e" > logs/e2e_test.log

# clean files
python3 clean_test_database.py