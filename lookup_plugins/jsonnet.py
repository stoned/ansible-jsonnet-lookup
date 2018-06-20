# (c) 2018, Stoned Elipot <stoned.elipot@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: jsonnet
    author: Stoned Elipot <stoned.elipot@gmail.com>
    version_added: "2.7"
    short_description: retrieve contents of file after templating with Jsonnet
    description:
      - XXX
      - XXX
    options:
      _terms:
        description: list of files to template
"""

EXAMPLES = """
- name: show templating results
  debug: msg="{{ lookup('jsonnet', 'some_template.jsonnet') }}
"""

RETURN = """
_raw:
   description: file(s) content after templating
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.template import generate_ansible_template_vars

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

try:
    import _jsonnet
    HAS_JSONNET = True
except ImportError:
    HAS_JSONNET = False


class LookupModule(LookupBase):

    def run(self, terms, variables, **kwargs):

        if not HAS_JSONNET:
            raise AnsibleError(
                "Requires the _jsonnet Python package. Try `pip install jsonnet`")

        lookup_template_vars = kwargs.get('template_vars', {})
        ret = []

        for term in terms:
            display.debug("File lookup term: %s" % term)

            lookupfile = self.find_file_in_search_path(
                variables, 'templates', term)
            display.vvvv("File lookup using %s as file" % lookupfile)
            if lookupfile:
                vars = variables.copy()
                vars.update(generate_ansible_template_vars(lookupfile))
                vars.update(lookup_template_vars)

                def ansible_expr(expr):
                    self._templar.set_available_variables(vars)
                    return self._templar.template(expr, convert_bare=True, bare_deprecated=False)

                native_callbacks = {
                    'ansible_expr': (('expr',), ansible_expr),
                }

                res = _jsonnet.evaluate_file(
                    lookupfile,
                    native_callbacks=native_callbacks, **kwargs)
                ret.append(res)
            else:
                raise AnsibleError(
                    "the template file %s could not be found for the lookup" % term)

        return ret
