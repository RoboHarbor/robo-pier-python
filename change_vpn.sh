#!/usr/bin/env bash

# read $PROTONVPN_USERNAME and $PROTONVPN_PASSWORD from arguments
PROTONVPN_USERNAME=$1
PROTONVPN_PASSWORD=$2
VPN_COUNTRY=$3

# check if ENABLE_PROTONVPN is set to "true"
if [ "$ENABLE_PROTONVPN" = "true" ]; then
    service openvpn stop
    echo "Enabling ProtonVPN"
    # write login credentials to file
    bash -c "echo $PROTONVPN_USERNAME > /etc/openvpn/credentials"
    bash -c "echo $PROTONVPN_PASSWORD >> /etc/openvpn/credentials"
    MY_IP=$(curl -4 icanhazip.com)
    # we iterate over the protonvpn config files and copy a random one to the openvpn directory until the
    # command 'curl -4 icanhazip.com' does not return my own ip or crashes
    while true; do
        cp /etc/openvpn/protonvpn/${VPN_COUNTRY}/$(ls /etc/openvpn/protonvpn/${VPN_COUNTRY} | shuf -n 1) /etc/openvpn/client.conf
        bash -c "echo 'auth-user-pass /etc/openvpn/credentials' >> /etc/openvpn/client.conf"
        # add ignore local traffic of example for kubernetes
        bash -c "echo 'route 10.233.0.0 255.255.0.0 net_gateway' >> /etc/openvpn/client.conf"
        bash -c "echo 'dhcp-option DNS 10.233.0.3' >> /etc/openvpn/client.conf"
        service openvpn start
        sleep 8
        # get the new ip and when command crashes we stop the openvpn service
        # but when the command crashes then use MY_IP as defualt to run a restart
        NEW_IP=$(curl -4 icanhazip.com || echo $MY_IP)
        # if the new ip is different from my ip, we break the loop
        if [ "$NEW_IP" != "$MY_IP" ]; then
            break
        fi
        service openvpn stop
    done

fi