PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
PIDFILE=${PIDDIR}/runsystem.pid
SRC=${DIR}/src
SUPERVISOR=${SRC}/supervisor.sh
REBOOTER=${SRC}/rebooter.sh

trap "terminate; exit" SIGHUP SIGINT SIGTERM

function now() {
    echo `date +"%Y-%m-%d %T %z"`
}

function log() {
    echo "[`now`] [$PID]"
}

if [[ -a ${PIDFILE} ]];then
    echo "`log` Gunicorn Server System Already Running. (pid: `cat ${PIDFILE}`"
    exit
else
    touch ${PIDFILE}
    echo $PID > $PIDFILE
    echo "`log` Run Gunicorn Server System."
fi
 
function terminate() {
    rm ${PIDFILE}
    sleep 0.3
    echo "`log` Gunicorn Server System Terminated."
}

${SUPERVISOR} & 
sleep 1
${REBOOTER}
