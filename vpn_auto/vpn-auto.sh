#!/bin/bash

client_pid=$(pgrep "Cisco AnyConnect Secure Mobility Client")
vpn_state=$(/opt/cisco/anyconnect/bin/vpn state | grep -c "state: Connected")
vpn_host=${VPN_HOST}
vpn_username=${VPN_USERNAME:-$USER}
vpn_keychain_service=${VPN_KEYCHAIN_SERVICE:=VPN}

echo "$vpn_keychain_service"
echo "$vpn_username"

vpn_password=$(security find-generic-password -w -s "${vpn_keychain_service}" -a "${vpn_username}")

if [[ -z "${vpn_password}" ]]; then
	echo "[ERROR] VPN password was not found in the keychain"
	exit 1
elif [[ -z "${vpn_host}" ]]; then
    echo "[ERROR] VPN hostname was not specified (Did you forget to set VPN_HOST?)"
    exit 1
fi

if [[ $client_pid != 0 ]]; then
	echo "[INFO] Killing running AnyConnect client..."
	kill -9 ${client_pid}
fi

if [[ $vpn_state != 0 ]]; then
	echo "[INFO] Connected to VPN, disconnecting"
	/opt/cisco/anyconnect/bin/vpn disconnect
fi

echo "[INFO] Starting VPN Connection..."
/opt/cisco/anyconnect/bin/vpn -s <<EOF
connect ${vpn_host}
${vpn_username}
${vpn_password}
exit
EOF

echo "[INFO] Starting AnyConnect client..."
osascript -e 'run application "Cisco AnyConnect Secure Mobility Client"'