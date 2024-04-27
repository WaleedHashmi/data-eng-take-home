import pytest
from tomorrow.utils import camel_to_snake

@pytest.mark.parametrize("input_str, expected_output", [
    ("temperatureMin", "temperature_min"),
    ("temperatureMax", "temperature_max"),
    ("cloudMax", "cloud_max"),
    ("someVariable", "some_variable"),
    ("AnotherVariable", "another_variable"),
    ("YetAnotherOne", "yet_another_one"),
])
def test_camel_to_snake(input_str, expected_output):
    assert camel_to_snake(input_str) == expected_output

    