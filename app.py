import redis
import time
import random
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.resources import Resource

logging.basicConfig(level=logging.DEBUG)

# Initialize tracing
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "pizza-order-service"}))
)
tracer = trace.get_tracer_provider().get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(otlp_exporter))

# Initialize Redis client
try:
    redis_client = redis.Redis(host="redis", port=6379)
    redis_client.ping()  # Test the connection
    print("Connected to Redis successfully!")
except Exception as e:
    print(f"Failed to connect to Redis: {e}")
    raise

def place_pizza_order():
    pizzas = ["Margherita", "Pepperoni", "Hawaiian", "Veggie", "BBQ Chicken"]
    order_id = f"order:{random.randint(1000, 9999)}"
    pizza_type = random.choice(pizzas)

    with tracer.start_as_current_span("place_pizza_order") as span:
        span.set_attribute("order_id", order_id)
        span.set_attribute("pizza_type", pizza_type)

        redis_client.set(order_id, pizza_type, ex=10)  # Expiry in 10 seconds
        print(f"Placed order {order_id} for {pizza_type}")

if __name__ == "__main__":
    while True:
        place_pizza_order()
        time.sleep(10)
