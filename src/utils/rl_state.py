class RulesetState:
    """
    Enum-like class representing the possible states of a ruleset.

    Attributes:
        Active (str): The rulset has been used.
        Inactive (str): The rulset is awaiting review or decision.

    This class is typically used to standardize state values when handling
    data contract decisions in the VPBank Challenge #23 API.
    """

    Active = "active"
    Inactive = "inactive"
