import logging
from pathlib import Path
import sys
from connie.syn.parse import Parse
from connie.run.runner import Run


def main():
    logging.basicConfig()
    argv = sys.argv
    search_paths = []
    if len(argv) == 1:
        source_name = 'stdin'
        source = sys.stdin.read()
    else:
        source_name = argv[1]
        with open(source_name) as fp:
            source = fp.read()
        search_paths += [Path(source_name).parent]
    #lex = Lex(source, source_name)
    #runner = Run(lex)
    #runner.run()
    parse = Parse(source, source_name)
    body = parse.parse()
    runner = Run(search_paths)
    runner.run(body)


if __name__ == '__main__': main()
