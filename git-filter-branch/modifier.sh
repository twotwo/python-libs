#!/bin/sh
image=git-filter-branch
repo_path=$2
if [ "$1" == "export" ]; then
    echo "export commit log as ./commits.json file ..."
    docker run -it --rm -v `pwd`:/var/run/repo -v ${repo_path}:/var/lib/repo ${image} python main.py --export -f /var/run/repo/commits.json ${ops}
elif [ "$1" == "modify" ]; then
    json_file=$3
    if [ -f "$json_file" ]; then
        echo "modify commit logs ..."
        docker run -it --rm -v `pwd`:/var/run/repo -v ${repo_path}:/var/lib/repo ${image} python main.py --modify -f /var/run/repo/${json_file} ${ops}
    else
        echo "modify failed. can't find .json file"
    fi
else
    match_email=$1
    email=$3
    name=$4
    echo "Modify by Email, find ${match_email}, change to email=${email}, name=${name}" ${ops}
    docker run -it --rm -v `pwd`:/var/run/repo -v ${repo_path}:/var/lib/repo ${image} python main.py -m ${match_email} -e ${email} -n ${name} --verbose
fi
