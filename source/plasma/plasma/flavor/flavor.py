# Copyright (c) 2016 Intel, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from plasma.common.redfish import api as rfs
import plasma.flavor.plugins
from oslo_log import log as logging
import json
import sys
import os 

FLAVOR_PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))+ '/plugins'
logger = logging.getLogger()

def get_available_criteria():
    pluginfiles = [f.split(".")[0] 
                       for f in os.listdir(FLAVOR_PLUGIN_PATH) 
			   if os.path.isfile(os.path.join(FLAVOR_PLUGIN_PATH, f)) and not f.startswith('__') and f.endswith('.py')]
    return {"criteria" : pluginfiles}

def create_flavors(criteria):
    #criteria : comma seperated generator names (should be same as thier file name)
    respjson = []
    lst_nodes = rfs.nodes_full_list()
    for g in criteria.split(","):
       if g:
	logger.info("Calling generator : %s ." % g)
        module = __import__("plasma.flavor.plugins." + g, fromlist = ["*"])
        classobj = getattr(module, g+"Generator")
        inst = classobj(lst_nodes)
        respjson.append(inst.generate())
    return respjson
