#!/usr/bin/env python
'''
Pockyll - generate Jekyll linkposts from pocket items
'''
from __future__ import print_function
import os
import io
import sys
import datetime
import webbrowser
import yaml
from pocket import Pocket


def usage():
    usage_text = '''
    pockyll - generate Jekyll linkposts from pocket items

    Usage: pockyll <-h|--help|init|auth|sync>

    Commands:
        --help  Show this help dialog
        init    Create an empty _pockyll.yml config file
        auth    Authenticate the application against the pocket OAuth API
        sync    Create Jekyll linkposts from pocket items

    '''
    print(usage_text)


def get_config_filename():
    return os.getcwd() + '/_pockyll.yml'


def create_config():
    '''
    Creates a `_pockyll.yml` with default values in the current working
    directory.
    '''
    default_config = {
        'pocket_consumer_key': None,
        'pocket_redirect_uri': None,
        'pocket_access_token': None,
        'pocket_sync_tags': ['blog'],
        'pocket_since': None,
        'linkpost_post_dir': '_posts/linkposts',
        'linkpost_draft_dir': '_drafts/linkposts'}
    save_config(default_config)


def save_config(config, filename=get_config_filename()):
    '''
    Saves the configuration to a YAML file.
    '''
    configfile = io.open(filename, 'w', encoding='utf8')
    yaml.dump(config, configfile)
    configfile.close()


def load_config(filename=get_config_filename()):
    '''
    Loads the the configuration from a YAML file and returns
    a the configuration as a ``dict`` object.
    '''
    try:
        configfile = io.open(filename, 'r', encoding='utf8')
        config = yaml.load(configfile)
        configfile.close()
    except IOError as e:
        raise RuntimeError('Could not open the configuration file %s. '
                           'Are you in the correct directory and/or did you '
                           'run `pockyll init` prior to the current '
                           'command?' % filename)
    return config


def auth(config):
    '''
    Interactive OAuth authentication against the pocket OAuth API. Generates a
    Pocket authentication URL and directs the users webbrowser to the URL to
    authenticate pocket access for the app.

    Upon successful authentication, the function stores the `access_token` in
    the pockyll config file.
    '''
    # make sure the config is complete
    pocket_consumer_key = config.get('pocket_consumer_key', None)
    pocket_redirect_uri = config.get('pocket_redirect_uri', None)
    if pocket_consumer_key is None or pocket_redirect_uri is None:
        raise RuntimeError(
            "You need to provide pocket_consumer_key and pocket_redirect_uri "
            "in the pockyll configuration file.")
    request_token = Pocket.get_request_token(
        consumer_key=pocket_consumer_key,
        redirect_uri=pocket_redirect_uri)
    auth_url = Pocket.get_auth_url(
        code=request_token,
        redirect_uri=pocket_redirect_uri)
    # start the interactive part
    print('Directing your browser to authenticate against Pocket.')
    print('Please continue authentication in your browser.')
    print('When finished, press ENTER.')
    # Open web browser tab to authenticate with Pocket
    webbrowser.open(auth_url)  # this also works in a text shell
    # Wait for user to hit ENTER before proceeding
    raw_input()
    access_token = Pocket.get_access_token(
        consumer_key=pocket_consumer_key,
        code=request_token)
    # update the config file
    config['pocket_access_token'] = access_token
    save_config(config)
    return config


def get_list(config):
    '''
    Requests the list of items tagged with `tags` since `since`,
    sorted from newest to oldest, irrespective of their read state,
    using the short/simple JSON reprensentation.
    '''
    instance = Pocket(config.get('pocket_consumer_key'),
                      config.get('pocket_access_token'))
    tags = config.get('pocket_sync_tags', 'all')
    since = config.get('pocket_since', None)
    items_list = instance.get(state='all',
                              tag=tags,
                              sort='newest',
                              since=since,
                              detailType='simple')
    return items_list


def create_linkpost(config, item_id, title, url, timestamp, is_draft=True):
    path = ''
    if not is_draft:
        path = config.get("linkpost_post_dir", "_posts/linkposts")
    else:
        path = config.get("linkpost_draft_dir", "_drafts/linkposts")
    if not os.path.exists(path):
        raise RuntimeError(
            "The linkpost destination path %s does not exist. Please "
            "double-check spelling and create the destination path if "
            "applicable." % path)
    linkfilename = "%s/%s-%s.markdown" % (
        path, timestamp.strftime('%Y-%m-%d'), item_id)
    # skip if file exists
    if os.path.exists(linkfilename):
        raise IOError('Doggedly refusing to overwrite existing file: %s' %
                      linkfilename)
    linkfile = io.open(linkfilename, 'w', encoding='utf8')
    text = '''---
title: '%s'
date: %s
type: 'reference'
ref: %s
---

[%s](%s)
''' % (title, timestamp.strftime('%Y-%m-%dT%H:%M:%S%z'), url, title, url)
    linkfile.write(text)
    linkfile.close()


def sync(config):
    print('Requesting new items from Pocket API...')
    if config.get('pocket_access_token', None) is None:
        raise RuntimeError("Please authenticate the app before syncing.")
    response = get_list(config)
    # [0] is the result, [1] is the HTTP return conde and headers
    bookmarks = response[0]['list']
    n_items = len(bookmarks)
    if n_items > 0:
        print('Syncing %d items.' % n_items)
        n_skipped = 0
        n_drafts = 0
        # pull relevant info from the API response
        # TODO: support tags
        for key, item in bookmarks.items():
            # make sure we have an URL and and item ID
            url = item.get('given_url', None)
            item_id = item.get('resolved_id', None)
            if not all([url, item_id]):
                print('Skipping incomplete item: %s' % str([item_id, url]))
                n_skipped = n_skipped + 1
                continue
            # pull the remaining data
            # check if we have a proper title
            title = item.get('resolved_title', None)
            is_draft = False
            if title in [None, '']:
                is_draft = True
                n_drafts = n_drafts + 1
            # supply a current timestamp, if necessary
            tmp = item.get('time_added', None)
            timestamp = None
            if tmp is not None:
                timestamp = datetime.datetime.utcfromtimestamp(
                    long(item['time_added']))
            else:
                timestamp = datetime.datetime.now()
            # create the linkpost
            try:
                msg = "Linking to POSTs:  %s" % str([title, url, item_id])
                if is_draft:
                    msg = "Linking to DRAFTs: %s" % str([title, url, item_id])
                create_linkpost(config, item_id, title,
                                url, timestamp, is_draft)
                print(msg)
            except IOError as e:
                print("Skipping: %s" % e.message)
        # update timestamp
        config['pocket_since'] = response[0]['since']
        save_config(config)
        print('Done (%d posts/%d drafts/%d skipped).' %
              (n_items - n_drafts - n_skipped, n_drafts, n_skipped))
    else:
        print('No new bookmarks. Done.')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        # the argument set is so simple that argparse is overkill
        if len(argv) != 2:
            raise RuntimeError('Wrong number of arguments.')
        command = argv[1]
        if command == 'init':
            create_config()
        elif command == 'auth':
            auth(load_config())
        elif command == 'sync':
            sync(load_config())
        elif command in ['-h', '--help']:
            usage()
        else:
            raise RuntimeError('Invalid command')
    except Exception as e:
        print('ERROR: %s' % e.message, file=sys.stderr)
        usage()
        exit(1)

if __name__ == '__main__':
    main(sys.argv)
    exit(0)
