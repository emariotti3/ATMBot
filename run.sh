#If container exists stop and remove it.
CONTAINER_NAME = "tbot"
OLD="$(docker ps --all --quiet --filter=name="$CONTAINER_NAME")"

if [ -n "$OLD" ]; then
  docker stop $OLD && docker rm $OLD
fi

#Build and run container.
docker build -t bot .
docker run -d -it -p 80:8080 --name=tbot bot
