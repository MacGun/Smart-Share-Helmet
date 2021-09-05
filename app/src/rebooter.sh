PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
PIDFILE=${PIDDIR}/rebooter.pid
TIMER=`cat ${DIR}/src/timer`

trap "cleanup; exit" SIGHUP SIGINT SIGTERM

function cleanup() {
    rm ${PIDfILE}
    echo -e "`log` Rebooter Terminated."
}

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`now`] [$PID]"
}

if [[ -a ${PIDFILE} ]];then
    echo "`log` Already Running Rebooter. (`cat ${PIDFILE}`)"
    exit
else
    echo "`log` Rebooter Start."
    touch ${PIDFILE}
    echo $PID > ${PIDFILE}
fi

while true; do
    STATE=`python3 ${DIR}/src/checkInternalError.py 2> /dev/null`
    if [[ $STATE == 500 ]];then
        kill `cat ${PIDDIR}/park_app.pid`
    else
        echo -e "`log` Status Code: $STATE."
    fi
    `sleep $TIMER`
done
