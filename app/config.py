from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix='X5TEST',
    settings_files=['./app/settings.yaml'],
    core_loaders=['YAML'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.
