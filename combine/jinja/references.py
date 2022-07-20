from typing import List, Optional
from jinja2 import meta, Environment


def get_references_in_path(path: str, jinja_env: Environment) -> List[str]:
    """Get all (recursive) references that go into this file"""

    with open(path, "r") as f:
        ast = jinja_env.parse(f.read())

    these_references = list(meta.find_referenced_templates(ast))

    references = set()

    for ref in these_references:
        if ref in references or not ref:
            continue
        else:
            references.add(ref)
            reference_path = get_path_for_reference(ref, jinja_env)
            if reference_path:
                references |= set(
                    get_references_in_path(
                        reference_path,
                        jinja_env,
                    )
                )

    return list(references)


def get_path_for_reference(reference: str, jinja_env: Environment) -> Optional[str]:
    return jinja_env.get_template(reference).filename
