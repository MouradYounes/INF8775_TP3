#!/bin/sh
programname=$0

function usage {
	echo "Vous avez mal entré les paramètres. Veuillez réessayer avec les options suivantes:"
    echo "usage: $programname -e [path_vers_exemplaire] -c [nombre_de_circonscriptions]"
    echo "  -e      path_vers_exemplaire peut être un chemin absolu,"
	echo "  relatif ou seulement le nom du fichier si ce dernier est dans le même directory"
    echo "  -c      représente le nombre de circonscriptions"
    exit 1
}

while [ "$1" != "" ]; do
    case $1 in
        -e )    shift
                file=$(basename $1)
				dir=$(dirname $1)
                PATH="$dir/$file"
                ;;
        -c )    shift
                C=$1
                ;;
        -p )    P=$1
                ;;
        * )     usage
                exit 1
    esac
    shift
done

if [ ! $C ]
then
    echo "number of circonscriptions not found"
    exit 1
fi

re='^[0-9]+$'
if ! [[ $C =~ $re ]] ; then
   echo "error: Not a number" 
   exit 1
fi

if [ ! -f $PATH ]
then
    echo "File not found!"
    exit 1
fi

/opt/anaconda3/bin/python main.py $PATH $C $P
#/usr/bin/g++ --std=c++17 -O3 src/main.cpp -o main.exe
#./main.exe $PATH $C $P
