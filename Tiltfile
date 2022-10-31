print("mulletrpc!")
load('ext://secret', 'secret_from_dict')
#local_resource("lint", ["poetry", "run", "flake8", "app", "mulletrpc.py"])
#local_resource("black", ["poetry", "run", "black", "--check", "app", "mulletrpc.py"])
#local_resource("isort", ["poetry", "run", "isort", "--check-only", "app", "mulletrpc.py"])
docker_build('mulletrpc', '.')
k8s_yaml(secret_from_dict("secrets", inputs = {
    'CLIENT_ID' : os.getenv('CLIENT_ID'),
    'CLIENT_SECRET' : os.getenv('CLIENT_SECRET'),
    'REDIRECT_URI' : os.getenv('REDIRECT_URI'),
    'AUTH_URI' : os.getenv('AUTH_URI'),
    'TOKEN_URI' : os.getenv('TOKEN_URI'),
    'ISSUER' : os.getenv('ISSUER'),
    'USERINFO_URI' : os.getenv('USERINFO_URI'),
    'TOKEN_INTROSPECTION_URI' : os.getenv('TOKEN_INTROSPECTION_URI'),
    'GIT_USER' : os.getenv('GIT_USER'),
    'GIT_TOKEN' : os.getenv('GIT_TOKEN'),
}))
k8s_yaml('local_dev/local.yaml')
k8s_resource('mulletrpc', port_forwards=8080)
