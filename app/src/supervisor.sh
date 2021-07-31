PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
PIDFILE=${PIDDIR}/supervisor.pid

trap "cleanup; exit;" SIGHUP SIGINT SIGTERM

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`now`] [$PID]"
}

function cleanup() {
    echo -e "`log` Supervisor Terminated."
    rm ${PIDFILE}
}

if [[ -a $PIDFILE ]];then
    echo "`log` Already Running Supervisor. (pid: `cat ${PIDFILE}`)"
    exit
else
    touch ${PIDDIR}
    echo $PID > ${PIDFILE}
    echo "`log` Running Gunicorn Supervisor."
fi

while true; do
    if [[ -a ${PIDDIR}/park_app.pid ]];then
        PARK_APP=`cat ${PIDDIR}/park_app.pid`
        echo "`log` Gunicorn Server Already running."
        echo "`log` Please kill 'Gunicorn APP[$PARK_APP]' Before Run This Process."
        kill $PARK_APP
    fi
    echo "`log` Start Gunicorn Server."
    echo `$DIR/src/runserver.sh 1>&2`
    echo "`log` Server Exited."
    `sleep 1`
done
