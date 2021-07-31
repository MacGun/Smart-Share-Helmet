PID=$$
DIR=~/Smart-Share-Helmet/app
PIDDIR=${DIR}/pid

APP="park_app.pid"
REB="rebooter.pid"
SYS="runsystem.pid"
SUP="supervisor.pid"
INFORMATION=($SYS $SUP $APP $REB)

COLOR="\033["
RED="${COLOR}0;31m"
PURPLE="${COLOR}0;35m"
WHITE="${COLOR}1;37m"
LITE_BLUE="${COLOR}1;34m"
NC="${COLOR}0m"

BOLD=$(tput bold)
NORM=$(tput sgr0)

START="${BOLD}${WHITE}"
END="${NC}${NORM}"

function now() {
    echo `date +"%Y-%m-%d %T %z"`
}

function log() {
    echo "[`log`] [$PID]"
}

WRAPPER_HEAD="${PURPLE}===== SERVER STATUS =====\n${NC}"
WRAPPER_TAIL="\n${PURPLE}=========================${NC}"
echo -e $WRAPPER_HEAD
for pid in ${INFORMATION[@]}; do
    if [[ ! -z `cat ${PIDDIR}/${pid} 2> /dev/null` ]];then
        STATE="${RED}On ${NC}"
        PIDNUM=`cat ${PIDDIR}/${pid}`
    else
        STATE="${LITE_BLUE}Off${NC}"
        PIDNUM=" - "
    fi

    case $pid in
        $APP) echo -e "${START}Application${END}  : $STATE ${WHITE}[$PIDNUM]${NC}" ;;
        $REB) echo -e "${START}Rebooter${END}     : $STATE ${WHITE}[$PIDNUM]${NC}" ;;
        $SYS) echo -e "${START}System${END}       : $STATE ${WHITE}[$PIDNUM]${NC}" ;;
        $SUP) echo -e "${START}Supervisor${END}   : $STATE ${WHITE}[$PIDNUM]${NC}" ;;
    esac
done

echo -e "${START}Reboot Timer${END} : ${PURPLE}`cat ${DIR}/src/timer`${NC} sec"
echo -e $WRAPPER_TAIL
