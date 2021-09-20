FROM nginx
COPY nginx.conf.template /etc/nginx/nginx.conf.template
CMD /bin/bash -c "envsubst '\$API_URL \$API_HOST \$PORT \$PROTOCOL' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"