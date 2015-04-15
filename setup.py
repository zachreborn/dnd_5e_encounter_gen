try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='dnd_5e_encounter_gen',
    version='1.1',
    packages=['monsters', 'random_encounter_builder'],
    url='https://github.com/zachreborn',
    license='BSD',
    author='Zachary Hill',
    author_email='zhill@octonetwork.com',
    description='D&D 5e Random Encounter Generator'
)
