# PersonalPass
Маленкий генератор паролей.

Работу проверял только на ОС Linux, возможно работает и по Windows ;)

## Usage

PersonalPass.py [-h]
                [--version]
                [--file FILE]
                [--len LEN]
                [--digits]
                [--special]
                resource

* file - Файл ключ, для геннерации пароля.
* len - Длина пароля
* digits - Обязательное наличие цифр
* special - Обязателное наличие спец. символов

### PersonalPass.cfg

`nano ~/.PersonalPass/PersonalPass.cfg`

или

`vim ~/.PersonalPass/PersonalPass.cfg`

```
[<resource>] or [default]
len = integer
file = path
digits = str2bool('true', '1', 't', 'y', 'yes')
special = str2bool('true', '1', 't', 'y', 'yes')
```

## install
**Only Python3**

`python setup.py build && python setup.py install`