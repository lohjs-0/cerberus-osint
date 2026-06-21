#!/usr/bin/env bash

R='\033[0;31m'
DR='\033[2;31m'
BR='\033[1;31m'
D='\033[2;37m'
W='\033[1;37m'
X='\033[0m'
BL='\033[5m'

glitch_line() {
    local text="$1"
    local glitch_chars=('█' '▓' '░' '▒' '╬' '╪' '#' '@' '%' '&')
    local len=${#text}
    for pass in 1 2; do
        echo -ne "\r\033[K${DR}"
        for ((i=0; i<len; i++)); do
            if (( RANDOM % 4 == 0 )); then
                echo -ne "${glitch_chars[$((RANDOM % ${#glitch_chars[@]}))]}"
            else
                echo -ne "${text:$i:1}"
            fi
        done
        echo -ne "${X}"
        sleep 0.05
    done
    echo -e "\r\033[K${R}${text}${X}"
}

flicker() {
    local text="$1"
    echo -ne "\r\033[K${DR}${text}${X}"; sleep 0.06
    echo -ne "\r\033[K${BR}${text}${X}"; sleep 0.06
    echo -e  "\r\033[K${R}${text}${X}"
}

get_info() {
    USER_NAME="$(whoami)"
    HOST_NAME="$(hostname)"
    OS_NAME="$(uname -s)"
    KERNEL="$(uname -r | cut -d'-' -f1)"

    if [[ "$OSTYPE" == "linux-android"* ]] || [ -d "/data/data/com.termux" ]; then
        ENV_TAG="termux"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        ENV_TAG="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        ENV_TAG="macos"
    else
        ENV_TAG="unknown"
    fi
}

ART=(
"              .-@W=                                       "
"              #WWWW-                                      "
"              *WWWWW*-.                        -++-       "
"      :       -WWWWWWW%.                      .#WW%-      "
"      **:     .WWWWWWWW%.                     +WWW=       "
"      :WW#-    *WWWWWWWW*                     :%WW:       "
"     .-#WWW#=.  %WWWWWW=#.                    .*@*-..     "
"    -@WWWWWWWW#:=WWWWWW:  .                      .-++**+. "
"  .-#WWWWWWWWWWWW%WWWWWW%--..           .....         :*@ "
".+WWWWWWWWWWWWWWWWWWWWWWWWWWW#*=-:::-=+*#%@WW%#*+-.    @*"
" =#%###++*%WWWWWWWWWWWWWWWWWWWWWWWW@@@WWWWWWWWWW@*==*#*-."
"           .-*WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW*..    "
"  .-+==-+#%+. =WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%:    "
" =W@@@%WWWWWWWWW%%%@WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW@:  "
"  +WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%@WWWWWWWWWWWWWWW@: "
"    +WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW%::%WWWWW@+%WWWWWWW+  "
"   .:@WWWW@#*#%@@WWWWWWWWWWWWWWWWWWW%.  =%WWWW+  .+*%@WW% "
"  .*W%+:..       .::=#WWWWWWWWWWWWWW#    .=%WWW*    .=@WW* "
"   .:               *WWW##=#%%@@@#+@WWW:   .@WW*     -WWW: "
"                  .#WW%- .  .....  @WW*     %WW:     +WW*  "
"                 :%WW=            -WW@.     #WW.    .@W@.  "
"              ..+WW%=             #WW*   .:-@W#      =WW@. "
"            +@@WWW+            .-*WWW-   *@W@#.    :%WWW*  "
"            :=+=-.            .#@WWW*.   ....      .:-::   "
"                               ..:-.                       "
)

clear
get_info

for i in 1 2 3; do
    echo -e "${DR}  $(head -c 80 /dev/urandom | tr -dc 'A-Z0-9@#%&!' | head -c 55)${X}"
    sleep 0.04
done
sleep 0.05
clear

echo ""
for line in "${ART[@]}"; do
    echo -e "${R}${line}${X}"
done
sleep 0.1

echo ""
glitch_line "    ___          _                         "
glitch_line "  / __\\___ _ __| |__   ___ _ __ _   _ ___ "
glitch_line " / /  / _ \\ '__| '_ \\ / _ \\ '__| | | / __|"
glitch_line "/ /__|  __/ |  | |_) |  __/ |  | |_| \\__ \\\\"
glitch_line "\\____/\\___|_|  |_.__/ \\___|_|   \\__,_|___/ "
echo ""

flicker "  ══════════════════════════════════════"
echo -e "${DR}        three heads.  one judgment.  no mercy.${X}"
flicker "  ══════════════════════════════════════"
echo ""
sleep 0.2

echo -e "${DR}  ┌─ soul recognized ──────────────────────┐${X}"
sleep 0.08
echo -e "${DR}  │  ${D}operator  ${R}${USER_NAME}${DR}@${R}${HOST_NAME}${X}"
sleep 0.08
echo -e "${DR}  │  ${D}environ   ${R}${ENV_TAG}${X}"
sleep 0.08
echo -e "${DR}  │  ${D}kernel    ${R}${KERNEL}${X}"
sleep 0.08
echo -e "${DR}  │  ${D}version   ${R}v1.3.0${X}"
sleep 0.08
echo -e "${DR}  └────────────────────────────────────────┘${X}"
echo ""
sleep 0.15

echo -e "${DR}  you may pass.${X}"
sleep 0.3
echo -e "${DR}  use only on authorized targets.${X}"
echo -e "${DR}  all souls pass through here.${X}"
echo ""
sleep 0.3
