from tortoise.contrib.fastapi import HTTPNotFoundError


def template_for_404():
    return dict(responses={404: {"model": HTTPNotFoundError}})
