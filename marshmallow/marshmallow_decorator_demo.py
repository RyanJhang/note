from marshmallow import (Schema, ValidationError, fields, post_dump, post_load,
                         pre_dump, pre_load, validates, validates_schema)


class UserSchema(Schema):

    email = fields.Str(required=True)
    age = fields.Integer(required=True)

    @post_load
    def lowerstrip_email(self, item, **kwargs):
        item['email'] = item['email'].lower().strip()
        return item

    # @pre_load(pass_many=True)
    # def remove_envelope(self, data, many, **kwargs):
    #     namespace = 'results' if many else 'result'
    #     return data[namespace]

    # @post_dump(pass_many=True)
    # def add_envelope(self, data, many, **kwargs):
    #     namespace = 'results' if many else 'result'
    #     return {namespace: data}

    @validates_schema
    def validate_email(self, data, **kwargs):
        if len(data['email']) < 3:
            raise ValidationError('Email must be more than 3 characters', 'email')

    @validates('age')
    def validate_age(self, data, **kwargs):
        if data < 14:
            raise ValidationError('Too young!')


u = UserSchema().load([dict(email="a@b", age=15), dict(email="a@b", age=12)], many=True)
print(u)
