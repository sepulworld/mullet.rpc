# mulletrpc

An oauth protected interface to request grpcurls against registered endpoints and protos

### Local Development

1. clone project
2. `poetry install`
3. `poetry shell`
4. export required OAuth client secrets in your shell, see Tiltfile for ones needed.
5. Start your local Docker/K8s cluster
6. `tilt up`
