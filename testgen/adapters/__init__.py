"""Input adapters: turn a source (requirement, API spec, source code) into a
common GenerationContext that the core engine knows how to prompt with."""

from .base import GenerationContext, InputAdapter
from .requirement import RequirementAdapter

__all__ = ["GenerationContext", "InputAdapter", "RequirementAdapter"]
