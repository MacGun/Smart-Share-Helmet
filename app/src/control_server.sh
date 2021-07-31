PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
SRC=${DIR}/src

OPT=$1
ON="on"
OFF="off"
START="start"
STOP="STOP"

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`date`] [$PID]"
}

case $OPT in
    $ON | $START) ${SRC}/system.sh ;;
    $OFF | $STOP) ${SRC}/killer.sh ;;
    *) echo "`log` Wrong Option." ;;
esac
