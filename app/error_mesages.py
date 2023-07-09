NOT_FOUND = '{instance} with id = ({id}) not found'

FORBIDDEN = 'user with id = ({user_id}) could not {action} {instance} ' \
            'with id = ({instance_id}). '

NOT_OWNER = FORBIDDEN + 'User is not owner.'

IS_OWNER = FORBIDDEN + 'User is owner'

INCORRECT_EMAIL = "Incorrect email"

INCORRECT_PASSWORD = 'Incorrect password'

