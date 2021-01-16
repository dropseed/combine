from jinja2 import meta


def get_references_in_path(path, jinja_env, exclude_references=[]):
    """Get all (recursive) references that go into this file"""
    references = set()

    with open(path, "r") as f:
        ast = jinja_env.parse(f.read())

    these_references = list(meta.find_referenced_templates(ast))
    # references += set(these_references)

    for ref in these_references:
        if ref in references:
            continue
        else:
            references.add(ref)
            references |= set(
                get_references_in_path(
                    get_path_for_reference(ref, jinja_env),
                    jinja_env,
                    exclude_references=list(references),
                )
            )

    return list(references)


def get_path_for_reference(reference, jinja_env):
    return jinja_env.get_template(reference).filename
