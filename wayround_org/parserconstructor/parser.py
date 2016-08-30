
import wayround_org.parserconstructor.utils
import wayround_org.parserconstructor.ast
import wayround_org.parserconstructor.abnf_abnf


def parse(text, rule_set, root_rule_name):
    """
    Parse text and make complete ast from it
    """

    if not isinstance(text, str):
        raise TypeError("`text' must be str")

    if not isinstance(rule_set, wayround_org.parserconstructor.utils.Rules):
        raise TypeError(
            "`rule_set' must be inst of "
            "wayround_org.parserconstructor.utils.Rules"
            )

    if not isinstance(root_rule_name, str):
        raise TypeError("`root_rule_name' must be str")

    if root_rule_name not in rule_set:
        raise ValueError(
            "`root_rule_name' \"{}\" not found in `rule_set'".format(
                root_rule_name
                )
            )

    rule_evaluator = rule_set[root_rule_name]

    ret = None

    if callable(rule_evaluator):
        ret = rule_evaluator(
            text,
            0,
            len(text),
            rule_set,
            root_rule_name
            )

    return ret
