# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2012 Red Hat, Inc.
# Authors:
# Thomas Woerner <twoerner@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# translation
import locale
try:
    locale.setlocale(locale.LC_ALL, "")
except locale.Error:
    import os
    os.environ['LC_ALL'] = 'C'
    locale.setlocale(locale.LC_ALL, "")

DOMAIN = 'firewalld'
import gettext
gettext.install(domain=DOMAIN)

# configuration
DAEMON_NAME = 'firewalld'
CONFIG_NAME = 'firewall-config'
APPLET_NAME = 'firewall-applet'
DATADIR = '/usr/share/' + DAEMON_NAME
CONFIG_GLADE_NAME = CONFIG_NAME + '.glade'
COPYRIGHT = '(C) 2010-2012 Red Hat, Inc.'
VERSION = '0.3.7'
AUTHORS = [
    "Thomas Woerner <twoerner@redhat.com>",
    "Jiri Popelka <jpopelka@redhat.com>",
    ]
LICENSE = _(
    "This program is free software; you can redistribute it and/or modify "
    "it under the terms of the GNU General Public License as published by "
    "the Free Software Foundation; either version 2 of the License, or "
    "(at your option) any later version.\n"
    "\n"
    "This program is distributed in the hope that it will be useful, "
    "but WITHOUT ANY WARRANTY; without even the implied warranty of "
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
    "GNU General Public License for more details.\n"
    "\n"
    "You should have received a copy of the GNU General Public License "
    "along with this program.  If not, see <http://www.gnu.org/licenses/>.")
WEBSITE = 'https://fedorahosted.org/firewalld/'

ETC_FIREWALLD = '/etc/firewalld'
FIREWALLD_CONF = ETC_FIREWALLD + '/firewalld.conf'
ETC_FIREWALLD_ZONES = ETC_FIREWALLD + '/zones'
ETC_FIREWALLD_SERVICES = ETC_FIREWALLD + '/services'
ETC_FIREWALLD_ICMPTYPES = ETC_FIREWALLD + '/icmptypes'

USR_LIB_FIREWALLD = '/usr/lib/firewalld'
FIREWALLD_ZONES = USR_LIB_FIREWALLD + '/zones'
FIREWALLD_SERVICES = USR_LIB_FIREWALLD + '/services'
FIREWALLD_ICMPTYPES = USR_LIB_FIREWALLD + '/icmptypes'

FIREWALLD_LOGFILE = '/var/log/firewalld'

FIREWALLD_DIRECT = ETC_FIREWALLD + '/direct.xml'

LOCKDOWN_WHITELIST = ETC_FIREWALLD + '/lockdown-whitelist.xml'

SYSCTL_CONFIG = '/etc/sysctl.conf'

# fallbacks: will be overloaded by firewalld.conf
FALLBACK_ZONE = "public"
FALLBACK_MINIMAL_MARK = 100
