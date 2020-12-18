# skillfactory-module-e9-shaidulov
Проект подготовлен для деплоя на хероку
Доступен по адресу:
https://skillfactory-events.herokuapp.com/index
Созданы два пользователя user1 с паролем 1 и user2 с паролем, соотсестсвенно, 2
Тестировать можно либо используя их, либо создав новых.

Также в конфиге приложения прописано SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
Но, sqlite используется только для отладки локально, на heroku прописано heroku addons:add heroku-postgresql:hobby-dev
