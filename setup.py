from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "TradingView API - Python implementation for anonymous access to TradingView market data"

setup(
    name="TradingView-API",
    version="1.0.1",
    author="TradingView Python API Contributors",
    author_email="",
    description="Python implementation for anonymous access to TradingView market data via WebSocket and symbol search",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/kaash04/TradingView-API-Python",
    packages=["TradingView"],
    classifiers=[
        "Development Status :: 5 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "websockets>=10.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="tradingview, websocket, api, financial, trading, market-data",
    project_urls={
        "Bug Reports": "https://github.com/kaash04/TradingView-API-Python/issues",
        "Source": "https://github.com/kaash04/TradingView-API-Python",
        "Documentation": "https://github.com/kaash04/TradingView-API-Python#readme",
    },
) 