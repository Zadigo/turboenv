from abc import ABC

from turboenv.typings import TypeTurboEnv


class BasePreset(ABC):
    def __init__(self, environ: TypeTurboEnv):
        self.environ = environ


class DjangoEnv(BasePreset):
    @property
    def debug(self):
        return self.environ.boolean("DEBUG", default=True)

    @property
    def debug_propagate_exceptions(self):
        return self.environ.boolean("DEBUG_PROPAGATE_EXCEPTIONS")

    @property
    def email_backend(self):
        return self.environ.string("EMAIL_BACKEND")

    @property
    def email_host(self):
        return self.environ.string("EMAIL_HOST")

    @property
    def email_port(self):
        return self.environ.integer("EMAIL_PORT")

    @property
    def email_host_user(self):
        return self.environ.string("EMAIL_HOST_USER")

    @property
    def email_host_password(self):
        return self.environ.string("EMAIL_HOST_PASSWORD")

    @property
    def email_use_tls(self):
        return self.environ.boolean("EMAIL_USE_TLS")

    @property
    def email_use_ssl(self):
        return self.environ.boolean("EMAIL_USE_SSL")

    @property
    def email_ssl_certfil(self):
        return self.environ.string("EMAIL_SSL_CERTFILE")

    @property
    def email_ssl_key(self):
        return self.environ.integer("EMAIL_SSL_KEYFILE")

    @property
    def email_timeout(self):
        return self.environ.integer("EMAIL_TIMEOUT")

    @property
    def default_from_email(self):
        return self.environ.string("DEFAULT_FROM_EMAIL")

    @property
    def dissalowed_user_agents(self):
        return self.environ.str_list("DISSALOWED_USER_AGENTS")

    @property
    def email_use_localtime(self):
        return self.environ.boolean("EMAIL_USE_LOCALTIME")

    def admins(self, *emails: str):
        return self.environ.str_list("ADMINS", default=list(emails))

    def internal_ips(self, *ips: str):
        return self.environ.str_list("INTERNAL_IPS", default=list(ips))

    def allowed_hosts(self, *hosts: str):
        return self.environ.str_list("ALLOWED_HOSTS", default=list(hosts))

    def time_zone(self, default: str = "UTC"):
        return self.environ.string("TIME_ZONE", default=default)

    def use_timezone(self, default: bool = True):
        return self.environ.boolean("USE_TZ", default=default)

    def language_code(self, default: str = "en-us"):
        return self.environ.string("LANGUAGE_CODE", default=default)

    def use_i18n(self, default: bool = True):
        return self.environ.boolean("USE_I18N", default=default)

    def locales_paths(self, *paths: str):
        return self.environ.str_list("LOCALES_PATHS", default=list(paths))

    def language_cookie_name(self, default: str = "django_language"):
        return self.environ.string("LANGUAGE_COOKIE_NAME", default=default)

    def language_cookie_age(self, default: int | None = None):
        return self.environ.integer("LANGUAGE_COOKIE_AGE", default=default)

    def language_cookie_domain(self, default: str | None = None):
        return self.environ.string("LANGUAGE_COOKIE_DOMAIN", default=default)

    def language_cookie_path(self, default: str | None = None):
        return self.environ.string("LANGUAGE_COOKIE_PATH", default=default)

    def language_cookie_secure(self, default: bool = False):
        return self.environ.boolean("LANGUAGE_COOKIE_SECURE", default=default)

    def language_cookie_http_only(self, default: bool = False):
        return self.environ.boolean("LANGUAGE_COOKIE_HTTP_ONLY", default=default)

    def language_cookie_samesite(self, default: str | None = None):
        return self.environ.string("LANGUAGE_COOKIE_SAMESITE", default=default)

    def databases(self):
        return self.environ.json("DATABASES")

    def media_root(self, default: str | None = None):
        return self.environ.string("MEDIA_ROOT", default=default)

    def media_url(self, default: str | None = None):
        return self.environ.string("MEDIA_URL", default=default)

    def static_root(self, default: str | None = None):
        return self.environ.string("STATIC_ROOT", default=default)

    def static_url(self, default: str | None = None):
        return self.environ.string("STATIC_URL", default=default)

    def cache(self):
        return self.environ.json("CACHE")

    def redis_url(self, port: int = 6379, database: int = 0, production: bool = False):
        user = self.environ.string("REDIS_USER", default="")
        password = self.environ.string("REDIS_PASSWORD", default="")
        host = self.environ.string("REDIS_HOST", default="localhost")

        if (production or not self.debug) and host == 'localhost':
            raise ValueError("In production, the host cannot be 'localhost'")
          
        url = f"redis://{user}:{password}@{host}:{port}/{database}"
        # If the url is redis://:localhost:6479 for example,
        # remove the extract column ":"
        url = url.replace('/:', '/')
        self.environ(REDIS_URL=url)
        return url

    def cloudfront_url(self, default: str | None = None):
        return self.environ.string("CLOUDFRONT_URL", default=default)

    def aws_s3_url(self):
        self.environ(AWS_S3_URL='')
        self.environ.conditional('AWS_S3_URL').depends_on(['AWS_S3_REGION'])
        
        bucket_name = self.environ.string('AWS_S3_BUCKET_NAME')
        region = self.environ.string('AWS_S3_REGION')
        
        url = f'https://{bucket_name}.s3.{region}.amazonaws.com'
        self.environ(AWS_S3_URL=url)
        return url

    def rabbitmq_url(self, port: int = 5672, vhost: str = "/", host: str = "localhost", production: bool = False):
        user = self.environ.string("RABBITMQ_USER", default="guest")
        password = self.environ.string("RABBITMQ_PASSWORD", default="guest")

        if (production or not self.debug) and host == 'localhost':
            raise ValueError("In production, the host cannot be 'localhost'")
        
        url = f"amqp://{user}:{password}@{host}:{port}{vhost}"
        self.environ(RABBITMQ_URL=url)
        return url


class TurboEnvWithPresets:
    def __init__(self, environ: TypeTurboEnv):
        self.environ = environ

    @property
    def django(self) -> DjangoEnv:
        return DjangoEnv(self.environ)

