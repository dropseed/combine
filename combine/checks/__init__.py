from .runner import CheckRunner

# Import these to force registration of checks
import combine.checks.empty_build  # NOQA
import combine.checks.seo  # NOQA
import combine.checks.src  # NOQA


__all__ = ['CheckRunner']
