from django.apps import AppConfig
from django.core.cache import cache

from .errors import BAD_CONFIG_ERROR
from .utils import STATS_FILE_CACHE_KEY


def webpack_cfg_check(app_configs, **kwargs):
    from django.conf import settings

    check_failed = False
    user_config = getattr(settings, 'WEBPACK_LOADER', {})
    try:
        user_config = [dict({}, **cfg) for cfg in user_config.values()]
    except TypeError:
        check_failed = True

    errors = []
    if check_failed:
        errors.append(BAD_CONFIG_ERROR)
    return errors


class WebpackLoaderConfig(AppConfig):
    name = 'webpack_loader'
    verbose_name = "Webpack Loader"

    def ready(self):
        from django.core.checks import register, Tags
        register(Tags.compatibility)(webpack_cfg_check)

        # Invalidate stats file cache
        cache.delete(STATS_FILE_CACHE_KEY)
