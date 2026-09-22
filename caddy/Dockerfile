# Immagine ufficiale pinnata per digest (index multi-arch), come backend e
# frontend. Ci si costruisce sopra per due motivi:
#   1. apk upgrade: il layer alpine dell'upstream può portare pacchetti con
#      CVE già fixate nei repo (curl, c-ares, libcurl) ma non ancora rilanciate
#      in immagine — qui si chiude subito;
#   2. la config entra nell'immagine invece che via volume: quello che gira è
#      quello committato, rebuildato e scansionabile.
FROM caddy:2-alpine@sha256:de23def33b17fb5d1290b0f6c2add1d70780e52341896c00a4c8a2a2fe9d355e

RUN apk upgrade --no-cache

COPY Caddyfile /etc/caddy/Caddyfile
