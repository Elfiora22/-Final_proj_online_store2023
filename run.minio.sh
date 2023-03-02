docker run \
  -p 9000:9000 \
  -p 9090:9090 \
  --name minio \
  -v /Users/elenafostachuk/project2023/django/minio/data:/data \
  -e "MINIO_ROOT_USER=ROOTNAME" \
  -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
  quay.io/minio/minio server /data --console-address ":9090"