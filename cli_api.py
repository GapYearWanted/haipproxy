# coding:utf8

import falcon
from haipproxy.client.py_cli import ProxyFetcher
from haipproxy.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
from collections import defaultdict

DEFAULT_STRATEGY = "robin"

redis_args = {
    'host': REDIS_HOST,
    'port': REDIS_PORT,
    'password': REDIS_PASSWORD,
    'db': REDIS_DB,
}

fetchers = {}

def generate_fetchers(tmpl):
    return {"greedy": ProxyFetcher(tmpl, "greedy", redis_args=redis_args) ,
            "robin": ProxyFetcher(tmpl, "robin", redis_args=redis_args) ,}

def fetch_proxy(tmpl, strategy):
    if tmpl not in fetchers:
        fetchers[tmpl] = generate_fetchers(tmpl)
    return fetchers[tmpl][strategy].get_proxy()

def fetch_proxies(tmpl, strategy):
    if tmpl not in fetchers:
        fetchers[tmpl] = generate_fetchers(tmpl)
    return fetchers[tmpl][strategy].get_proxies()


class GetProxy(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        tmpl = req.get_param("tmpl", required=True)
        strategy = req.get_param("strategy", default=DEFAULT_STRATEGY)
        strategy = strategy if strategy in ("robin", "greedy") else DEFAULT_STRATEGY
        resp.body = fetch_proxy(tmpl, strategy)


class GetProxies(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        tmpl = req.get_param("tmpl", required=True)
        strategy = req.get_param("strategy", default=DEFAULT_STRATEGY)
        strategy = strategy if strategy in ("robin", "greedy") else DEFAULT_STRATEGY
        resp.body = fetch_proxies(tmpl, strategy)

app = falcon.API()
proxy = GetProxy()
app.add_route("/get_proxy", proxy)
app.add_route("/get_proxies", proxy)
