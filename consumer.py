import time

from main import redis, Order

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key, group, id='0', mkstream=True)
except:
    print("group already exists")

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                if 'pk' in obj:
                    print(f"Processing order {obj['pk']}")

                    # Fetch the order and cancel it
                    try:
                        order = Order.get(obj['pk'])  # Assuming 'pk' is the primary key
                        order.status = 'cancelled'
                        order.save()
                        print(f"Order {obj['pk']} has been cancelled.")
                    except Exception as e:
                        print(f"Error updating order {obj['pk']}: {str(e)}")
                else:
                    print(f"Invalid order data: {obj}")

    except Exception as e:
        print(str(e))

    time.sleep(1)