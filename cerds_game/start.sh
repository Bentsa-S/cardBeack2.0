echo "Making migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server with Daphne (WebSocket support)..."
# Використовуємо PORT змінну Railway або 8000 за замовчуванням
daphne -b 0.0.0.0 -p ${PORT:-8000} cerds_game.asgi:application