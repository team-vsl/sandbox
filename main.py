# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shows how to use the <noloc>Converse</noloc> API with Anthropic Claude 3 Sonnet (on demand).
"""

import logging
from datetime import datetime
from pathlib import Path
import os

# Import from services
from services.data_contracts import generate_datacontract

# Import from utils
from utils.file import write_to_file

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    """
    Entrypoint for Anthropic Claude 3 Sonnet example.
    """

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    user_input = input("Enter your question: ")

    try:
        result, messages = generate_datacontract(user_input)

        # Show the complete conversation.
        for message in messages:
            print(f"Role: {message['role']}")
            for content in message["content"]:
                print(f"Text: {content['text']}")
            print()

        print(
            "Wrote to file: ",
            write_to_file("draft-datacontract", result),
        )

    except Exception as err:
        print(f"A client error occured: {str(err)}")


if __name__ == "__main__":
    main()
