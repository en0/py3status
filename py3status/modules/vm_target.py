# -*- coding: utf-8 -*-
"""
Control VM Targets for XForwarding

@author ilaird
"""

from time import time
import xmlrpclib


def safe_parse(v, t, d):
    _ret = d
    try:
        _ret = t(v)
    except ValueError:
        _ret = d
    return _ret


class Py3status:
    """
    """

    format = '{output}'
    cache_latency = 1
    rpc_host = '127.0.0.1'
    rpc_port = 8189

    def __init__(self):
        self._has_proxy = False
        self._proxy = None
        self._target = None

    @property
    def proxy(self):
        if not self._has_proxy:
            self._proxy = xmlrpclib.ServerProxy("http://{}:{}/".format(
                self.rpc_host,
                int(self.rpc_port)
            ), allow_none=True)
            self._has_proxy = True
        return self._proxy

    def vm_target(self, i3s_output_list, i3s_config):
        _target = self.proxy.get_name()

        if _target == "LOCAL":
            _color = i3s_config.get('color_good', None)
        else:
            _color = i3s_config.get('color_bad', None)

        response = {
            'cached_until': time() + self.cache_latency,
            'color': _color,
            'transformed': self._target != _target
        }

        self._target = _target
        response['full_text'] = self.format.format(output=_target)
        return response

    def on_click(self, i3s_output_list, i3s_config, event):
        """
        Enable/Disable DPMS on left click.
        """
        if event['button'] == 1:
            self.proxy.move(1)

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00ff00',
        'color_bad': '#ff0000',
    }
    while True:
        print(x.vm_target([], config))
        sleep(1)
