import json
import os
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor

from tornado.options import define, options
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web

thread_pool = ThreadPoolExecutor()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user_name")

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'text/json')
        self.finish(json.dumps({
            'error': {
                'code': status_code,
                'message': self._reason,
            }
        }))


class NotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'text/json')
        self.finish(json.dumps({
            'error': {
                'code': 404,
                'message': "Not found",
            }
        }))


class PrimesHandler(BaseHandler):
    @gen.coroutine
    def get(self, index):
        username = self.get_argument("username")
        if not self.current_user:
            self.set_secure_cookie("user_name", username)
        prime = yield thread_pool.submit(self.calculate_prime, int(index))
        self.write({"result": prime})

    def calculate_prime(self, index):
        """
        Calculate prime of given index number.

        :param index: index number of prime.
        :return: generated prime
        """
        for i, prime in enumerate(self._prime_gen()):
            if i == index - 1:
                return prime

    def _prime_gen(self):
        """
        Helper function which yields prime numbers starting from 2.
        """
        # Maps composites to primes witnessing their compositeness.
        # This is memory efficient, as the sieve is not "run forward"
        # indefinitely, but only as long as required by the current
        # number being tested.
        comp_to_primes = {}

        # The running integer that's checked for primeness
        q = 2
        while True:
            if q not in comp_to_primes:
                # q is a new prime.
                # Yield it and mark its first multiple that isn't
                # already marked in previous iterations
                #
                yield q
                comp_to_primes[q * q] = [q]
            else:
                # q is composite. comp_to_primes[q] is the list of primes that
                # divide it. Since we've reached q, we no longer
                # need it in the map, but we'll mark the next
                # multiples of its witnesses to prepare for larger
                # numbers
                #
                for p in comp_to_primes[q]:
                    comp_to_primes.setdefault(p + q, []).append(p)
                del comp_to_primes[q]
            q += 1


class FactorizeHandler(BaseHandler):
    @gen.coroutine
    def get(self, n):
        username = self.get_argument("username")
        if not self.current_user:
            self.set_secure_cookie("user_name", username)
        factorized = yield thread_pool.submit(self._calculate_factors, int(n))
        self.write({"result": factorized})

    def _calculate_factors(self, n):
        """
        Calculate prime factors of given natural number.

        :param n: Number to factorize
        :return: List of numbers which give original number when multiplied
        """
        def factors(n):
            while n > 1:
                for i in range(2, n + 1):
                    if n % i == 0:
                        n = int(n / i)
                        yield i
                        break
        return list(number for number in factors(n))


class PingHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        username = self.get_argument("username")
        if not self.current_user:
            self.set_secure_cookie("user_name", username)
        server_name = self.get_argument("server")
        ping_count = int(self.get_argument("ping_count"))
        result = yield thread_pool.submit(self._ping_servers, ping_count, server_name)
        self.write({"result": result})

    def _ping_servers(self, ping_count, server_name):
            return list({"try": c+1, "ret_code": self._ping_return_code(server_name)} for c in range(ping_count))

    def _ping_return_code(self, hostname):
        """
        Use the ping utility to attempt to reach the host. We send 5 packets
        ('-c 5')The function
        returns the return code from the ping utility.

        :param hostname: Hostname to ping
        :return: return code of 'ping' command.
        """
        ret_code = subprocess.call(['ping', '-c', '5', hostname],
                                   stdout=open(os.devnull, 'w'),
                                   stderr=open(os.devnull, 'w'))
        return ret_code


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/primes/([0-9]+)", PrimesHandler),
            (r"/api/factorize/([0-9]+)", FactorizeHandler),
            (r"/api/ping/?", PingHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def make_app():
    handlers = [
        (r"/api/primes/([0-9]+)", PrimesHandler),
        (r"/api/factorize/([0-9]+)", FactorizeHandler),
        (r"/api/ping/?", PingHandler),
        (r"/.*", NotFoundHandler),
    ]
    cookie_secret = "secret"
    return tornado.web.Application(handlers, cookie_secret=cookie_secret)


def main():
    define("port", default="8080", help="Web server port")
    options.parse_command_line()
    app = make_app()
    print("Starting web server at :%s" % options.port)
    app.listen(options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
