from database import redis
from model import Order
import time

key = "refund_order"
group = "payment-group"

try:
    redis.xgroup_create(key, group)
except:
    print("group already exist")

while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)
        if results !=[]:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj["pk"])
                order.status = "refunded"
                print(" order was refunded")
                order.save()
    except Exception as e:
        print(str(e))
    time.sleep(1)