import six

from contracts import contract
import re

__all__ = ['expand_string', 'get_wildcard_matches']


def flatten(seq):
    res = []
    for l in seq:
        res.extend(l)
    return res


@contract(x='str|unicode|list(str|unicode)', options='list(str|unicode)', returns='list(str|unicode)')
def expand_string(x, options):
    if isinstance(x, list):
        return flatten(expand_string(y, options) for y in x)
    elif isinstance(x, six.string_types):
        x = x.strip()
        if ',' in x:
            splat = [_ for _ in x.split(',') if _]  # remove empty
            return flatten(expand_string(y, options) for y in splat)
        elif '*' in x:
            xx = expand_wildcard(x, options)
            expanded = list(xx)
            return expanded
        else:
            return [x]
    else:
        assert False


def wildcard_to_regexp(arg):
    """ Returns a regular expression from a shell wildcard expression. """
    return re.compile(r'\A' + arg.replace('*', r'.*') + r'\Z')


def has_wildcard(s):
    return s.find('*') > -1
    
@contract(wildcard='str|unicode', universe='list(str|unicode)')
def expand_wildcard(wildcard, universe):
    ''' 
        Expands a wildcard expression against the given list.
        Raises ValueError if none found.
        
        :param wildcard: string with '*' 
        :param universe: a list of strings
    '''
    if not has_wildcard(wildcard):
        msg = 'No wildcards in %r.' % wildcard
        raise ValueError(msg)
    
    matches = list(get_wildcard_matches(wildcard, universe))
        
    if not matches:
        msg = ('Could not find matches for pattern %r in %s.' % 
                (wildcard, universe))
        raise ValueError(msg)

    return matches

def get_wildcard_matches(wildcard, universe):
    ''' 
        Expands a wildcard expression against the given list.
        Yields a sequence of strings.
        
        :param wildcard: string with '*' 
        :param universe: a list of strings
    '''     
    regexp = wildcard_to_regexp(wildcard)
    for x in universe:
        if regexp.match(x):
            yield x

