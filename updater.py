import dockercloud
import os
import requests
import sys
import time

LABEL = os.environ['DOCKERCLOUD_SUBDOMAINS_LABEL']

def generate_provider(containers):
    provider = {
        "frontends": {},
        "backends": {},
    }
    for container in containers:
        container.refresh()
        if not hasattr(container, "labels"):
            continue
        subdomain = container.labels.get(LABEL)
        if not subdomain:
            continue

        if subdomain not in provider["frontends"]:
            provider["frontends"][subdomain] = {
                "backend": subdomain,
                "routes": {
                    "default": {
                        "rule": "Host: %s" % subdomain,
                    }
                }
            }
        if subdomain not in provider["backends"]:
            provider["backends"][subdomain] = {
                "servers": {},
            }
        provider["backends"][subdomain]["servers"][container.uuid] = {
            "url": "http://%s" % container.private_ip,
        }

    return provider

def main():
    if not os.environ.get("DOCKERCLOUD_USER") or not os.environ.get("DOCKERCLOUD_APIKEY"):
        print "Please set DOCKERCLOUD_USER and DOCKERCLOUD_APIKEY environment variables."
        return 1


    previous_provider = None
    while True:
        containers = dockercloud.Container.list()
        provider = generate_provider(containers)
        if provider != previous_provider:
            print "Updating provider: %s" % provider
            resp = requests.put("http://traefik:8080/api/providers/web", json=provider)
            resp.raise_for_status()
            previous_provider = provider

        time.sleep(int(os.environ.get("UPDATE_INTERVAL", 30)))

    return 0

if __name__ == "__main__":
    sys.exit(main())
