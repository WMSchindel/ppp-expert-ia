from src.core.config.environments import Environment

print(Environment.DEVELOPMENT)
print(Environment.DEVELOPMENT.value)
print(Environment.TEST.value)
print(Environment.PRODUCTION.value)

print(type(Environment.DEVELOPMENT))
print(isinstance(Environment.DEVELOPMENT, str))