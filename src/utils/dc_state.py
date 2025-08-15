class DataContractState:
    """
    Enum-like class representing the possible states of a data contract.

    Attributes:
        Rejected (str): The data contract has been reviewed and rejected.
        Pending (str): The data contract is awaiting review or decision.
        Approved (str): The data contract has been reviewed and approved.

    This class is typically used to standardize state values when handling
    data contract decisions in the VPBank Challenge #23 API.
    """

    Rejected = "rejected"
    Pending = "pending"
    Approved = "approved"
