# All attributes and methods are public

class Person(object): # inherits from object
    """My first class"""
    # Constructor
    def __init__(self, input_name, *args, **kwargs):
        self.__name = input_name
        return super().__init__(*args, **kwargs)

    def Exclaim(this):
        print('I\'m a person')

    # Property: Option 1
    def get_name(self):
        print('getter')
        return self.__name

    def set_name(self, input_name):
        print('setter')
        self.__name = input_name

    name = property(get_name, set_name)

# Inheritance
class JDPerson(Person):
    def __init__(self, name, birthdate, *args, **kwargs):
        super().__init__(name)
        self.__name = name + ', Esquire'
        self.__birthdate = birthdate

    @property
    def Age(this):
        return 80

class MDPerson(Person):
    count = 0 # created 1 time and shared across instances (like static)

    # Override
    def __init__(self, name, email, *args, **kwargs):
        super().__init__(name)
        MDPerson.count += 1 # class attribute
        self.__name = 'Dr. ' + name
        self.__email = email

    def Exclaim(this):
        print('I\'m a doctor')

    # Property: Option 2
    # Use over public attributes (self.*) when additional validation/behavior is required.
    @property
    def email(self):
        print('getter')
        return self.__email

    @email.setter
    def email(self, email):
        print('setter')
        self.__email = email

    # Class method: can be used to define alternative constructors for your classes.
    @classmethod
    def classMethod(cls):
        print("class method call: " + str(cls.count))

    # Static method
    @staticmethod
    def staticMethod():
        print("static method call")

    # Operator overloads
    def __eq__(self, person2):
        return self.name == person2.name

    def __str__(self): # like ToString
        return self.name

# Custom iterator class
class ReadVisits(object):
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)

# Allows an object to be called like a function
class BetterCountMissing(object):
    def __init__(self):
        self.added = 0

    def __call__(self):
        self.added += 1
        return 0

counter = BetterCountMissing()
print(counter())

# Use modules
from crack import linkedlist

print(linkedlist.node(7))