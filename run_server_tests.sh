docker-compose exec delivery-planner-server python -m pytest -n 8 -p no:warnings --cov-config=.coveragerc --cov=. --ignore=delivery_planner_app --ignore=delivery_planner_site

