#!/bin/bash
mkdir -p /config/.pki/nssdb
[ -f /config/.pki/nssdb/cert9.db ] || certutil -d sql:/config/.pki/nssdb -N --empty-password
certutil -d sql:/config/.pki/nssdb -D -n "CA Laboratorio CAI4" 2>/dev/null
certutil -d sql:/config/.pki/nssdb -A -t "C,," -n "CA Laboratorio CAI4" -i /certs/ca.crt
chown -R abc:abc /config/.pki
echo "CA del laboratorio importada"
