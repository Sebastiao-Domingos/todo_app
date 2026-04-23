#!/bin/bash
# Executado pela Vercel durante cada deploy
echo "==> Instalando dependencias..."
pip install -r requirements.txt
echo "==> Recolhendo ficheiros estaticos..."
python manage.py collectstatic --noinput
echo "==> Aplicando migracoes..."
python manage.py migrate --noinput
echo "==> Build concluido!"