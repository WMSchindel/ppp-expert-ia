from core.config.environments import Environment


def test_environment_values():
    assert Environment.DEVELOPMENT.value == "development"
    assert Environment.TEST.value == "test"
    assert Environment.PRODUCTION.value == "production"

    print(Environment.DEVELOPMENT)
    print(type(Environment.DEVELOPMENT))
    print(isinstance(Environment.DEVELOPMENT, str))
    print(Environment.DEVELOPMENT.value)