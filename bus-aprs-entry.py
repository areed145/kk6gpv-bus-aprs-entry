import aprslib
from datetime import datetime
import paho.mqtt.client as mqtt
import json


def unpack_dict(d):
    try:
        message = {}
        message["timestamp"] = datetime.utcnow().isoformat()
        message["script"] = "entry"
        for k, v in d.items():
            try:
                for k1, v1 in v.items():
                    message[k + "_" + k1] = v1
            except Exception:
                try:
                    message[k] = v
                except Exception:
                    message[k] = str(v)
        client.publish(
            "kk6gpv_bus/aprs/" + str(message["script"]),
            json.dumps(message),
            retain=True,
        )
        print(message)
    except Exception:
        print("unpack failed")


if __name__ == "__main__":
    while True:
        try:
            client = mqtt.Client(
                client_id="kk6gpv-bus-aprs-entry", clean_session=False
            )
            client.connect("broker.mqttdashboard.com", 1883)

            ais = aprslib.IS("N0CALL", "13023", port=14580)
            ais.set_filter("e/KK6GPV*")
            ais.connect()
            ais.consumer(unpack_dict, raw=False)
        except Exception:
            pass