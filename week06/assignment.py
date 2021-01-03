from abc import ABCMeta

# 动物


class Animal(metaclass=ABCMeta):
    def __init__(self, food_type, body_size, character):
        self.food_type = food_type
        self.body_size = body_size
        self.character = character

    @property
    def is_fierce(self):
        return self.body_size != '小' and self.food_type == '食肉' and self.character == '凶猛'

# 猫


class Cat(Animal):
    sound = 'Meow'

    def __init__(self, name, food_type, body_size, character):
        super().__init__(food_type, body_size, character)
        self.name = name

    @property
    def is_pettable(self):
        return not self.is_fierce

# 狗


class Dog(Animal):
    sound = 'Bark'

    def __init__(self, name, food_type, body_size, character):
        super().__init__(food_type, body_size, character)
        self.name = name

    @property
    def is_pettable(self):
        return not self.is_fierce

# 动物园类


class Zoo(object):
    def __init__(self, name):
        self.name = name
        # 使用set防止单个动物实例增加多次
        self.animals = set()

    def add_animal(self, animal):
        # 同一只动物只会记录一次
        self.animals.add(animal)
        # 用类名作为属性名，支持hasattr
        self.__setattr__(type(animal).__name__, True)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    print(z.__dict__)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
