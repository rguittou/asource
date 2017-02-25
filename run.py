#!/usr/bin/env python2

from flask import Flask, render_template, request, jsonify
import tfo
from tfo.Runner import Runner
from tfo.Options import Options


try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

app = Flask(__name__)

def v2_playbook_on_stats(stats):
    hosts = sorted(stats.processed.keys())
    for h in hosts:
        t = stats.summarize(h)
        msg = "PLAY RECAP [%s] : %s %s %s %s %s" % (
                h,
                "ok: %s" % (t['ok']),
                "changed: %s" % (t['changed']),
                "unreachable: %s" % (t['unreachable']),
                "skipped: %s" % (t['skipped']),
                "failed: %s" % (t['failures']),
            )

    return  msg

@app.route('/run')
def run():
   runner = tfo.Runner(
        playbook='command.yaml',
        hosts='hosts',
        display=display,
        options={
          #'tags':'debug',
        },
    )

   stats=runner.run()
   msg=v2_playbook_on_stats(stats)
   
   return jsonify({'tasks': msg})

def main():

#    stats = runner.run()
   
    # Maybe do something with stats here? If you want!
    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    main()
