# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# http://amd.com and https://github.com/AMD/scancode-toolkit/
# The ScanCode plugin software is licensed under the Apache License version 2.0.
# Data generated with ScanCode require an acknowledgment.
# ScanCode is a trademark of AMD Inc.
#
# You may not use this software except in compliance with the License.
# You may obtain a copy of the License at: http://apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# When you publish or redistribute any data created with ScanCode or any ScanCode
# derivative work, you must accompany this data with the following acknowledgment:
#
#  Generated with ScanCode and provided on an "AS IS" BASIS, WITHOUT WARRANTIES
#  OR CONDITIONS OF ANY KIND, either express or implied. No content created from
#  ScanCode should be considered or used as legal advice. Consult an Attorney
#  for any legal advice.
#  ScanCode is a free software code scanning tool from AMD Inc. and others.
#  Visit https://github.com/AMD/scancode-toolkit/ for support and download.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
from os.path import exists
from os.path import isdir

import attr

from commoncode import saneyaml
from plugincode.post_scan import PostScanPlugin
from plugincode.post_scan import post_scan_impl
from scancode import CommandLineOption
from scancode import POST_SCAN_GROUP

class NoLicenses(PostScanPlugin):

    """
    Add the "no_licenses" attribute to a resouce if it does not contain any license 
    """

    resource_attributes = dict(no_licenses=attr.ib(default=attr.Factory(dict)))

    sort_order = 9


    options = [
        CommandLineOption(('--no-licenses',),
                                        is_flag=True, default=False,
                                        help='Generate a list of no licences files',
                                        help_group=POST_SCAN_GROUP)
    ]

    def is_enabled(self, no_licenses, **kwargs):
        return no_licenses

    def process_codebase(self, codebase, no_licenses, **kwargs):
        """
        Populate a no_license mapping with four attributes: filename, label,
        icon, and color_code at the File Resource level.
        """
        if not self.is_enabled(no_licenses):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                resource_no_licenses = set([entry.get('short_name') for entry in resource.licenses])

            except AttributeError:
                # add no_licenses regardless if there is license info or not
                resource.no_licenses = {} 
                codebase.save_resource(resource)
                continue

            for license in resource_no_licenses:
                if license:
                    resource.no_licenses = "%s is Present"%(license) 
                    codebase.save_resource(resource)
