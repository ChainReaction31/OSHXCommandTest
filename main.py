from consys4py.datamodels.api_utils import URI, UCUMCode
from consys4py.datamodels.control_streams import ControlStreamJSONSchema
from consys4py.datamodels.swe_components import DataRecordSchema, TimeSchema, QuantitySchema, VectorSchema
from oshconnect.oshconnectapi import OSHConnect
from oshconnect.osh_connect_datamodels import System, Node, Datastream
from oshconnect.timemanagement import TemporalModes, TimeInstant


def setup_with_control():
    oshconnect = OSHConnect(name="OSHConnect", playback_mode=TemporalModes.REAL_TIME)

    node = Node(protocol="http", address="localhost", port=8181, username="admin", password="admin")
    oshconnect.add_node(node)

    controllable_system = oshconnect.insert_system(
        System(name="Controllable System", description="Controllable System for testing", label="Controllable System",
               urn="urn:system:test:controllable:1"))

    datarecord_schema = DataRecordSchema(label='Example Data Record', description='Example Data Record Description',
                                         definition='www.test.org/records/example-datarecord', fields=[])
    time_schema = TimeSchema(label="Timestamp", definition="http://test.com/Time", name="timestamp",
                             uom=URI(href="http://test.com/TimeUOM"))
    continuous_value_field = QuantitySchema(name='continuous-value-distance', label='Continuous Value Distance',
                                            description='Continuous Value Description',
                                            definition='www.test.org/fields/continuous-value',
                                            uom=UCUMCode(code='m', label='meters'))

    datarecord_schema.fields.append(time_schema)
    datarecord_schema.fields.append(continuous_value_field)

    datastream = controllable_system.add_datastream(datarecord_schema=datarecord_schema)

    command_schema = ControlStreamJSONSchema()

def setup_with_location():
    oshconnect = OSHConnect(name="OSHConnect", playback_mode=TemporalModes.REAL_TIME)

    node = Node(protocol="http", address="localhost", port=8282, username="admin", password="admin")
    oshconnect.add_node(node)

    the_system = oshconnect.insert_system(
        System(name="Controllable System", description="Controllable System for testing", label="Controllable System",
               urn="urn:system:test:controllable:1"), target_node=node)

    datarecord_schema = DataRecordSchema(label='Example Data Record', description='Example Data Record Description',
                                         definition='www.test.org/records/example-datarecord', fields=[])
    time_schema = TimeSchema(label="Timestamp", definition="http://test.com/Time", name="timestamp",
                             uom=URI(href="http://test.com/TimeUOM"))
    loc_schema = create_loc_schema()

    datarecord_schema.fields.append(time_schema)
    datarecord_schema.fields.append(loc_schema)

    datastream = the_system.add_insert_datastream(datarecord_schema)

    return oshconnect, the_system, datastream



def create_loc_schema():
    loc_schema = VectorSchema(label="Sensor Location", name="sensorLocation", description="Sensor Location as reported by the device",
                              reference_frame="http://www.opengis.net/def/crs/EPSG/0/4979", local_frame="#REF_FRAME_LOCAL_SIM_DEVICE_001", definition="http://www.opengis.net/def/property/OGC/0/SensorLocation", coordinates=[
            QuantitySchema(label="Geodetic Latitude", name="lat", axis_id="Lat", definition="http://sensorml.com/ont/swe/property/GeodeticLatitude", uom=UCUMCode(code="deg", label="degrees")),
            QuantitySchema(label="Longitude", name="lon", axis_id="Lon", definition="http://sensorml.com/ont/swe/property/Longitude", uom=UCUMCode(code="deg", label="degrees")),
            QuantitySchema(label="Altitude", name="alt", axis_id="h", definition="http://sensorml.com/ont/swe/property/HeightAboveEllipsoid", uom=UCUMCode(code='m', label='meters'))
        ], type="Vector")

    return loc_schema

def generate_location_result():
    result = {
        "resultTime": TimeInstant.now_as_time_instant().get_iso_time(),
        "phenomenonTime": TimeInstant.now_as_time_instant().get_iso_time(),
        "result": {
            "timestamp": TimeInstant.now_as_time_instant().epoch_time,
            "sensorLocation": {
                "lat": 0.0,
                "lon": 90.0,
                "alt": 100.0,
            }
        }
    }

    return result

def main():
    oshconnect, the_system, datastream = setup_with_location()
    datastream.insert_observation_dict(generate_location_result())


if __name__ == '__main__':
    main()
