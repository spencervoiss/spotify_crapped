import setuptools

setuptools.setup(
    name="spotify_crapped",
    version="0.1.0",
    packages=setuptools.find_packages(),
    install_requires=["pandas", "pywebview", "notebook"],
    entry_points={
        "console_scripts": [
            "spotify_crapped = spotify_crapped.main:main",
        ]
    },
    python_requires=">=3.6",
)
