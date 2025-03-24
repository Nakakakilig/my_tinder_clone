random_username=$(date +%s)

user_id=$(
  curl -X 'POST' \
  'http://0.0.0.0:8000/api/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "'$(date +%s)'"
}'| jq -r '.id'
)


profile_id=$(
  curl -X 'POST' \
  'http://0.0.0.0:8000/api/profiles/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d $'{
  "user_id": '"$user_id"',
  "first_name": "string",
  "last_name": "string",
  "gender": "male",
  "age": 0,
  "geo_latitude": 0,
  "geo_longitude": 0
}'| jq -r '.id'
)

curl -X 'POST' \
  'http://0.0.0.0:8000/api/preferences/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "profile_id": '"$profile_id"',
  "gender": "male",
  "age": 0,
  "radius": 0
}'
