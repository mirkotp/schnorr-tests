FROM mirkotp/charm-crypto:1.0
WORKDIR /app
COPY ./src/* ./

CMD for f in *.py; do echo -n -e "$f:   "; python "$f"; done
