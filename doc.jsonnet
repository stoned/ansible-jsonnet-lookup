{
  person1: {
    name: "Alice",
    welcome: "Hello " + self.name + "!",
  },
  person2: self.person1 { name: "Bob" },
  person3: self.person1 {
     name: std.native("ansible_expr")("ansible_hostname"),
     two: 1 + 1,
     jinja_two: std.parseInt(std.native("ansible_expr")("{{ 1 + 1 }}")),
     alist: std.native("ansible_expr")("ansible_all_ipv4_addresses"),
     an_ext_var: std.extVar("avar"),
     arch: std.extVar("anothervar"),
  },
}
