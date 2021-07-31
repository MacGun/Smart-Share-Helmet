TARGET="$1"
PID=`ps -ef | grep $TARGET | grep -v grep | awk '{print $2}' | head -n1`
if [ -n "$PID" ]; then
    kill $PID
    TTY=`tty`
    IFS="/"
    read -a strarr <<< "$TTY"
    MYTTY="${strarr[2]}${strarr[3]}"
    echo "kill: $PID | process_name: $TARGET"
    wall "$(whoami)($MYTTY) killed $TARGET [$PID]"
else
    echo "$TARGET: The corresponding process does not exist."
fi
