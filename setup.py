from setuptools import setup, find_packages

with open("README.md","r",encoding="utf-8") as readme:
	long_description = readme.read()

with open("requirements.txt","r",encoding="utf-8") as requirements:
	install_requires = requirements.read().splitlines()
 
setup(
  name="whisper-yt-subtitle",
  author="chanasia",
  description="Generate subtitle from youtube with Whisper.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=install_requires,
  python_requires=">=3.10",
  packages=find_packages(),
  zip_safe=False,
)