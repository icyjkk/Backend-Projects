from marshmallow import Schema, fields, validate

# List of valid language codes
valid_languages = [
    "de", "de-DE", "de-AT", "de-CH", "en", "en-US", "en-AU", "en-GB", "en-CA", "en-NZ",
    "en-ZA", "es", "es-AR", "fr", "fr-CA", "fr-CH", "fr-BE", "nl", "nl-BE", "pt-AO",
    "pt-BR", "pt-MZ", "pt-PT", "ar", "ast-ES", "be-BY", "br-FR", "ca-ES", "ca-ES-valencia",
    "ca-ES-balear", "da-DK", "de-DE-x-simple-language", "el-GR", "eo", "fa", "ga-IE", 
    "gl-ES", "it", "ja-JP", "km-KH", "pl-PL", "ro-RO", "ru-RU", "sk-SK", "sl-SI", "sv",
    "ta-IN", "tl-PH", "uk-UA", "zh-CN", "crh-UA", "nb", "no", "nl-NL", "de-LU", "fr-FR",
    "sv-SE", "it-IT", "fa-IR", "es-ES"
]

class NoteSchema(Schema):
    # Field for the note content
    note = fields.Str(
        required=True,
        validate=[
            # Ensure the note is not empty
            validate.Length(min=1, error="Note cannot be empty"),
            # Ensure the note contains at least one non-whitespace character
            validate.Regexp(r'.*\S.*', error="Note cannot contain only spaces")
        ],
        error_messages={"required": "Name is required"}
    )
    
    # Field for the language, must be one of the valid language codes
    language = fields.Str(
        required=True,
        validate=validate.OneOf(
            valid_languages,
            error="Invalid language. Please choose a valid language code."
        ),
        error_messages={"required": "Language is required"}
    )
