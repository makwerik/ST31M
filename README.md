<h1>Бот для восстановления пароля в STEAM</h1>
<h3>Использование:</h3>
<code>pip install -r req.txt</code>
<p>options_driver.py - настройки браузера</p>
<p>numbers.txt -  здесь указываем нужный номер</p>
<p>general.py - внутри указываем данные в поля api_key='' от рукапчи, site_key='' ключ сайта с капчей</p>
<h3>После запускаем скрипт: <code>python general.py</code></h3>
<p>Результат исполения смотрим тут /maim/data/result.txt</p>

p.s Если нет расшерения от рукапчи, то в general.py нужно вместо вызова метода "__solver_captcha_extension"
, поменять на "__solver_captcha"