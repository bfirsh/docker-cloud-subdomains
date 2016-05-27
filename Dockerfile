FROM python:2.7-onbuild
ENV PYTHONUNBUFFERED=1
CMD ["python", "updater.py"]
