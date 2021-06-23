# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""The step definitions for workflow."""
from __future__ import absolute_import

from typing import List, Union

import attr

from sagemaker.workflow.entities import Expression
from sagemaker.workflow.properties import PropertyFile


@attr.s
class Join(Expression):
    """Join together properties.

    Attributes:
        values (List[Union[PrimitiveType, Parameter]]): The primitive types
            and parameters to join.
        on_str (str): The string to join the values on (Defaults to "").
    """

    on: str = attr.ib(factory=str)
    values: List = attr.ib(factory=list)

    @property
    def expr(self):
        """The expression dict for a `Join` function."""
        return {
            "Std:Join": {
                "On": self.on,
                "Values": [
                    value.expr if hasattr(value, "expr") else value for value in self.values
                ],
            },
        }


@attr.s
class JsonGet(Expression):
    """Get JSON properties from PropertyFiles.

    Attributes:
        processing_step_name (str): The step name of the `sagemaker.workflow.steps.ProcessingStep`
            from which to get the property file.
        property_file (Union[PropertyFile, str]): Either a PropertyFile instance
            or the name of a property file.
        json_path (str): The JSON path expression to the requested value.
    """

    processing_step_name: str = attr.ib()
    property_file: Union[PropertyFile, str] = attr.ib()
    json_path: str = attr.ib()

    @property
    def expr(self):
        """The expression dict for a `JsonGet` function."""
        if isinstance(self.property_file, PropertyFile):
            name = self.property_file.name
        else:
            name = self.property_file

        if not isinstance(self.processing_step_name, str):
            raise ValueError("processing_step_name passed in is not instance of a str")

        return {
            "Std:JsonGet": {
                "PropertyFile": {"Get": f"Steps.{self.processing_step_name}.PropertyFiles.{name}"},
                "Path": self.json_path,
            }
        }
