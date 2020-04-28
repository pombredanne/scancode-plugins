# Copyright (c) 2019 AMD Inc. and others. All rights reserved.

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

class OnlyLicensesTitles(PostScanPlugin):

    """
    Add the "only_licenses_titles" attribute to a resouce if it does not contain any license 

    """

    resource_attributes = dict(only_licenses_titles=attr.ib(default=attr.Factory(dict)))

    sort_order = 9


    options = [
        CommandLineOption(('--only-licenses-titles',),
                                        is_flag=True, default=False,
                                        help='Generate a list of files with only license titles',
                                        help_group=POST_SCAN_GROUP)
    ]

    def is_enabled(self, only_licenses_titles, **kwargs):
        return only_licenses_titles 

    def process_codebase(self, codebase, only_licenses_titles, **kwargs):
        """
        Populate a only_licenses_titles only_licenses_titles mapping 
        """
        if not self.is_enabled(only_licenses_titles):
            return

        for resource in codebase.walk(topdown=True):
            if not resource.is_file:
                continue

            try:
                resource_start_line = set([entry.get('start_line') for entry in resource.licenses])
                resource_end_line   = set([entry.get('end_line') for entry in resource.licenses])
         

            except AttributeError:
                resource.only_licenses_titles = {}
                codebase.save_resource(resource)
                continue

            for singlelinetitles in resource_start_line:
                    resource.only_licenses_titles = {"LineStart": resource_start_line, "LineEnd": resource_end_line}
                    codebase.save_resource(resource)
