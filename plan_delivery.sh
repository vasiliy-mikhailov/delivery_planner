curl -X POST -H "Content-Type:multipart/form-data" -F "plan_file=@plan.xlsx" http://localhost:8000/delivery_planner_app/plan_delivery -o plan_out.xlsx
