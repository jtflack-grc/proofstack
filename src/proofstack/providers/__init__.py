import os
from proofstack.providers.mock import MockProvider
from proofstack.providers.nvidia_nim import NvidiaNimProvider

def get_provider():
    name = os.getenv("PROOFSTACK_PROVIDER", "mock").strip().lower()
    if name == "mock":
        return MockProvider()
    if name == "nvidia":
        return NvidiaNimProvider()
    raise ValueError(f"Unknown PROOFSTACK_PROVIDER: {name}")
