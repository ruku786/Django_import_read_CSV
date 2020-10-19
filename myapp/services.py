from myapp.registry_class import InheritableClassType
from myapp.models import Person, Person_detail
import csv
import io
from myapp.exceptions import CSVException


class BaseCSVClass(metaclass=InheritableClassType):
    class Meta:
        name = None
        description = None
        columns = None

    @classmethod
    def info(cls):
        return {"job_name": cls.Meta.name}

    @classmethod
    def validate_headers(cls, headers):
        columns = cls.Meta.columns
        columns_str = ", ".join(columns)
        if set(columns) != set(headers):
            raise CSVException(f"Invalid Headers in CSV, Allowed headers are {columns_str}")

    @classmethod
    def read_csv(cls, csv_file):
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        data_list = [{k: v for k, v in x.items()}
                     for x in
                     csv.DictReader(io_string, skipinitialspace=True)]
        return data_list

    @classmethod
    def execute(cls, csv_file):
        data_set = cls.read_csv(csv_file)
        if data_set:
            cls.validate_headers(data_set[0].keys())
            upload = cls.upload_csv(data_set)
            return upload
        return None

    @classmethod
    def upload_csv(cls, rows):
        raise NotImplementedError("Upload CSV method not implemented")


class PersonService(BaseCSVClass):
    class Meta:
        name = "Person"
        columns = (
            'name',
            'email',
            'location'
        )

    @classmethod
    def upload_csv(cls, rows):
        for row in rows:
            _, created = Person.objects.update_or_create(
                name=row.get("name"),
                email=row.get("email"),
                location=row.get("location")
            )


class PersonDetailsService(BaseCSVClass):
    class Meta:
        name = "Person_detail"
        columns = (
            'email',
            'Address',
            'Date of Birth',
            'Phone no.'
        )

    @classmethod
    def upload_csv(cls, rows):
        person_emails = [x.get("email") for x in rows]
        person_objs = Person.objects.filter(email__in=person_emails)
        for row in rows:
            person = person_objs.get(email=row.get('email'))
            _, created = Person_detail.objects.update_or_create(
                address=row.get("Address"),
                person_id=person,
                birth_date=row.get("Date of Birth"),
                phone=row.get("Phone no.")
            )
            print(_)


def add_classes_to_server():
    PersonDetailsService()
    PersonService()
