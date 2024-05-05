## Запуск контейнера nominatim с дампом России

--- 
### docker-compose.yml
```
volumes:
  nominatim-data:

services:
  backend:
    build: .
    ports:
      - "8081:8080"
    ...
    links:
      - "nominatim"
    depends_on:
      ...
      nominatim:
        condition: service_started
    ...
  
  ...
  
  nominatim:
    container_name: nominatim
    image: mediagis/nominatim:4.4
    restart: always
    ports:
      - "8091:8080"
    environment:
      # more info here https://github.com/mediagis/nominatim-docker/tree/master/4.4
      PBF_URL: https://download.geofabrik.de/russia-latest.osm.pbf
      FREEZE: true
      IMPORT_STYLE: address
    volumes:
      - nominatim-data:/var/lib/postgresql/14/main
    shm_size: 2gb
```

### src/bot/config.py
В ```nominatim_URL``` заменить ```http://nominatim.openstreetmap.org``` на ```http://nominatim:8080```.

---
### Тестирование запросов вручную в браузере при запущенном контейнере 
```
http://localhost:8091/reverse?format=json&lat=55.7505412&lon=37.6174782
http://localhost:8091/search?city={Мытищи}
```

