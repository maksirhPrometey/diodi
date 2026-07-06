#!/usr/bin/env bash
# Встановлення Docker Engine + Compose на Ubuntu 24.04 (один раз на Droplet)
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Запусти від root: sudo bash deploy/docker/install-docker.sh"
  exit 1
fi

apt-get update
apt-get install -y ca-certificates curl

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${VERSION_CODENAME:-$VERSION_ID}") stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker

echo "==> Docker $(docker --version)"
echo "==> Compose $(docker compose version)"
