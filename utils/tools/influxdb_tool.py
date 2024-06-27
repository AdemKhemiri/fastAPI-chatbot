from influxdb_client import InfluxDBClient, Point
from langchain.tools import BaseTool
import os
from dotenv import load_dotenv

load_dotenv()

desc = (
    "Whenever the user asks about the energy consumption, abide to the following policy:"
    "1. You ALWAYS need to get the id returned from the 'Get Ids from MongoDB' tool"
    "2. Use the influxdb code snipped provided as a query to retrieve the data for the user "
    "3. MAKE SURE to update the 'id' and dates according to the prompt inputted."
    "4. To use the tool you MUST provide parameters ['influx_query']."
    "5. Execute the query you generated and get the necessary information."
    "6. Format the value (in kWh) nicely with commas for the user for ease of readability\n"

    "the bucket of influxdb is called 'energy-ds'"
    "format the date accordingly if necessary"
    "make SURE you use this code snipped as a query to get the energy consumption"
    '''
        import "timezone" option
        location = timezone.fixed(offset: 0h)
        from(bucket: "energy-ds")
        |> range(start: 2023-06-11T23:00:00.000Z, stop: 2023-06-12T23:00:00.000Z)
        |> filter(fn: (r) => r["_measurement"] == "<insert id from 'Get Ids from MongoDB' tool here>")
        |> filter(fn: (r) => r["_field"] == "Eit")
        |> sum()
        |> sort(columns: ["_time"], desc: false)
    '''
)


class GetInfluxData(BaseTool):
    name: str = "Get access to InfluxDB"
    description = desc

    token = os.environ.get("INFLUXDB_TOKEN")
    uri = "http://localhost:8086"
    bucket = "energy-ds"
    org: str = "Orbit"
    def _run(self, influx_query):

        # Initialize the client
        client = InfluxDBClient(url=self.uri, token=self.token, org=self.org)

        tables = client.query_api().query(query=influx_query, org=self.org)
        value = "0"
        # Process the results
        for table in tables:
            for record in table.records:
                # if value != "0": break
                value = record["_value"]
        return value

    def _arun(self, influx_query):
        token = os.environ.get("INFLUXDB_TOKEN")
        uri = "http://localhost:8086"
        bucket = "energy-ds"
        org = "Orbit"

        # Initialize the client
        client = InfluxDBClient(url=uri, token=token, org=org)
        tables = client.query_api().query(influx_query, org=org)
        value = "0"
        # Process the results
        for table in tables:
            for record in table.records:
                # if value != "0": break
                print(record["_value"])
                value = record["_value"]
                print(value)
        return value
