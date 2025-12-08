#!/bin/bash
set -e

echo "SSHing to PythonAnywhere..."

sshpass -p "$PA_PASSWORD" ssh -o StrictHostKeyChecking=no $PA_USERNAME@ssh.pythonanywhere.com << EOF
    cd /home/emu86/Emu86
    git pull origin master
    ./myutils/prod.sh
EOF

echo "Deployment complete."