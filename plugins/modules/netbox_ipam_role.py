#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_ipam_role
short_description: Creates or removes ipam roles from Netbox
description:
  - Creates or removes ipam roles from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynetbox
version_added: "0.1.0"
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
    type: str
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
    type: str
  data:
    type: dict
    description:
      - Defines the ipam role configuration
    suboptions:
      name:
        description:
          - Name of the ipam role to be created
        required: true
        type: str
      weight:
        description:
          - The weight of the ipam role to be created
        type: int
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: "yes"
    type: bool
"""

EXAMPLES = r"""
- name: "Test Netbox module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create ipam role within Netbox with only required information
      netbox_ipam_role:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test IPAM Role 
        state: present

    - name: Delete ipam role within netbox
      netbox_ipam_role:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test IPAM Role
        state: absent
"""

RETURN = r"""
role:
  description: Serialized object as created or already existent within Netbox
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox_community.ansible_modules.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
)
from ansible_collections.netbox_community.ansible_modules.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_IPAM_ROLES,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = dict(
        netbox_url=dict(type="str", required=True),
        netbox_token=dict(type="str", required=True, no_log=True),
        data=dict(type="dict", required=True),
        state=dict(required=False, default="present", choices=["present", "absent"]),
        validate_certs=dict(type="bool", default=True),
    )
    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_ipam_role = NetboxIpamModule(module, NB_IPAM_ROLES)
    netbox_ipam_role.run()


if __name__ == "__main__":
    main()
