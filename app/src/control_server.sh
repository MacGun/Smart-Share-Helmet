PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
SRC=${DIR}/src

OPT=$1
PARAM=$2
ON="on"
OFF="off"
START="start"
STOP="stop"
STATUS="status"
STAT="stat"
KILL="kill"
TIMER="timer"
SETTIMER="set_timer"

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`now`] [$PID]"
}

case $OPT in
    $ON | $START) ${SRC}/system.sh ;;
    $OFF | $STOP) ${SRC}/killer.sh ;;
    $STATUS | $STAT) ${SRC}/status.sh;;
    $KILL)
        case $PARAM in
            system) kill `cat ${PIDDIR}/runsystem.pid` 2> /dev/null;;
            supervisor) kill `cat ${PIDDIR}/supervisor.pid` 2> /dev/null;;
            rebooter) kill `cat ${PIDDIR}/rebooter.pid` 2> /dev/null ;;
            app|application) kill `cat ${PIDDIR}/park_app.pid` 2> /dev/null ;;
            *) echo "`log` Wrong Parameter." ;;
        esac ;;
    $TIMER) cat ${SRC}/timer;;
    $SETTIMER) 
        case $PARAM in
            0.[0-9]         ) echo $PARAM > ${SRC}/timer;;
            [0-9]           ) echo $PARAM > ${SRC}/timer;;
            [0-9][0-9]      ) echo $PARAM > ${SRC}/timer;;
            [0-9][0-9][0-9] ) echo "Timer Parameter is too Big." ;;
            *) echo "Wrong Parameter."; exit;;
        esac 
        echo "Set Timer ${PARAM} sec.";;
    *) echo "`log` Wrong Option." ;;
esac
