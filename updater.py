import dns.resolver
import dockercloud
import os
import requests
import sys
import time

if not os.environ.get("DOCKERCLOUD_SUBDOMAINS_DOMAIN"):
    print 'Please set the DOCKERCLOUD_SUBDOMAINS_DOMAIN environment variable to specify the domain that subdomains are on.'
    sys.exit(1)

DOMAIN = os.environ['DOCKERCLOUD_SUBDOMAINS_DOMAIN']

SUBDOMAIN_LABEL = os.environ['DOCKERCLOUD_SUBDOMAINS_SUBDOMAIN_LABEL']
PORT_LABEL = os.environ['DOCKERCLOUD_SUBDOMAINS_PORT_LABEL']

def generate_provider(containers):
    provider = {
        "frontends": {},
        "backends": {},
    }
    for container in containers:
        container.refresh()
        if not hasattr(container, "labels"):
            continue
        if not container.state == "Running":
            continue
        subdomain = container.labels.get(SUBDOMAIN_LABEL)
        if not subdomain:
            continue

        domain = '.'.join([subdomain, DOMAIN])

        if domain not in provider["frontends"]:
            provider["frontends"][domain] = {
                "backend": domain,
                "routes": {
                    "default": {
                        "rule": "Host: %s" % domain,
                    }
                },
                "passHostHeader": True,
            }
        if domain not in provider["backends"]:
            provider["backends"][domain] = {
                "servers": {},
            }
        port = container.labels.get(PORT_LABEL, '80')
        provider["backends"][domain]["servers"][container.uuid] = {
            "url": "http://{}:{}".format(container.private_ip, port),
        }

    return provider


def get_traefik_ip_addresses():
    return [unicode(r) for r in dns.resolver.query('traefik', 'A')]


def main():
    if not os.environ.get("DOCKERCLOUD_USER") or not os.environ.get("DOCKERCLOUD_APIKEY"):
        print "Please set DOCKERCLOUD_USER and DOCKERCLOUD_APIKEY environment variables."
        return 1


    previous_provider = None
    while True:
        containers = dockercloud.Container.list()
        provider = generate_provider(containers)
        addresses = get_traefik_ip_addresses()
        print "Updating {} to {}".format(addresses, provider)
        for address in addresses:
            resp = requests.put(
                "http://{}:8080/api/providers/web".format(address),
                json=provider
            )
            resp.raise_for_status()

        time.sleep(int(os.environ.get("UPDATE_INTERVAL", 30)))

    return 0

if __name__ == "__main__":
    sys.exit(main())
