FROM python:2.7-onbuild
ENV PYTHONUNBUFFERED=1
ENV DOCKERCLOUD_SUBDOMAINS_SUBDOMAIN_LABEL=sh.fir.subdomains.subdomain
ENV DOCKERCLOUD_SUBDOMAINS_PORT_LABEL=sh.fir.subdomains.port
CMD ["python", "updater.py"]
