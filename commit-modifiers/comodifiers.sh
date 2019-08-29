#!/bin/sh
image=comodifiers
repo_path=$1
echo "export commit logs ..."
docker run -it --rm -v `pwd`:/var/run/repo -v ${repo_path}:/var/lib/repo ${image} python main.py --export -f /var/run/repo/commits.json
json_file=$2
if [ -f "$json_file" ]
then
    echo "modify commit logs ..."
    docker run -it --rm -v `pwd`:/var/run/repo -v ${repo_path}:/var/lib/repo ${image} python main.py --modify -f /var/run/repo/commits.json
fi