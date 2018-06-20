# Jsonnet lookup plugin for Ansible

A first try at a [Jsonnet][1] [lookup plugin for Ansible][2].

Install Python package `jsonnet` and then try:

	$ ansible-playbook -i localhost, -c local set-fact.yml -v


[1]: https://jsonnet.org/
[2]: https://docs.ansible.com/ansible/latest/user_guide/playbooks_lookups.html
