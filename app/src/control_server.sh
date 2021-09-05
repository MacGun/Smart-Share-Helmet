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
TREE="tree"
KILL="kill"
TIMER="timer"
SETTIMER="set_timer"
HELP="help"

USAGE="USAGE:\n\t server [ ACT ] | [OPTION] [PARAMETER]\n"
EXAMPLE="EXAMPLE:\n\t'server start'\n\t'server off'\n"
OPTIONS="OPTIONS:\n\t$ON     | $START        : Run Whole Server System.
\t$OFF    | $STOP         : Terminate Whole Server System.
\t$STATUS | $STAT         : Show Server Process Status. Also Show Timer Interval Setting.
\t$TREE                  : Show File Tree About This Application.
\t$TIMER                 : Show Timer Interval Setting.
\t$SETTIMER [PARAMETER] : Set Timer interval.
\t$HELP                  : Show This Message.\n"

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`now`] [$PID]"
}

function help() {
    echo -e "$USAGE\n$EXAMPLE\n$OPTIONS"
}

case $OPT in
    $ON | $START) ${SRC}/system.sh ;;
    $OFF | $STOP) ${SRC}/killer.sh ;;
    $STATUS | $STAT) ${SRC}/status.sh;;
    $TREE) tree ${DIR};;
    $KILL)
        case $PARAM in
            system) kill `cat ${PIDDIR}/runsystem.pid` 2> /dev/null;;
            supervisor) kill `cat ${PIDDIR}/supervisor.pid` 2> /dev/null;;
            rebooter) kill `cat ${PIDDIR}/rebooter.pid` 2> /dev/null ;;
            app|application) kill `cat ${PIDDIR}/park_app.pid` 2> /dev/null ;;
            *) echo "`log` Wrong Parameter." ;;
        esac ;;
    $TIMER) echo "Timer Interval :`cat ${SRC}/timer`";;
    $SETTIMER) 
        case $PARAM in
            0.[0-9]         ) echo $PARAM > ${SRC}/timer;;
            [0-9]           ) echo $PARAM > ${SRC}/timer;;
            [0-9][0-9]      ) echo $PARAM > ${SRC}/timer;;
            [0-9][0-9][0-9] ) echo "Timer Parameter is too Big." ;;
            *) echo "Wrong Parameter."; exit;;
        esac 
        echo "Set Timer ${PARAM} sec.";;
    $HELP) help;;
    *) help ;;
esac
