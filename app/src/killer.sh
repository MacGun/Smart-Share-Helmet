PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid
array=(`ls $PIDDIR`)

function now() {
    NOW=`date +"%Y-%m-%d %T %z"`
    echo $NOW
}

function log() {
    echo "[`now`] [$PID]"
}

if [[ -z ${array[@]} ]];then
    echo "`log` There Are No Gunicorn Application Running."
    exit
else
    for process in ${array[@]};do
        kill `cat ${PIDDIR}/${process}`
    done
    echo "`log` Killed Gunicorn Apps"
fi
