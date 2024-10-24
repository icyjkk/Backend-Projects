from marshmallow import Schema, fields,validate

# Esquema para la paginación
class PaginationSchema(Schema):
    page = fields.Int(required=False, missing=1, validate=lambda x: x > 0,
        error_messages={
            "invalid": "Page must be a valid integer.",
            "validator_failed": "Page must be a positive integer."
        })
    limit = fields.Int(required=False, missing=10, validate=lambda x: x > 0, 
        error_messages={
            "invalid": "Limit must be a valid integer.",
            "validator_failed": "Limit must be a positive integer."
        })

class TaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Title cannot be empty"),
        error_messages={"required": "Title is required"}
    )
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Description cannot be empty"),
        error_messages={"required": "Description is required"}
    )
