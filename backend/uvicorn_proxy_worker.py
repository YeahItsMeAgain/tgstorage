from uvicorn.workers import UvicornWorker

class UvicornProxyWorker(UvicornWorker):
    CONFIG_KWARGS = {**UvicornWorker.CONFIG_KWARGS, 'proxy_headers': True}
