class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration,
                 distance, speed, calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {format(self.duration,".3f")} ч.; '
                f'Дистанция: {format(self.distance, ".3f")} км; '
                f'Ср. скорость: {format(self.speed, ".3f")} км/ч; '
                f'Потрачено ккал: {format(self.calories, ".3f")}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.LEN_STEP * self.action / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__, self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        energy = ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                  * self.weight / self.M_IN_KM * self.duration * 60)
        return energy


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        energy = ((coeff_calorie_1 * self.weight + (self.get_mean_speed() **
                                                    2 // self.height) * coeff_calorie_2 *
                   self.weight) * self.duration * 60)
        return energy


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.length_pool * self.count_pool /
                 self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        energy = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return energy

    def __name__(self):
        pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type == 'SWM':
        training = dictionary[workout_type](action=data[0], duration=data[1],
                                            weight=data[2], length_pool=data[3],
                                            count_pool=data[4])
        return training
    elif workout_type == 'RUN':
        training = dictionary[workout_type](action=data[0], duration=data[1],
                                            weight=data[2])
        return training
    elif workout_type == 'WLK':
        training = dictionary[workout_type](action=data[0], duration=data[1],
                                            weight=data[2], height=data[3])
        return training


def main(training: Training):
    """Главная функция."""
    info = training.show_training_info()
    result = info.get_message()
    print(result)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
