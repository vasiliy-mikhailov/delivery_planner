#!/bin/sh

JQ="jq --raw-output --exit-status"

configure_aws_cli() {
  aws --version
  aws configure set default.region eu-central-1
  aws configure set default.output json
  echo "AWS Configured!"
}

register_definition() {
  if revision=$(aws ecs register-task-definition --cli-input-json "$task_def" | $JQ '.taskDefinition.taskDefinitionArn'); then
    echo "Revision: $revision"
  else
    echo "Failed to register task definition"
    return 1
  fi
}

deploy_cluster() {

  # server
  template="ecs_server_task_definition.json"
  task_template=$(cat "ecs/$template")
  task_def=$(printf "$task_template" $AWS_ACCOUNT_ID $AWS_REGION $AWS_REGION $SECRET_KEY $SQL_HOST $SQL_PASSWORD $AWS_REGION)
  echo "$task_def"
  register_definition

  # client
  template="ecs_client_task_definition.json"
  task_template=$(cat "ecs/$template")
  task_def=$(printf "$task_template" $AWS_ACCOUNT_ID $AWS_REGION $AWS_REGION)
  echo "$task_def"
  register_definition

}

configure_aws_cli
deploy_cluster
