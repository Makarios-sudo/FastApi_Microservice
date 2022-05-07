from redis_om import get_redis_connection


redis = get_redis_connection(
    host="redis-19958.c8.us-east-1-4.ec2.cloud.redislabs.com",
    port = 19958,
    password = "DFd94jr23DBXJk8R5ygP8GssBdz3e2xv",
    decode_responses=True
)