from influxdb_client import InfluxDBClient, Point
from langchain.tools import BaseTool
import os
from dotenv import load_dotenv
load_dotenv()


desc = (
    "Use this tool to access InfluxDB and get the relevent data"
    "You are an EXPERT in writing queries with InfluxQL for influxdb (InfluxQL)"
    "To be able to access this tool you need to get the id from the provided name"
    "To use the tool you MUST provide parameters*"
    "['influx_query']."
    # "id: you get it from 'Get Id from DB' action/tool"
    "You have to generate a snippet code of query according to the user input to get 'influx_query'"
    "Execute the query you generated and get the necessary information"
    "the bucket of influxdb is called 'energy-ds'"
    "format the date accordingly if necessary"
    "use this example to get the energy"
    """
    import "timezone" option
    location = timezone.fixed(offset: 0h)
    from(bucket: "energy-ds")
    |> range(start: 2023-06-11T23:00:00.000Z, stop: 2023-06-12T23:00:00.000Z)
    |> filter(fn: (r) => r["_measurement"] == "id")
    |> filter(fn: (r) => r["_field"] == "Eit")
    |> sum()
    |> sort(columns: ["_time"], desc: false)
    """
    "use this snippet query example to get the neccessary informations"
    "but you subtitute 'id' with the id of the device"
    "format a nicely put sentence using the data recieved"
)

class GetInfluxData(BaseTool):
    
    name: str = "Get access to InfluxDB"
    description = desc
    
    def _run(self, influx_query):
        
        token=os.environ.get("INFLUXDB_TOKEN"), 
        uri="https://next-molly-formerly.ngrok-free.app", 
        bucket="energy-ds",
        org="Orbit",
        
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


    def _arun(self):
        raise NotImplementedError("This tool does not support async")