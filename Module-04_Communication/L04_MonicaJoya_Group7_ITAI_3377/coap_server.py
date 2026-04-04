import asyncio
import aiocoap
import aiocoap.resource as resource

class SensorDataResource(resource.Resource):
    """CoAP resource that receives sensor data via POST requests."""

    async def render_post(self, request):
        payload = request.payload.decode('utf-8')
        print(f"Received sensor data: {payload}")
        return aiocoap.Message(code=aiocoap.CHANGED, payload=b"Data received")

async def main():
    root = resource.Site()
    root.add_resource(['sensor', 'data'], SensorDataResource())

    await aiocoap.Context.create_server_context(root, bind=('localhost', 5683))
    print("CoAP Server running on coap://localhost:5683/sensor/data")
    await asyncio.get_event_loop().create_future()  # Run forever

asyncio.run(main())
