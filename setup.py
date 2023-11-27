from setuptools import setup

setup(
    name="estimating_uncertainties_enso",
    python_requires=">=3.8",
    version="0.1.0",
    packages=["estimating_uncertainties_enso", "estimating_uncertainties_enso.compute_lib",
              "estimating_uncertainties_enso.figure_scripts", "estimating_uncertainties_enso.figure_templates"],
    url="",
    license="Apache-2.0",
    author="yyplanton",
    author_email="yann.planton@locean.ipsl.fr",
    description="code for the paper estimating_uncertainties_in_simulated_ENSO submitted to JAMES"
)
