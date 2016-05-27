# docker-cloud-subdomains

A Docker Cloud app which automatically makes other apps in your Docker Cloud account accessible as Heroku-style subdomains (e.g. myapp.example.com).

## Getting started

1. Create a stack on Docker Cloud using this stack file, filling in your Docker Cloud details:

        traefik:
          image: traefik
          command: --web
          ports:
            - "80:80"
        updater:
          image: bfirsh/docker-cloud-subdomains
          environment:
            - "DOCKERCLOUD_USER"
            - "DOCKERCLOUD_APIKEY"
          links:
            - traefik

2. Get the address of the traefik service that you have just created in Docker Cloud (something ending with `.svc.dockerapp.io`). Set up a wildcard CNAME on the domain you want to use and point it at the service address.

3. You can now set the label `sh.fir.docker-cloud-subdomain` on containers in your Docker Cloud apps to making them automatically appear at that domain. For example, you might put something like this in your stack file to make it available at `myapp.example.com`:

        web:
           image: oscorp/myapp
           labels:
             - "sh.fir.docker-cloud-subdomain=myapp.example.com"
