import glob
import jsonschema
import os
import json


def load_json(fn):
    with open(fn, "r") as ff:
        return json.load(ff)


person_schema = load_json("./json_schemas/person/person.json")
car_schema = load_json("./json_schemas/car/car.json")
common_schema = load_json("./json_schemas/common.json")
schema_store = {
    person_schema["$id"]: person_schema,
    car_schema["$id"]: car_schema,
    common_schema["$id"]: common_schema,
}
person_validator = jsonschema.Draft7Validator(
    schema=person_schema,
    resolver=jsonschema.RefResolver.from_schema(person_schema, store=schema_store),
)

if __name__ == "__main__":
    person_validator.validate({"id": "id-person-1", "age": 20, "cars": []})
    person_validator.validate(
        {
            "id": "id-person-1",
            "age": 30,
            "cars": [
                {"id": "id-car-1", "vin": "vin-1"},
                {"id": "id-car-2", "vin": "vin-2"},
            ],
        }
    )
    print(
        [
            str(e)
            for e in person_validator.iter_errors({"id": "bad-person-id-1", "cars": []})
        ]
    )
    print(
        [
            str(e)
            for e in person_validator.iter_errors(
                {
                    "id": "id-person-1",
                    "age": 30,
                    "cars": [
                        {"id": "bad-id", "vin": "vin-1"},
                        {"id": "id-car-2", "vin": "vin-2"},
                    ],
                }
            )
        ]
    )
