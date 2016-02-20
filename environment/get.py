import environment.trading_plans.develop
import environment.trading_plans.testing

import environment.connections.develop
import environment.connections.testing

import environment.db_spec.develop
import environment.db_spec.testing

env = None

def get_trading_plan():
    if env is None:
        raise EnvironmentNotSetError
    print(env)
    if env == 0: return environment.trading_plans.develop.plan
    if env == 1: return environment.trading_plans.testing.plan

def get_connections():
    if env is None:
        raise EnvironmentNotSetError
    print(env)
    if env == 0: return environment.connections.develop.connections
    if env == 1: return environment.connections.testing.connections

def get_db_spec():
    if env is None:
        raise EnvironmentNotSetError
    print(env)
    if env == 0: return environment.db_spec.develop
    if env == 1: return environment.db_spec.testing

def set_environment(new_env):
    global env
    env = new_env

class EnvironmentNotSetError(Exception):
    pass
