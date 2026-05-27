#!/bin/bash
# setup-chapan.sh — деплой сайта Чапан на chapan.aslankaa.com через Caddy
# ЗАПУСК (на ai-server): sudo bash ~/setup-chapan.sh
set -euo pipefail

if [ "$EUID" -ne 0 ]; then
    echo "ERROR: требуется sudo. Запусти: sudo bash ~/setup-chapan.sh"; exit 1
fi

CHAPAN_TARGET=/srv/zs/chapan
CHAPAN_SRC=/home/adminai/chapan-www
CADDYFILE=/srv/caddy/conf/Caddyfile

echo "=== Чапан · деплой на chapan.aslankaa.com ==="

# 1. Развёртывание сайта
mkdir -p "$CHAPAN_TARGET"
cp -rf "$CHAPAN_SRC/." "$CHAPAN_TARGET/"
chown -R root:root "$CHAPAN_TARGET"
echo "✓ Сайт скопирован в $CHAPAN_TARGET ($(du -sh "$CHAPAN_TARGET" | cut -f1))"
echo "  Структура: $(ls "$CHAPAN_TARGET" | tr '\n' ' ')"

# 2. Caddyfile — добавить блок если ещё нет
if ! grep -q "chapan.aslankaa.com" "$CADDYFILE"; then
    cat >> "$CADDYFILE" <<'EOF'

chapan.aslankaa.com, www.chapan.aslankaa.com {
    root * /srv/zs/chapan
    try_files {path} {path}/ /index.html
    file_server
    encode gzip zstd
    header /assets/* Cache-Control "public, max-age=86400"
    header / Cache-Control "public, max-age=300"
    log {
        output file /var/log/caddy/chapan.log
        format console
    }
}
EOF
    echo "✓ Блок chapan.aslankaa.com добавлен в $CADDYFILE"
else
    echo "= Блок chapan.aslankaa.com уже в Caddyfile (пропускаем)"
fi

# 3. Валидация и reload Caddy
echo ""
echo "--- Caddy validate ---"
if docker exec caddy caddy validate --config /etc/caddy/Caddyfile; then
    echo "✓ Caddyfile валиден"
else
    echo "✗ Caddyfile невалиден — проверь $CADDYFILE и исправь"
    exit 1
fi

echo "--- Caddy reload ---"
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
echo "✓ Caddy перезагружен"

# 4. Финальный статус
echo ""
echo "=== ГОТОВО ==="
echo ""
echo "На сервере:"
echo "  Файлы:     $CHAPAN_TARGET ($(du -sh "$CHAPAN_TARGET" | cut -f1))"
echo "  Caddyfile: добавлен блок chapan.aslankaa.com"
echo ""
echo "Что осталось (вне ai-server):"
echo "  1. DNS на reg.ru: добавить A-запись"
echo "       subdomain: chapan"
echo "       domain:    aslankaa.com"
echo "       IP:        45.10.142.253"
echo "       TTL:       3600 (по умолчанию)"
echo ""
echo "  2. После пропагации DNS (5–30 мин) Caddy автоматически получит Let's Encrypt сертификат."
echo ""
echo "Проверка через 5 мин:"
echo "  curl -I https://chapan.aslankaa.com/"
echo ""
echo "Лог Caddy для отладки:"
echo "  docker logs caddy --tail 50 -f"
