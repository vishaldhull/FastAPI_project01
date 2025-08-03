import pytest

def test_equal_or_not_equal():
    assert 2 ==2
    assert 2 != 3

def test_is_instance():
    assert isinstance("hello", str)
    assert not isinstance(123, str)

def test_boolean():
    validation = True
    assert validation is True
    assert ('hello' == 'world') is False


def test_type():
    assert type("hello" is str)
    assert type('World' is not int)


def test_greater_and_less_than():
    assert 5>3
    assert 2 < 4


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]       
    assert 3 in num_list
    assert 6 not in num_list
    assert all(num_list) is True
    assert any(any_list) is False


class Student:
    def __init__(self, first_name: str, last_name:str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student("Jane", "Doe", "Computer Science", 4)

def test_person_initilization(default_employee):
    assert default_employee.first_name == "Jane"
    assert default_employee.last_name == "Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 4



