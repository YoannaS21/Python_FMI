CONCRETE = 2500
BRICK = 2000
STONE = 1600
WOOD = 600
STEEL = 7700


class Material:
    def __init__(self, mass, density):
        self.mass = mass
        self.density = density
        self._used = False
        self._number_of_materials_in_it = 1

    @property
    def volume(self):
        return self.mass / self.density

    def is_used(self):
        if self._used:
            raise AssertionError
        self._used = True


class Concrete(Material):
    def __init__(self, mass):
        super().__init__(mass, CONCRETE)


class Brick(Material):
    def __init__(self, mass):
        super().__init__(mass, BRICK)


class Stone(Material):
    def __init__(self, mass):
        super().__init__(mass, STONE)


class Wood(Material):
    def __init__(self, mass):
        super().__init__(mass, WOOD)


class Steel(Material):
    def __init__(self, mass):
        super().__init__(mass, STEEL)


class Factory:

    MATERIAL_NAMES = {
        "Brick": Brick,
        "Concrete": Concrete,
        "Stone": Stone,
        "Wood": Wood,
        "Steel": Steel,
    }

    all_created_materials = []

    def __init__(self):
        self.created_materials = []

    def _create_class_name_from_materials(self, materials):
        class_names = []
        for material in materials:
            class_name = type(material).__name__
            class_names.extend(class_name.split("_"))

        sorted_class_names = sorted(class_names)
        return "_".join(sorted_class_names)

    def _calculate_density_and_ingredients(self, materials):
        new_class_density = 0
        number_ingredients = 0
        for material in materials:
            new_class_density += material.density * material._number_of_materials_in_it
            number_ingredients += material._number_of_materials_in_it
        new_class_density /= number_ingredients
        return new_class_density, number_ingredients

    def _create_new_class(self, class_name, density):
        new_class = type(class_name, (Material,), {
            '__init__': lambda self, mass: super(type(self), self).__init__(mass, density)
        })
        self.MATERIAL_NAMES[class_name] = new_class
        return new_class

    def _handle_kwargs(self, kwargs):
        result = []
        for material_name, material_mass in kwargs.items():
            if (material_name in self.MATERIAL_NAMES):
                material_instance = self.MATERIAL_NAMES[material_name](material_mass)
                self.created_materials.append(material_instance)
                Factory.all_created_materials.append(material_instance)
                result.append(material_instance)
            else:
                raise ValueError
        return tuple(result)

    def _handle_args(self, args):
        temp_used_materials = []

        try:
            for material in args:
                material.is_used()
                temp_used_materials.append(material)

            class_name = self._create_class_name_from_materials(args)

            if class_name in self.MATERIAL_NAMES:
                new_mass = sum(material.mass for material in args)
                result_material = self.MATERIAL_NAMES[class_name](new_mass)
                self.created_materials.append(result_material)
                Factory.all_created_materials.append(result_material)
                return result_material
            else:
                new_class_density, number_ingredients = self._calculate_density_and_ingredients(args)
                new_class = self._create_new_class(class_name, new_class_density)
                new_mass = sum(material.mass for material in args)
                result_material = new_class(new_mass)
                result_material._number_of_materials_in_it = number_ingredients
                self.created_materials.append(result_material)
                Factory.all_created_materials.append(result_material)
                return result_material

        except AssertionError as e:
            for material in temp_used_materials:
                material._used = False
            raise e

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise ValueError
        if not args and not kwargs:
            raise ValueError

        self.created_materials.clear()

        if kwargs:
            return self._handle_kwargs(kwargs)

        if args:
            return self._handle_args(args)

    def can_build(self, needed_volume):
        total_volume = sum(
            material.volume for material in self.created_materials)
        return total_volume >= needed_volume

    @classmethod
    def can_build_together(cls, needed_volume):
        total_volume = sum(
            material.volume for material in cls.all_created_materials)
        return total_volume >= needed_volume

