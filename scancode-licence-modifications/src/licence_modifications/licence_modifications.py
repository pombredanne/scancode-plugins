# Copyright (c) 2019 AMD Inc. and others. All rights reserved.
# http://amd.com and https://github.com/AMD/scancode-toolkit/
# The ScanCode plugin software is licensed under the Apache License version 2.0.
# for any issue please email to chamohan@amd.com

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

class LicenceModifications(PostScanPlugin):

    """
    Add the "licence_modifications" attribute to a resouce if it does not contain any license 
    """

    resource_attributes = dict(licence_modifications=attr.ib(default=attr.Factory(dict)))

    sort_order = 9


    options = [
        CommandLineOption(('--licence-modifications',),
                                        is_flag=True, default=False,
                                        help='Generate a list of files in case of modified license',
                                        help_group=POST_SCAN_GROUP)
    ]

    def is_enabled(self, licence_modifications, **kwargs):
        return licence_modifications

    def process_codebase(self, codebase, licence_modifications, **kwargs):
        """
        Populate a licence_modifications mapping with license modification text 
        """
        if not self.is_enabled(licence_modifications):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                licence_score_match = set([entry.get('score') for entry in resource.licenses])
                 

            except AttributeError:
                # add licence_modifications regardless if there is license modification info or not
                resource.licence_modifications = {} 
                codebase.save_resource(resource)
                continue

            for licensemodification in licence_score_match:
                if licensemodification != '100.0':
                    modification_score = 100.00 - licensemodification
                    resource.licence_modifications = {"modinfo": "%s license percent is modified "%(modification_score) } 
                    codebase.save_resource(resource)
