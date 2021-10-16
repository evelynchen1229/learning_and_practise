class Config:
    def __init__(self, env):
        # two environments - dev and qa
        # going to test dev environment and qa environment; doing this
        # any single change in the test can run just fine in both dev and qa
        # environment
        '''env: the envir I'm in '''
        SUPPORTED_ENVS = ['dev', 'qa']
        if env.lower() not in SUPPORTED_ENVS:
            raise Exception(f'''
                            '{env}' is not a supported environment.
                            Supported envs are '{SUPPORTED_ENVS}'
                            ''')

        self.base_url = {
            'dev' : 'https://mydev-env.com',
            'qa' : 'https://myqa-env.com'
        }[env]


        self.app_port = {
            'dev' : 8080,
            'qa' : 80

        }[env]

