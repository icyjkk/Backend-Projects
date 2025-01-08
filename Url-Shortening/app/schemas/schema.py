from marshmallow import Schema, fields, validate

class UrlSchema(Schema):
    # Campo para la URL original (obligatorio, formato válido)
    url = fields.Str(
        required=False,
        validate=[
            validate.Length(min=5, error="URL cannot be empty or too short"),
            validate.URL(error="Invalid URL format")  # Verifica si es una URL válida
        ],
        error_messages={"required": "URL is required"}
    )

    # Campo para el short_code (Generado con uuid)
    short_code = fields.Str(
        required=False,  # No obligatorio en la solicitud, se genera en backend
        validate=[
            validate.Length(equal=6, error="Short code must be exactly 6 characters"),
            validate.Regexp(r'^[a-zA-Z0-9]+$', error="Short code must contain only letters and numbers")
        ]
    )
