#!/bin/sh

JQ="jq --raw-output --exit-status"

configure_aws_cli() {
  aws --version
  aws configure set default.region eu-central-1
  aws configure set default.output json
  echo "AWS Configured!"
}

register_task_definition() {
  if revision=$(aws ecs register-task-definition --cli-input-json "$task_definition" | $JQ '.taskDefinition.taskDefinitionArn'); then
    echo "Revision: $revision"
  else
    echo "Failed to register task definition"
    return 1
  fi
}

update_service() {
  if [[ $(aws ecs update-service --cluster $cluster --service $service --task-definition $revision | $JQ '.service.taskDefinition') != $revision ]]; then
    echo "Error updating service."
    return 1
  fi
}

deploy_cluster() {

  cluster="delivery-planner-cluster"

  # server
  task_definition_template_file="ecs_server_task_definition.json"
  task_definition_template=$(cat "ecs/$task_definition_template_file")
  task_definition=$(printf "$task_definition_template" $AWS_ACCOUNT_ID $AWS_REGION $SECRET_KEY $SQL_HOST $SQL_PASSWORD $AWS_REGION)
  echo "$task_definition"
  register_task_definition

  service="delivery-planner-server-service"
  update_service

  # client
  task_definition_template_file="ecs_client_task_definition.json"
  task_definition_template=$(cat "ecs/$task_definition_template_file")
  task_definition=$(printf "$task_definition_template" $AWS_ACCOUNT_ID $AWS_REGION $AWS_REGION)
  echo "$task_definition"
  register_task_definition

  service="delivery-planner-client-service"
  update_service 

}

configure_aws_cli
deploy_cluster
