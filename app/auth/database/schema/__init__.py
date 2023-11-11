from auth.database.schema import schemaUser, shemaPassword, schemaContact, schemaToken


SCHEMA_TYPE_SELECT = schemaUser.User | shemaPassword.Password | schemaContact.Contact | schemaContact.Adress \
                    | schemaContact.Phone | schemaToken.Token 

SCHEMA_TYPE_CREATE = schemaUser.UserCreate | shemaPassword.PasswordCreate | schemaContact.ContactCreate | schemaContact.AdressCreate \
                    | schemaContact.PhoneCreate | schemaToken.TokenCreate

SCHEMA_TYPE_PATCH = schemaUser.UserPatch | shemaPassword.PasswordPatch | schemaContact.ContactPatch | schemaContact.AdressPatch \
                    | schemaContact.PhonePatch | schemaToken.TokenPatch