from django.db import models


class ModelsRegistryHolder(object):
    _JOBS_REGISTRY = {}

    @classmethod
    def register(cls, job):
        cls._JOBS_REGISTRY[job.Meta.name] = job

    @classmethod
    def get(cls, job_name):
        return dict(cls._JOBS_REGISTRY)[job_name]

    @classmethod
    def get_jobs(cls):
        return dict(cls._JOBS_REGISTRY)

    @classmethod
    def is_registered(cls, job_name):
        return job_name in cls.get_jobs().keys()


class InheritableClassType(type):
    _holder = ModelsRegistryHolder

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if not new_cls.__name__ == "BaseCSVClass":
            job_name = new_cls.Meta.name
            if not job_name:
                raise Exception(f"{new_cls.Meta.name} is not configured properly")

            cls._holder.register(new_cls)
        return new_cls
