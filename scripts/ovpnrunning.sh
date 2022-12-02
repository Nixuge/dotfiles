#!/bin/bash

if [[ "$(pgrep openvpn)" -eq 0 ]] ; then
    echo ""
    exit 0
fi
echo 

