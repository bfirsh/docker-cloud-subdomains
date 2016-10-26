FROM python:2.7-onbuild
ENV PYTHONUNBUFFERED=1
ENV DOCKERCLOUD_SUBDOMAINS_LABEL=sh.fir.docker-cloud-subdomain
CMD ["python", "updater.py"]
