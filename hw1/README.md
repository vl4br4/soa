# Сереализация/Десереализация на C++

Сборка:
``
    docker build -t cpp_sd .
``

Затем
``
    docker-compose up
``

Для запроса к приложению можно использовать утилиту curl:
    
    curl -XGET http://localhost:2000/get_result?method={метод сериализации}

Список доступных методов: "NATIVE", "XML", "JSON", "YAML", "AVRO", "MPACK"

``
!написание метода не чувствительно к регистру!
``

сборка без докера: без докера создать папку hw1/build и из нее выполнить cmake .. && make

make_query.py - утилита для запросов: python3 make_query.py {название метода}
