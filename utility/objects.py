class SmartHashable(object):
    def __init__(self, ignore_attrs=set([])):
        self._ignore = ignore_attrs.union(self._get_methods()).union({'_ignore', '_important'})
        self._important = None

    def _get_methods(self):
        return set([method for method in dir(self) if callable(getattr(self, method))])

    def _resolve_important(self):
        if self._important is None:
            self._important = [d for d in dir(self) if d not in self._ignore
                                     and not d.startswith('__')]
        return [getattr(self, d) for d in self._important]

    def __hash__(self):
        return hash(tuple(self._resolve_important()))

    def __eq__(self, other):
        if not isinstance(other, SmartHashable):
            return False
        return all([t[0] == t[1] for t in
                    zip(self._resolve_important(), other._resolve_important())])

    def __ne__(self, other):
        return not self.__eq__(other)
