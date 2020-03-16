# Python Design Patterns

- [](https://plantuml.com/zh/class-diagram)

## The Factory
- [Python Design Patterns: -03- The Factory](https://medium.com/@mrfksiv/python-design-patterns-03-the-factory-86cb351c68b0)
- [simple_factory.py](./simple_factory.py)
- [factory_method.py](./factory_method.py) [factory-method example](https://refactoringguru.cn/design-patterns/abstract-factory/python/example)
- [abstract_factory.py](./abstract_factory.py) [abstract-factory example](https://refactoringguru.cn/design-patterns/abstract-factory/python/example)

## Bridge
''Bridge'' is a structural design pattern that divides business logic or huge class into separate class hierarchies that can be developed independently.

- [pazdera/bridge.py](https://gist.github.com/pazdera/1173009) python 2 implementation
- [Bridge in Python](https://sourcemaking.com/design_patterns/bridge/python/1)
- [Bridge pattern in Python](https://www.giacomodebidda.com/bridge-pattern-in-python/)

``plantuml
@startuml
'Class Diagram for Bridge Design Pattern

Website <|-- FreeWebsite
Website <|-- PaidWebsite

Website : __init__(self, implementation)
Website : show_page(self)

Implementation <|-- ImplementationA
Implementation <|-- ImplementationB

Implementation : get_excerpt(self)
Implementation : get_article(self)
Implementation : get_ads(self):

@enduml
``