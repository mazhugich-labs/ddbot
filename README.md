# README.md

## Цель
Проверить практические навыки моделирования, программирования и интеграции сенсоров для автономного мобильного робота в симуляторе Gazebo с использованием ROS.

## Задача
В симуляторе Gazebo создать сцену и запрограммировать автономный проезд робота из точки А в точку Б с объездом препятствий. Робот должен использовать данные сенсоров: лидар или ультразвуковые датчики, камеру глубины (эмуляция Orbbec Astra), GPS.

## Исходные данные
- Робот: любой (TurtleBot3, Jackal или собственный URDF/Xacro).
- Обязательные сенсоры: 2D лидар или ультразвуковые дальномеры; камера глубины (depth camera plugin как аналог Orbbec Astra); GPS (gazebo_ros_gps).
- ROS 2 Humble (на выбор кандидата, зафиксировать в README). Симулятор Gazebo Classic или Ignition.
- Мир: плоская поверхность, несколько статических препятствий, обозначенные стартовая и финишная зоны.

## Требования к выполнению
1. Робот стартует из точки А и автономно доезжает до точки Б, не касаясь препятствий.
2. Маршрут задаётся waypoints в GPS-координатах или в системе координат мира.
3. Необходимо использовать ROS: узлы, топики, tf, launch-файлы.
4. Допускается использование готовых пакетов (nav2, gmapping, amcl, move_base), но кандидат должен понимать их настройку.
5. Код на Python или C++.
6. Записать демонстрационное видео (Gazebo + RViz) и, по возможности, rosbag.

## Этапы выполнения
1. [x] Выбрать или создать модель робота с сенсорами и плагинами.
2. [x] Создать мир в Gazebo с препятствиями и зонами старта/финиша.
3. [] Реализовать узлы ROS для:
    - [x] чтения данных сенсоров;
    - [x] построения карты или использования SLAM;
    - [] планирования пути и управления;
    - [] следования по GPS-точкам.
4. [] Запустить и отладить симуляцию.
5. [] Записать видео 1–3 минуты.
6. [] Оформить Git-репозиторий с README (инструкция запуска, зависимости, описание).

## Инструкция
Изменить параметры доступа к файла для работы с Docker:
```bash
chmod +x docker/{build,run,enter,stop}.sh
```

1. Забилдить контейнер:
```bash
docker/build.sh
```

2. Запустить контейнер:
```bash
docker/run.sh
```

3. Войти в контейнер:
```bash
docker/enter.sh
```

4. Остановить контейнер:
    - Выход из контейнера:
    ```bash
    exit
    ```
    - Остановка контейнера:
    ```bash
    docker/stop.sh
    ```

## Описание пакетов ROS 2

### ddbot_description
Содержит описание 4-колесного мобильного робота с дифференциальным приводом:
```bash
ros2 launch ddbot_description rviz.launch.py
```

![ddbot_description](assets/ddbot_description.png)

### ddbot_gazebo
Содержит описание контроллера дифференциального привода и датчиков (IMU, лидар, камера глубины, 4 псевдо ультразвуковых датчика, GPS):
```bash
ros2 launch ddbot_gazebo full.launch.py
```

https://github.com/user-attachments/assets/0318aa5d-25d0-43a8-b7bf-b422deb59c7f


> Мир с препятствиями построен благодаря [Dynamic World Generator Wizard](https://github.com/ali-pahlevani/Dynamic_World_Generator)

### ddbot_localization
Содержит реализацию системы комплексирования навигационных данных на основе пакета [robot_localization](https://github.com/cra-ros-pkg/robot_localization/tree/rolling-devel).

> **map** (GPS)->**odom** (кинематика + IMU)->**base_footprint**

```bash
ros2 launch ddbot_localization full.launch.py
```

https://github.com/user-attachments/assets/d12dfe32-a63f-4944-9cb6-ff804dec1cf6

### ddbot_slam
Содержит реализацию SLAM на основе slam_toolbox.
> **map**->**odom** исключительно на основе сопоставления сканов (без комплексирования GPS)

Режим SLAM:
```bash
ros2 launch ddbot_slam full.launch.py
```

https://github.com/user-attachments/assets/c9800de2-e6e5-4ad2-a33c-721f4c9a67e3

Режим локализации:
```bash
ros2 launch ddbot_slam full.launch.py set_localization_mode:=true
```

https://github.com/user-attachments/assets/6a12a04b-cc8b-4d8b-bee5-2b45483ea171

