from abc import ABC, abstractmethod

# We start by creating some abstract ingredients.
# These will be extended by each region-specific ingredients


class Dough:
    pass


class Sauce:
    pass


class Cheese:
    pass


class Pepperoni:
    pass

# Normally, in OO languages such as Java, the abstract factory
# is implemented through interfaces. However because we don't
# have those in Python, we will use abstract classes instead.


class PizzaIngredientFactory(ABC):
    @abstractmethod
    def createDough() -> Dough:
        pass

    @abstractmethod
    def createSauce() -> Sauce:
        pass

    @abstractmethod
    def createCheese() -> Cheese:
        pass

    @abstractmethod
    def createPepperoni() -> Pepperoni:
        pass

# Before creating the concrete region-specific PizzaIgredientFactories
# we need to create some concrete ingredients by extending the abstract
# ingredient classes


class ThinCrustDough(Dough):
    pass


class MarinaraSauce(Sauce):
    pass


class ReggianoCheese(Cheese):
    pass


class SlicedPepperoni(Pepperoni):
    pass

# We now have everything we need to create the concrete New York
# PizzaIngredientFactory:


class NYPizzaIngredientFactory(PizzaIngredientFactory):
    def createDough(self):
        return ThinCrustDough()

    def createSauce(self):
        return MarinaraSauce()

    def createCheese(self):
        return ReggianoCheese()

    def createPepperoni(self):
        return SlicedPepperoni()

# The next step is to modify our abstract Pizza class so that
# it uses our newly created ingredients


class Pizza(ABC):

    # We add here the dependency ingredients
    dough: Dough
    sauce: Sauce
    cheese: Cheese
    pepperoni: Pepperoni

    @abstractmethod
    def prepare(self):
        pass

    def bake(self):
        print("baking pizza for 12min in 400 degrees..")

    def cut(self):
        print("cutting pizza in pieces")

    def box(self):
        print("putting pizza in box")


# Now we can create some concrete Pizzas. Note that all pizzas
# will have an PizzaIngredientFactory dependency that will be
# responsible for creating all the proper ingredients:
class CheesePizza(Pizza):
    ingredientFactory: PizzaIngredientFactory

    def __init__(self, ingredientFactory: PizzaIngredientFactory):
        self.ingredientFactory = ingredientFactory

    # We also need to override the prepare() abstract method:

    def prepare(self):
        # Since this is a CheesePizza we don't put any pepperoni:
        self.dough = self.ingredientFactory.createDough()
        self.sauce = self.ingredientFactory.createSauce()
        self.cheese = self.ingredientFactory.createCheese()

# The PizzaStore remains unchanged (same as in the Factory Method pattern)


class PizzaStore(ABC):

    @abstractmethod
    def _createPizza(self, pizzaType: str) -> Pizza:
        pass

    def orderPizza(self, pizzaType):
        pizza: Pizza

        pizza = self._createPizza(pizzaType)

        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()


# Remember that PizzaStore calls the prepare(), bake(), etc in the orderPizza
# so here we only need to override the _createPizza method:
class NYPizzaStore(PizzaStore):

    def _createPizza(self, pizzaType: str) -> Pizza:
        pizza: Pizza = None
        ingredientFactory: PizzaIngredientFactory = NYPizzaIngredientFactory()

        if pizzaType == 'Greek':
            # Prepare the greek pizza here after creating
            # the proper ingredients and then the GreekPizza
            pass
        elif pizzaType == 'Cheese':
            pizza = CheesePizza(ingredientFactory)
        else:
            print("No matching pizza found in the NY pizza store...")

        return pizza


store = NYPizzaStore()

store.orderPizza('Cheese')
