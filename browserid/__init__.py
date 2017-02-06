# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""

Python library for the BrowserID identity protocol.

"""

__version__      = "2.0.0rc1"
__description__  = "Python library for the BrowserID Protocol"
__url__          = "https://github.com/mozilla/PyBrowserID"
__license__      = "MPLv2.0"
__author__       = 'Mozilla Services'
__author_email__ = 'dev-identity@lists.mozilla.org'
__keywords__     = 'authentication browserid login email'

from browserid.errors import (  # pylint: disable=W0622
    Error                    # NOQA
    , ConnectionError        # NOQA
    , TrustError             # NOAQ
    , ExpiredSignatureError  # NOQA
    , InvalidSignatureError  # NOQA
    , AudienceMismatchError  # NOQA
    , )

from browserid.verifiers.remote import RemoteVerifier  # NOQA
from browserid.verifiers.local import LocalVerifier  # NOQA


_DEFAULT_VERIFIER = None


def verify(assertion, audience=None):
    """Verify the given BrowserID assertion.

    This function uses the "best" verification method available in order to
    verify the given BrowserID assertion and return a dict of user data.  The
    best method currently involves POSTing to the hosted verifier service on
    persona.org; eventually it will do local verification.
    """
    global _DEFAULT_VERIFIER # pylint: disable=W0603
    if _DEFAULT_VERIFIER is None:
        _DEFAULT_VERIFIER = RemoteVerifier()
    return _DEFAULT_VERIFIER.verify(assertion, audience)
