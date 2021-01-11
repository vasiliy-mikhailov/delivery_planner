docker build -f server/Dockerfile -t 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-server:dev ./server
docker build -f client/Dockerfile -t 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-client:dev ./client
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 367629471055.dkr.ecr.eu-central-1.amazonaws.com
docker push 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-server:dev
docker push 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-client:dev

docker build -f server/Dockerfile.prod -t 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-server:prod ./server
docker build -f client/Dockerfile.prod -t 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-client:prod ./client
docker push 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-server:prod
docker push 367629471055.dkr.ecr.eu-central-1.amazonaws.com/delivery-planner-client:prod

